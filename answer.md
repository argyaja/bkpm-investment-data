### Answer

* **How is the data table actually loaded?**

  * Data tabel dimuat secara dinamis melalui request **AJAX/XHR** ke endpoint yang mengembalikan data dalam format **JSON**.

* **Is it present in the HTML that `requests.get()` returns, or does it arrive some other way?**

  * Tidak. HTML hasil `requests.get()` hanya berisi struktur halaman dan kerangka tabel. Data tabel tidak berada di dalam HTML, tetapi diperoleh dari respons JSON yang diminta setelah halaman dimuat.

* **Evidence**

  * `View Page Source` tidak menampilkan isi data tabel.
  * Pada **Developer Tools → Network → XHR/Fetch** terlihat request menuju endpoint data.
  * Respons request berupa **JSON** yang berisi record tabel.
  * Parameter seperti `draw`, `start`, dan `length` menunjukkan penggunaan **server-side processing**, di mana data diambil sesuai kebutuhan halaman.


## Etika dan Teknis Scraping

Berdasarkan pengamatan saya, website tersebut secara teknis berfungsi sebagai portal penyedia data yang menampilkan informasi kepada pengguna melalui halaman web. Data yang terlihat pada halaman kemungkinan tidak seluruhnya ditulis langsung pada HTML, tetapi dimuat melalui proses komunikasi antara browser dan server. Ketika pengguna membuka halaman, browser mengirimkan permintaan ke server, kemudian server mengirimkan data yang diperlukan untuk ditampilkan. Adanya formulir sebelum mengakses dataset dapat memiliki beberapa tujuan, seperti mengetahui profil pengguna, mencatat jumlah pengguna data, mengirimkan informasi terbaru, atau memahami bagaimana dataset tersebut digunakan oleh masyarakat.

Menurut saya, penggunaan endpoint JSON yang ditemukan tanpa melalui formulir masih dapat diterima dalam kondisi tertentu. Hal ini karena data tersebut berstatus publik dan menggunakan lisensi CC-BY 4.0 yang memberikan izin kepada pengguna untuk menggunakan data dengan tetap memberikan atribusi kepada pemilik data. Selain itu, endpoint tersebut tidak membutuhkan login, kredensial, atau cara khusus untuk melewati sistem keamanan. Namun, saya tetap mempertimbangkan tujuan dari publisher yang membuat formulir tersebut. Walaupun secara teknis endpoint dapat digunakan langsung, pengguna sebaiknya tetap menghargai mekanisme yang dibuat oleh penyedia data. Jika penggunaan endpoint dilakukan hanya untuk mengambil data secara efisien dan tetap mengikuti aturan penggunaan data, menurut saya hal tersebut masih dapat dibenarkan.

Dalam proses scraping, terdapat batasan tertentu ketika saya harus berhenti dan meminta arahan dari manusia. Salah satu contoh adalah jika website menambahkan sistem CAPTCHA sebagai kontrol untuk memastikan bahwa akses dilakukan oleh manusia. CAPTCHA menunjukkan bahwa publisher secara sengaja membatasi otomatisasi. Selain itu, jika terdapat autentikasi khusus, pembatasan akses berdasarkan izin pengguna, atau aturan penggunaan yang secara jelas melarang scraping, saya tidak akan mencoba melewati kontrol tersebut karena keputusan tersebut sudah masuk ke ranah kebijakan dan tanggung jawab organisasi.

Apabila portal menambahkan beberapa hambatan teknis, saya akan menyelesaikannya berdasarkan urutan dari solusi yang paling sederhana terlebih dahulu. Jika mendapatkan error 403 karena User-Agent tidak sesuai, langkah pertama yang saya lakukan adalah menambahkan User-Agent seperti browser normal pada request. Jika terdapat batas 30 request per menit dengan respons 429, saya akan menerapkan rate limiting dan memberikan jeda antar request agar sesuai dengan kapasitas server. Jika terdapat rotating CSRF token, saya akan mengikuti alur normal website dengan mengambil token terbaru sebelum melakukan request berikutnya. Terakhir, jika muncul CAPTCHA, saya akan menghentikan otomatisasi dan melakukan eskalasi kepada manusia karena CAPTCHA bukan masalah teknis biasa, tetapi merupakan kontrol keamanan yang sengaja dibuat oleh pemilik website.

Menurut saya, developer tidak boleh mengambil keputusan sendiri untuk melewati CAPTCHA, menggunakan teknik bypass keamanan, mengabaikan batas akses, atau melakukan scraping terhadap data yang memiliki pembatasan khusus tanpa persetujuan. Keputusan tersebut harus melibatkan pemilik data atau pihak yang bertanggung jawab agar proses pengambilan data tetap sesuai dengan aturan dan etika yang berlaku.