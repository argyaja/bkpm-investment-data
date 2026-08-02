import pandas as pd
import json
import os

def determine_suspect_reason(row):
    """Fungsi pembantu untuk mendiagnosis alasan is_suspect"""
    reasons = []
    if row['investasi_rp_juta'] < 0 or row['investasi_us_ribu'] < 0:
        reasons.append("Nilai investasi negatif")
    if row['investasi_rp_juta'] == 0 and row['investasi_us_ribu'] == 0:
        reasons.append("Investasi Rp dan USD keduanya nol")
    if pd.isna(row['provinsi']) or str(row['provinsi']).strip() == "":
        reasons.append("Provinsi kosong")
    if pd.isna(row['kbli_kode']) or str(row['kbli_kode']).strip() == "":
        reasons.append("Kode KBLI gagal diekstrak/tidak valid")

    return ", ".join(reasons) if reasons else "Tidak diketahui"

def main():
    print("Men-generate quality report...")

    os.makedirs('reports', exist_ok=True)

    raw_file = '/data/raw/investasi_raw.jsonl'
    clean_file = '/data/clean/investasi_clean.csv'

    rows_in = 0
    with open(raw_file, 'r', encoding='utf-8') as f:
        rows_in = sum(1 for _ in f)

    df = pd.read_csv(clean_file)
    rows_out = len(df)

    null_counts = df.isnull().sum()
    null_percentages = (null_counts / rows_out) * 100
    null_df = pd.DataFrame({'Null Count': null_counts, 'Percentage (%)': null_percentages})

    numeric_cols = ['investasi_rp_juta', 'investasi_us_ribu', 'tki']
    stats_df = df[numeric_cols].agg(['min', 'max', 'mean', 'median', 'sum']).T

    distinct_cols = ['provinsi', 'kabupaten_kota', 'nama_sektor', 'negara']
    distinct_counts = {col: df[col].nunique() for col in distinct_cols if col in df.columns}

    suspect_df = df[df['is_suspect'] == True].copy()
    suspect_df['reason'] = suspect_df.apply(determine_suspect_reason, axis=1)

    grand_total_triliun = df['investasi_rp_juta'].sum() / 1_000_000
    bkpm_published_figure = "511.8"

    with open('reports/quality_report.md', 'w', encoding='utf-8') as f:
        f.write("# Data Quality Report\n\n")

        f.write("## 1. Row Counts\n")
        f.write(f"- **Rows In (Raw):** {rows_in}\n")
        f.write(f"- **Rows Out (Clean):** {rows_out}\n")
        f.write(f"- **Difference:** {rows_in - rows_out}\n\n")

        f.write("## 2. Null Count & Percentage\n")
        f.write(null_df.to_markdown() + "\n\n")

        f.write("## 3. Numeric Statistics\n")
        f.write(stats_df.to_markdown() + "\n\n")

        f.write("## 4. Distinct Value Counts\n")
        for col, count in distinct_counts.items():
            f.write(f"- **{col}**: {count} distinct values\n")
        f.write("\n")

        f.write("## 5. Suspect Rows Analysis\n")
        f.write(f"Total suspect rows: {len(suspect_df)}\n\n")
        if not suspect_df.empty:
            report_suspects = suspect_df[['provinsi', 'investasi_rp_juta', 'investasi_us_ribu', 'reason']]
            f.write(report_suspects.head(50).to_markdown(index=False) + "\n")
            f.write("\n*(Menampilkan maksimal 50 baris pertama)*\n\n")

        f.write("## 6. Grand Total Reconciliation\n")
        f.write(f"- **Calculated Total:** Rp {grand_total_triliun:,.2f} Triliun\n")
        f.write(f"- **Published BKPM Figure:** Rp {bkpm_published_figure} Triliun\n")

    print("Laporan berhasil dibuat di reports/quality_report.md!")

if __name__ == "__main__":
    main()