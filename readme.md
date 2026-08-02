# Data Management Analyst Test - Athallah Anargya Yogapranata

Scrapes BKPM investment realization data (Q2 2026), cleans it, and aggregates by KBLI and wilayah.

## ⚙️ Setup

Karena pengembangan utama dilakukan di lingkungan Google Colab, struktur ini merepresentasikan repositori untuk dijalankan secara lokal (setelah diunduh dari Colab).

```bash
git clone <repo-url> && cd <repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Setup
```bash
python scraper.py        # downloads ~33k rows -> data/raw/investasi_raw.jsonl
python transform.py      # cleans -> data/clean/investasi_clean.parquet (or .csv)
python aggregate.py      # aggregations -> data/marts/
```

## Results
Rows scraped: 33.641
Total investment: Rp 511.8 Trillion

Top 10 Provinces with their top KBLI:
1. **Daerah Khusus Ibukota Jakarta** (Total Investasi: **Rp94.877.459,98 juta**) – **Perdagangan Besar, Bukan Mobil dan Sepeda Motor (KBLI 46)** (Investasi: **Rp10.604.441,67 juta**)

2. **Jawa Barat** (Total Investasi: **Rp61.340.527,85 juta**) – **Industri Kendaraan Bermotor, Trailer dan Semi Trailer (KBLI 29)** (Investasi: **Rp8.965.119,78 juta**)

3. **Maluku Utara** (Total Investasi: **Rp40.246.969,99 juta**) – **Industri Logam Dasar (KBLI 24)** (Investasi: **Rp34.853.134,95 juta**)

4. **Jawa Timur** (Total Investasi: **Rp40.093.855,72 juta**) – **Real Estat (KBLI 68)** (Investasi: **Rp4.808.374,09 juta**)

5. **Sulawesi Tengah** (Total Investasi: **Rp36.595.135,60 juta**) – **Industri Logam Dasar (KBLI 24)** (Investasi: **Rp28.922.691,47 juta**)

6. **Banten** (Total Investasi: **Rp31.894.725,02 juta**) – **Real Estat (KBLI 68)** (Investasi: **Rp6.496.380,68 juta**)

7. **Jawa Tengah** (Total Investasi: **Rp25.526.087,06 juta**) – **Industri Kayu, Barang dari Kayu dan Gabus (KBLI 16)** (Investasi: **Rp4.600.258,18 juta**)

8. **Riau** (Total Investasi: **Rp20.230.430,43 juta**) – **Pergudangan dan Aktivitas Penunjang Angkutan (KBLI 52)** (Investasi: **Rp7.445.906,89 juta**)

9. **Kalimantan Timur** (Total Investasi: **Rp18.091.417,70 juta**) – **Aktivitas Jasa Penunjang Pertambangan (KBLI 9)** (Investasi: **Rp3.186.697,01 juta**)

10. **Kepulauan Riau** (Total Investasi: **Rp16.587.118,40 juta**) – **Industri Komputer, Barang Elektronik dan Optik (KBLI 26)** (Investasi: **Rp2.287.079,82 juta**)

80% Investment KBLI: It takes 26 KBLI codes to reach 80% of the total investment.

80% Investment Provinces: It takes **12** provinces to reach 80% of the total investment.

Jawa vs Luar Jawa: Jawa accounts for **69%** of investment, while Luar Jawa accounts for **31%**.

Highest Investment per Worker: **Papua Tengah** has the highest investment per worker (**Rp 9.201,83 juta/tki**).


## 🔍 How I found the data (Task A1.2)

Instead of parsing complex and fragile HTML tables with BeautifulSoup, I opened the browser's Developer Tools and navigated to the **Network** tab (filtered by Fetch/XHR). When interacting with the data table (e.g., clicking the next page), I observed a clean JSON endpoint being called by the DataTables plugin: 

`https://data.bkpm.go.id/data`

This endpoint accepts `GET` requests with DataTables query parameters. The crucial parameters allowing me to fetch the raw data systematically without dealing with UI rendering are:
* `start`: Acts as the pagination offset (e.g., 0, 1000, 2000).
* `length`: Acts as the limit or page size (number of records per request).
* `dataset_detail_parent_id`: The unique UUID for this specific dataset (`15605157-8247-4bef-b387-0b23719fe976`).

## Decisions and Tradeoff

Scraper Page Size (Task A2.9): I chose a page size of 100 per request, resulting in 330 total requests. This size balances the need to minimize total HTTP requests to the government server (politeness) while avoiding payloads that are too large and prone to connection timeouts.

Hidden Characters (Task B1.2): I discovered a Byte Order Mark (BOM) character (\ufeff) hidden in the column names, likely originating from how the source system exported the CSV/JSON. This causes df["periode"] to fail because the actual key is \ufeffperiode. I resolved this by stripping .replace('\ufeff', '') from all column headers during the extraction phase.

KBLI as String (Task B1.4): The kbli_kode is explicitly cast and kept as a zero-padded string (e.g., "07", not 7). This is crucial because KBLI codes are categorical identifiers, not quantitative measures. Converting them to integers drops leading zeros, which would break foreign-key relationships when joining this data to standard KBLI reference tables.

## Known limitations
Development Environment: The initial pipeline and exploration were developed using Google Colab due to local machine constraints. While the code has been modularized into .py scripts (scraper.py, transform.py, aggregate.py) for the final submission, full end-to-end local execution with Docker/Airflow was not implemented.

## Time Spent

Part A (Scraping): 30 hours

Part B (Cleaning): 30 minutes

Part C (Aggregation): 2 hours
