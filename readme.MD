# Proyek Analisis Data: E-Commerce Public Dataset (Olist)

Proyek analisis data pada dataset e-commerce Olist (Brasil) yang mencakup seluruh proses analisis data: mendefinisikan pertanyaan bisnis, data wrangling (gathering, assessing, cleaning), exploratory data analysis (EDA), visualization & explanatory analysis, hingga conclusion & recommendation, serta dashboard interaktif menggunakan Streamlit.

- **Nama:** Radithya Danutirta
- **Email:** ds288b6y1465@student.devacademy.id
- **ID Dicoding:** radithya_danutirta_HKkL
- **Dashboard Streamlit Cloud:** https://g3ioau2pfua9eyqtl7ualq.streamlit.app

## Pertanyaan Bisnis

1. Kategori produk apa saja yang menghasilkan revenue tertinggi dan terendah dari order berstatus *delivered* selama September 2016 – Agustus 2018, dan berapa persen kontribusi 5 kategori teratas terhadap total revenue?
2. Berapa selisih rata-rata review score antara order terlambat dan tepat waktu selama September 2016 – Agustus 2018, dan bagaimana hubungan durasi pengiriman dengan review score?
3. Bagaimana segmentasi pelanggan unik berdasarkan RFM (recency, frequency, monetary) selama September 2016 – Agustus 2018, dan segmen mana yang menyumbang spending terbesar sehingga layak menjadi target retensi?

## Rangkuman Insight per Tahapan

### 1. Gathering Data

- Seluruh 9 tabel dataset (customers, orders, order_items, order_payments, order_reviews, products, sellers, geolocation, product_category_name_translation) berhasil dimuat ke dalam DataFrame.
- `orders_df` mencakup 99.441 order, `order_items_df` 112.650 item transaksi, dan `order_reviews_df` 99.224 ulasan.
- Satu `customer_id` mewakili satu order, sehingga analisis perilaku pelanggan harus memakai `customer_unique_id` (96.096 pelanggan unik).

### 2. Assessing Data

Masalah kualitas data yang teridentifikasi (melebihi minimal 2):

- **Duplicate data:** 261.831 baris duplikat penuh pada `geolocation_dataset`.
- **Inaccurate/inconsistent value:** 8 order berstatus *delivered* tanpa `order_delivered_customer_date` (tidak konsisten) dan 6 order *canceled* yang tanggal sampainya terisi.
- **Invalid value:** 2 baris pembayaran kartu kredit dengan `payment_installments = 0`; 4 produk dengan `product_weight_g = 0`.
- **Missing value:** 610 produk tanpa `product_category_name`; kolom komentar review banyak kosong (wajar).
- **Wrong data type:** seluruh kolom tanggal di `orders_df`, `order_items_df`, dan `order_reviews_df` bertipe `object`, padahal berisi tanggal-waktu.

### 3. Cleaning Data

- Menghapus duplikat `geo_df` dengan `drop_duplicates()`.
- Mengubah seluruh kolom tanggal menjadi `datetime` dengan `pd.to_datetime()`.
- Menghapus 8 order *delivered* tanpa tanggal sampai (0,008% dari order *delivered*).
- Review ganda diringkas menjadi satu baris per `order_id` dengan merata-ratakan `review_score` (547 order terdampak).
- `product_category_name` kosong diisi `"unknown"`, dan kategori tanpa terjemahan diisi dengan nama aslinya agar transaksi tidak hilang dari analisis revenue per kategori.
- Temuan kecil lainnya (mis. `payment_installments = 0`) dibiarkan karena tidak dipakai menjawab pertanyaan bisnis dan jumlahnya sangat kecil.

### 4. Exploratory Data Analysis (EDA)

