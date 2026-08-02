import pandas as pd
import json
import re

def clean_column_names(columns):
    return [re.sub(r'[\u200b\ufeff]', '', str(col)).strip() for col in columns]

def parse_id_number(val):

    if pd.isna(val) or val == "":
        return 0.0
    val_str = str(val).strip()

    val_str = val_str.replace('.', '')
    val_str = val_str.replace(',', '.')

    try:
        return float(val_str)
    except ValueError:
        return None

def extract_kbli(val):
    match = re.match(r'^\((\d{2})-(\d{4})\)\s*(.*)$', str(val).strip())
    if match:
        return match.group(1), match.group(2), match.group(3).strip()
    return None, None, None

def check_suspect(row):
    if row['investasi_rp_juta'] < 0 or row['investasi_us_ribu'] < 0:
        return True
    if row['investasi_rp_juta'] == 0 and row['investasi_us_ribu'] == 0:
        return True
    if pd.isna(row['provinsi']) or str(row['provinsi']).strip() == "":
        return True
    if pd.isna(row['kbli_kode']):
        return True

    return False

def main():
    print("Memulai proses transformasi data...")

    data = []
    with open('/content/sample_data/investasi_raw.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

    df = pd.DataFrame(data)

    df.columns = clean_column_names(df.columns)

    df['investasi_rp_juta'] = df['investasi_rp_juta'].apply(parse_id_number)
    df['investasi_us_ribu'] = df['investasi_us_ribu'].apply(parse_id_number)

    df['tki'] = pd.to_numeric(df['tki'], errors='coerce').fillna(0).astype(int)

    df[['kbli_kode', 'kbli_versi', 'kbli_nama']] = df['deskripsi_kbli_2digit'].apply(
        lambda x: pd.Series(extract_kbli(x))
    )

    df['provinsi'] = df['provinsi'].str.strip().str.title()
    df['kabupaten_kota'] = df['kabupaten_kota'].str.strip().str.title()

    string_cols = df.columns.difference(['investasi_rp_juta', 'investasi_us_ribu', 'tki'])
    df[string_cols] = df[string_cols].astype(str)

    df['is_suspect'] = df.apply(check_suspect, axis=1)

    total_triliun_rp = df['investasi_rp_juta'].sum() / 1_000_000

    print(f"Total baris awal  : {len(df)}")
    print(f"Baris is_suspect  : {df['is_suspect'].sum()}")
    print(f"Total Investasi   : Rp {total_triliun_rp:,.2f} Triliun")

    df.to_csv('data/clean/investasi_clean.csv', index=False)
    print("Data bersih berhasil disimpan")

    
if __name__ == "__main__":
    main()