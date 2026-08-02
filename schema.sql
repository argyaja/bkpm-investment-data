CREATE TABLE dim_provinsi (
    id SERIAL PRIMARY KEY,
    nama VARCHAR(100) NOT NULL UNIQUE,
    pulau VARCHAR(50) NOT NULL,
    jawa_luar_jawa VARCHAR(20) NOT NULL
);
CREATE TABLE dim_kbli (
    id SERIAL PRIMARY KEY,
    kbli_kode VARCHAR(10) NOT NULL UNIQUE,
    kbli_nama VARCHAR(255) NOT NULL,
    kbli_versi VARCHAR(4) NOT NULL,
    sektor_utama VARCHAR(100),
    nama_sektor VARCHAR(100)
);
CREATE TABLE dim_negara (
    id SERIAL PRIMARY KEY,
    nama_negara VARCHAR(100) NOT NULL UNIQUE,
    regional VARCHAR(100)
);

CREATE TABLE fakta_investasi (
    id SERIAL PRIMARY KEY,
    periode VARCHAR(50) NOT NULL,
    status_penanaman_modal VARCHAR(10) NOT NULL, 
    kabupaten_kota VARCHAR(100), 
    provinsi_id INT NOT NULL,
    kbli_id INT NOT NULL,
    negara_id INT NOT NULL,
    
    investasi_rp_juta DECIMAL(18, 4) NOT NULL,
    investasi_us_ribu DECIMAL(18, 4) NOT NULL,
    tki INT NOT NULL,
    is_suspect BOOLEAN NOT NULL DEFAULT FALSE,

    -- Foreign Keys
    CONSTRAINT fk_provinsi FOREIGN KEY (provinsi_id) REFERENCES dim_provinsi(id),
    CONSTRAINT fk_kbli FOREIGN KEY (kbli_id) REFERENCES dim_kbli(id),
    CONSTRAINT fk_negara FOREIGN KEY (negara_id) REFERENCES dim_negara(id)
);