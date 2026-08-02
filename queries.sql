--D2 8 Analytical Queries

-- 1. Top 10 KBLI by total investment for Q2 2026.
SELECT 
    k.kbli_kode, 
    k.kbli_nama, 
    SUM(f.investasi_rp_juta) AS total_investasi_rp
FROM fakta_investasi f
JOIN dim_kbli k ON f.kbli_id = k.id
WHERE f.periode = '2026 - Triwulan 2'
GROUP BY k.kbli_kode, k.kbli_nama
ORDER BY total_investasi_rp DESC
LIMIT 10;

-- 2. Total investment per province, with its percentage of the national total.
WITH national_total AS (
    SELECT SUM(investasi_rp_juta) AS grand_total 
    FROM fakta_investasi 
    WHERE periode = '2026 - Triwulan 2'
)
SELECT 
    p.nama AS provinsi,
    SUM(f.investasi_rp_juta) AS total_investasi_rp,
    ROUND((SUM(f.investasi_rp_juta) / (SELECT grand_total FROM national_total)) * 100, 4) AS persentase_nasional
FROM fakta_investasi f
JOIN dim_provinsi p ON f.provinsi_id = p.id
WHERE f.periode = '2026 - Triwulan 2'
GROUP BY p.nama
ORDER BY total_investasi_rp DESC;

-- 3. For each province, its single largest KBLI by investment. (Window function.)
WITH ranked_kbli AS (
    SELECT 
        p.nama AS provinsi,
        k.kbli_nama,
        SUM(f.investasi_rp_juta) AS total_investasi_rp,
        ROW_NUMBER() OVER(PARTITION BY p.nama ORDER BY SUM(f.investasi_rp_juta) DESC) as rn
    FROM fakta_investasi f
    JOIN dim_provinsi p ON f.provinsi_id = p.id
    JOIN dim_kbli k ON f.kbli_id = k.id
    WHERE f.periode = '2026 - Triwulan 2'
    GROUP BY p.nama, k.kbli_nama
)
SELECT provinsi, kbli_nama, total_investasi_rp
FROM ranked_kbli
WHERE rn = 1;

-- 4. Provinces whose average investment per project exceeds the national average.
WITH province_avg AS (
    SELECT p.nama AS provinsi, AVG(f.investasi_rp_juta) AS rata_rata_provinsi
    FROM fakta_investasi f
    JOIN dim_provinsi p ON f.provinsi_id = p.id
    GROUP BY p.nama
),
national_avg AS (
    SELECT AVG(investasi_rp_juta) AS rata_rata_nasional
    FROM fakta_investasi
)
SELECT p.provinsi, ROUND(p.rata_rata_provinsi, 2) AS rata_rata_provinsi
FROM province_avg p
CROSS JOIN national_avg n
WHERE p.rata_rata_provinsi > n.rata_rata_nasional
ORDER BY p.rata_rata_provinsi DESC;

-- 5. KBLI codes present in Q2 but absent in Q1 new sectors.
SELECT DISTINCT k.kbli_kode, k.kbli_nama
FROM fakta_investasi f
JOIN dim_kbli k ON f.kbli_id = k.id
WHERE f.periode = '2026 - Triwulan 2'
AND k.id NOT IN (
    SELECT kbli_id 
    FROM fakta_investasi 
    WHERE periode = '2026 - Triwulan 1'
);

-- 6. Quarter-over-quarter growth per province: Q1 value, Q2 value, % change. 
WITH q1_data AS (
    SELECT p.nama AS provinsi, SUM(f.investasi_rp_juta) as total_q1
    FROM fakta_investasi f
    JOIN dim_provinsi p ON f.provinsi_id = p.id
    WHERE f.periode = '2026 - Triwulan 2'
    GROUP BY p.nama
),
q2_data AS (
    SELECT p.nama AS provinsi, SUM(f.investasi_rp_juta) as total_q2
    FROM fakta_investasi f
    JOIN dim_provinsi p ON f.provinsi_id = p.id
    WHERE f.periode = '2026 - Triwulan 2'
    GROUP BY p.nama
)
SELECT 
    COALESCE(q1.provinsi, q2.provinsi) AS provinsi,
    COALESCE(q1.total_q1, 0) AS q1_value,
    COALESCE(q2.total_q2, 0) AS q2_value,
    CASE 
        WHEN q1.total_q1 IS NULL OR q1.total_q1 = 0 THEN NULL
        ELSE ROUND(((q2.total_q2 - q1.total_q1) / q1.total_q1) * 100, 2)
    END AS percentage_change
FROM q1_data q1
FULL OUTER JOIN q2_data q2 ON q1.provinsi = q2.provinsi
ORDER BY percentage_change DESC NULLS LAST;

-- 7. Cumulative running share of investment by KBLI, ordered descending. (Window function.)
WITH kbli_totals AS (
    SELECT 
        k.kbli_kode, 
        k.kbli_nama, 
        SUM(f.investasi_rp_juta) AS total_investasi
    FROM fakta_investasi f
    JOIN dim_kbli k ON f.kbli_id = k.id
    WHERE f.periode = '2026 - Triwulan 2'
    GROUP BY k.kbli_kode, k.kbli_nama
),
running_totals AS (
    SELECT 
        kbli_kode,
        kbli_nama,
        total_investasi,
        SUM(total_investasi) OVER(ORDER BY total_investasi DESC) AS cumulative_investasi,
        SUM(total_investasi) OVER() AS grand_total
    FROM kbli_totals
)
SELECT 
    kbli_kode,
    kbli_nama,
    total_investasi,
    cumulative_investasi,
    ROUND((cumulative_investasi / grand_total) * 100, 2) AS cumulative_share_percentage
FROM running_totals
ORDER BY total_investasi DESC;

-- 8. Top 3 KBLI within each island group, ranked. (Window function with partition.)
WITH island_kbli_rank AS (
    SELECT 
        p.pulau,
        k.kbli_nama,
        SUM(f.investasi_rp_juta) AS total_investasi_rp,
        RANK() OVER(PARTITION BY p.pulau ORDER BY SUM(f.investasi_rp_juta) DESC) as rnk
    FROM fakta_investasi f
    JOIN dim_provinsi p ON f.provinsi_id = p.id
    JOIN dim_kbli k ON f.kbli_id = k.id
    WHERE f.periode = '2026 - Triwulan 2'
    GROUP BY p.pulau, k.kbli_nama
)
SELECT pulau, kbli_nama, total_investasi_rp, rnk
FROM island_kbli_rank
WHERE rnk <= 3
ORDER BY pulau, rnk;


-- D3. Query Optimization
SELECT 
    p.nama, 
    COUNT(*) AS jumlah, 
    ROUND(AVG(f.investasi_rp_juta), 2) AS rata2
FROM fakta_investasi f
INNER JOIN dim_provinsi p ON f.provinsi_id = p.id
WHERE f.investasi_rp_juta > 0
  AND f.periode LIKE '2026%'
GROUP BY p.nama
HAVING COUNT(*) > 5
ORDER BY rata2 DESC;
