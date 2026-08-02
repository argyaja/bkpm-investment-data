# Data Quality Report

## 1. Row Counts
- **Rows In (Raw):** 33641
- **Rows Out (Clean):** 33641
- **Difference:** 0

## 2. Null Count & Percentage
|                        |   Null Count |   Percentage (%) |
|:-----------------------|-------------:|-----------------:|
| periode                |            0 |                0 |
| status_penanaman_modal |            0 |                0 |
| regional               |            0 |                0 |
| negara                 |            0 |                0 |
| sektor_utama           |            0 |                0 |
| nama_sektor            |            0 |                0 |
| deskripsi_kbli_2digit  |            0 |                0 |
| provinsi               |            0 |                0 |
| kabupaten_kota         |            0 |                0 |
| jawa_luar_jawa         |            0 |                0 |
| pulau                  |            0 |                0 |
| investasi_rp_juta      |            0 |                0 |
| investasi_us_ribu      |            0 |                0 |
| tki                    |            0 |                0 |
| kbli_kode              |            0 |                0 |
| kbli_versi             |            0 |                0 |
| kbli_nama              |            0 |                0 |
| is_suspect             |            0 |                0 |

## 3. Numeric Statistics
|                   |   min |            max |       mean |    median |              sum |
|:------------------|------:|---------------:|-----------:|----------:|-----------------:|
| investasi_rp_juta |     0 |    2.55605e+07 | 15213.1    | 14.5      |      5.11784e+08 |
| investasi_us_ribu |     0 |    1.54912e+06 |   922.007  |  0.878788 |      3.10172e+07 |
| tki               |     0 | 5987           |    22.0651 |  0        | 742293           |

## 4. Distinct Value Counts
- **provinsi**: 38 distinct values
- **kabupaten_kota**: 511 distinct values
- **nama_sektor**: 23 distinct values
- **negara**: 161 distinct values

## 5. Suspect Rows Analysis
Total suspect rows: 14136

| provinsi                      |   investasi_rp_juta |   investasi_us_ribu | reason                            |
|:------------------------------|--------------------:|--------------------:|:----------------------------------|
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Jawa Timur                    |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Nusa Tenggara Barat           |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Daerah Khusus Ibukota Jakarta |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Nusa Tenggara Barat           |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Daerah Khusus Ibukota Jakarta |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Daerah Khusus Ibukota Jakarta |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Sumatera Barat                |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Nusa Tenggara Barat           |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Jawa Timur                    |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Nusa Tenggara Barat           |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Daerah Khusus Ibukota Jakarta |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Bali                          |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Nusa Tenggara Barat           |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Nusa Tenggara Barat           |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Nusa Tenggara Barat           |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Daerah Khusus Ibukota Jakarta |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Daerah Khusus Ibukota Jakarta |                   0 |                   0 | Investasi Rp dan USD keduanya nol |
| Nusa Tenggara Barat           |                   0 |                   0 | Investasi Rp dan USD keduanya nol |

*(Menampilkan maksimal 50 baris pertama)*

## 6. Grand Total Reconciliation
- **Calculated Total:** Rp 511.78 Triliun
- **Published BKPM Figure:** Rp 511.8 Triliun
