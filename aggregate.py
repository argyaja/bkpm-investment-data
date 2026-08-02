import pandas as pd
import os

JAWA_PROVINCES = [
    'DKI JAKARTA', 'JAWA BARAT', 'JAWA TENGAH',
    'DAERAH ISTIMEWA YOGYAKARTA', 'JAWA TIMUR', 'BANTEN'
]

def get_pulau(provinsi):
    prov = str(provinsi).upper()
    if prov in JAWA_PROVINCES: return 'Jawa'
    if 'SUMATERA' in prov or prov in ['ACEH', 'RIAU', 'JAMBI', 'BENGKULU', 'LAMPUNG', 'KEPULAUAN BANGKA BELITUNG', 'KEPULAUAN RIAU']: return 'Sumatera'
    if 'KALIMANTAN' in prov: return 'Kalimantan'
    if 'SULAWESI' in prov or prov == 'GORONTALO': return 'Sulawesi'
    if 'MALUKU' in prov or 'PAPUA' in prov: return 'Maluku & Papua'
    if 'NUSA TENGGARA' in prov or prov == 'BALI': return 'Bali & Nusa Tenggara'
    return 'Lainnya'

def main():
    print("Mulai proses agregasi data (Part C)...")
    os.makedirs('data/marts', exist_ok=True)

    df = pd.read_csv('data/clean/investasi_clean.csv')

    df_valid = df[df['is_suspect'] == False].copy()

    df_valid['is_jawa'] = df_valid['provinsi'].apply(lambda x: 'Jawa' if str(x).upper() in JAWA_PROVINCES else 'Luar Jawa')
    df_valid['pulau'] = df_valid['provinsi'].apply(get_pulau)

    grand_total_rp = df_valid['investasi_rp_juta'].sum()

    def run_aggregation(groupby_cols, output_filename):
        agg = df_valid.groupby(groupby_cols, dropna=False).agg(
            total_investasi_rp_juta=('investasi_rp_juta', 'sum'),
            total_investasi_us_ribu=('investasi_us_ribu', 'sum'),
            total_tki=('tki', 'sum'),
            row_count=('investasi_rp_juta', 'count')
        ).reset_index()

        agg['percentage_share'] = (agg['total_investasi_rp_juta'] / grand_total_rp) * 100

        agg = agg.sort_values(by='total_investasi_rp_juta', ascending=False)

        current_total = agg['total_investasi_rp_juta'].sum()
        assert abs(current_total - grand_total_rp) < 1, f"Self-check GAGAL di {output_filename}: Total {current_total} != {grand_total_rp}"

        agg.to_csv(f'data/marts/{output_filename}', index=False)
        print(f"Berhasil membuat: {output_filename}")
        return agg

    run_aggregation(['kbli_kode', 'kbli_nama'], 'agg_kbli.csv')

    run_aggregation(['provinsi'], 'agg_provinsi.csv')
    run_aggregation(['pulau'], 'agg_pulau.csv')
    run_aggregation(['is_jawa'], 'agg_jawa_luar_jawa.csv')

    run_aggregation(['kbli_kode', 'provinsi'], 'agg_kbli_provinsi.csv')

    if 'status_penanaman_modal' in df_valid.columns:
        run_aggregation(['kbli_kode', 'status_penanaman_modal'], 'agg_kbli_status.csv')
    else:
        print("Peringatan: Kolom 'status_penanaman_modal' tidak ditemukan, lewati C4.")

if __name__ == "__main__":
    main()