- Order berstatus *delivered* mencakup 97,02% dari seluruh order, menjadi dasar filter analisis.
- **P1 – Revenue per kategori:** 5 kategori teratas adalah `health_beauty` (BRL 1.233.131,72), `watches_gifts` (BRL 1.165.898,98), `bed_bath_table` (BRL 1.023.434,76), `sports_leisure` (BRL 954.673,55), dan `computers_accessories` (BRL 888.613,62) — total BRL 5.265.752,63 atau **39,83%** dari total revenue. Peringkat revenue tidak selalu sama dengan peringkat volume: `bed_bath_table` memiliki order terbanyak (9.272) tetapi harga rata-ratanya rendah (BRL 93,44).
- **P2 – Keterlambatan & rating:** 8,1% order *delivered* terlambat. Rata-rata rating order terlambat **2,57** vs tepat waktu **4,29** (selisih 1,73 poin). Korelasi `delivery_time` dengan `review_score` sebesar **-0,33**. Rating stabil di 4,41–4,10 untuk pengiriman sampai 21 hari, lalu turun ke 3,49 (22–30 hari) dan anjlok ke 2,18 (>30 hari).
- **P3 – RFM:** 97% pelanggan hanya berbelanja satu kali. Segmen *At Risk (Spender Besar)* berisi 24,7% pelanggan tetapi menyumbang **41,3%** total spending; *Big Spender Baru* menyumbang 39,1%.
- **Analisis lanjutan (geospatial):** State dengan persentase order terlambat tertinggi adalah MA (19,66%) dan CE (15,32%), jauh di atas rata-rata 8,1%.

### 5. Visualization & Explanatory Analysis

Notebook memuat visualisasi untuk setiap pertanyaan bisnis, antara lain: bar chart 5 kategori revenue tertinggi/terendah, perbandingan rating tepat waktu vs terlambat, bar chart rating per kelompok durasi pengiriman, jumlah pelanggan dan spending per segmen RFM, serta persentase order terlambat per state.

### 6. Conclusion & Recommendation

**Kesimpulan:**

1. Lima kategori teratas (`health_beauty`, `watches_gifts`, `bed_bath_table`, `sports_leisure`, `computers_accessories`) menyumbang 39,83% total revenue; lima kategori terendah hanya BRL 3.403,55 (≈0,03%).
2. 8,1% order terlambat dengan selisih rating 1,73 poin (2,57 vs 4,29); durasi pengiriman berkorelasi negatif dengan rating (-0,33) dan rating turun tajam pada pengiriman di atas 21 hari.
3. 97% pelanggan hanya belanja sekali; segmen *At Risk (Spender Besar)* menyimpan 41,3% spending dari 24,7% pelanggan.

**Rekomendasi (action item):**

- Tinjau akurasi estimasi pengiriman dan prioritaskan penanganan pengiriman di atas 21 hari, terutama di state dengan keterlambatan tertinggi (MA dan CE).
- Jalankan kampanye repeat-order (misalnya voucher) untuk segmen *At Risk (Spender Besar)*.
- Pertahankan stok dan promosi pada 5 kategori teratas penyumbang 39,83% revenue.

## Struktur Direktori

```
submission
├── dashboard
│   ├── main_data.csv
│   └── dashboard.py
├── data
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── Radithya_danutirta_Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

- `data/` berisi dataset mentah.
- `Radithya_danutirta_Proyek_Analisis_Data.ipynb` berisi seluruh proses analisis dari wrangling hingga kesimpulan (sudah dijalankan).
- `dashboard/main_data.csv` adalah data hasil olahan (order *delivered*) yang dipakai dashboard.
- `dashboard/dashboard.py` adalah kode dashboard Streamlit.
- `url.txt` berisi tautan dashboard yang sudah dideploy ke Streamlit Cloud.

## Setup dan Menjalankan Dashboard

1. Clone atau unduh repositori ini.
2. (Opsional) Buat virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Linux/macOS
   ```

3. Pasang dependensi:

   ```
   pip install -r requirements.txt
   ```

4. Jalankan dashboard dari folder utama:

   ```
   streamlit run dashboard/dashboard.py
   ```

Dashboard memiliki filter rentang tanggal order di sidebar dan menampilkan empat bagian: ringkasan metrik, revenue per kategori produk, keterlambatan pengiriman vs review score, segmentasi pelanggan RFM, serta analisis lanjutan persentase order terlambat per state.

## Sumber Data

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — tersedia di Kaggle.
