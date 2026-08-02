import requests
import urllib.parse
import json
import time
import random
import os

API_URL = "https://data.bkpm.go.id/data"
RAW_QUERY_STRING = "draw=1&columns%5B0%5D%5Bdata%5D=function&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=function&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=function&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=function&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=function&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=function&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=function&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=function&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=function&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=function&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=function&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=function&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=function&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=function&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&dataset_detail_parent_id=15605157-8247-4bef-b387-0b23719fe976"
OUTPUT_FILE = "/content/drive/MyDrive/katadata_test/investasi_raw.jsonl"
PAGE_LENGTH = 100  

def scrape_data():
  print("Memulai proses scraping...")

  base_params = dict(
    urllib.parse.parse_qsl(
        RAW_QUERY_STRING,
        keep_blank_values=True
    )
)

  session = requests.Session()

  session.headers.update({
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'application/json, text/javascript, */*; q=0.01'
  })

  downloaded_count = 0
  if os.path.exists(OUTPUT_FILE):
      with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
          downloaded_count = sum(1 for _ in f)
      print(f"Ditemukan file cache! Sudah ada {downloaded_count} baris data di Google Drive.")
  else:
      print("Tidak ada file cache. Memulai unduhan dari awal.")

  current_start = downloaded_count
  total_records = None

  request_count = 0

  while True:
      # Menyiapkan parameter untuk halaman saat ini
      current_params = base_params.copy()
      current_params['start'] = current_start
      current_params['length'] = PAGE_LENGTH

      print(f"Mengambil data mulai dari indeks {current_start}...")

      try:
          response = session.get(API_URL, params=current_params)
          response.raise_for_status() 

          data_json = response.json()

          if total_records is None:
              total_records = data_json.get('recordsTotal', 0)
              print(f"Total data di server BKPM: {total_records} baris")

              if current_start >= total_records:
                  print("Semua data sudah lengkap terunduh. Scraping dihentikan.")
                  break

          records = data_json.get('data', [])

          if not records:
              print("Tidak ada data lagi yang diterima dari server. Selesai.")
              break

          with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
              for row in records:
                  f.write(json.dumps(row) + '\n')

          print(f"Berhasil menyimpan {len(records)} baris data.")

          current_start += len(records)

          if current_start >= total_records:
              print("Seluruh data berhasil diunduh!")
              break

          request_count += 1
          if request_count % 50 == 0:
              print(f"[{request_count} Request] Istirahat 30 detik untuk mendinginkan koneksi...")
              time.sleep(30)
          else:
              delay = random.uniform(2.0, 4.0)
              print(f"Jeda acak selama {delay:.2f} detik...")
              time.sleep(delay)

      except Exception as e:
          print(f"Terjadi kesalahan saat mengambil data: {e}")
          print("Skrip dihentikan. Kamu bisa menjalankan ulang nanti tanpa mengulang dari awal.")
          break

if __name__ == "__main__":
    scrape_data()