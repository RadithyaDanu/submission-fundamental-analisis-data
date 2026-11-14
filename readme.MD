# Proyek Analisis Data: E-Commerce (Olist)

Proyek analisis data untuk dataset e-commerce Olist (Brasil), mencakup proses data wrangling, exploratory data analysis (EDA), visualisasi, dan dashboard interaktif menggunakan Streamlit.

- **Nama:** Radithya Danutirta
- **Email:** ds288b6y1465@student.devacademy.id
- **ID Dicoding:** radithya_danutirta_HKkL
- **Dashboard:** https://g3ioau2pfua9eyqtl7ualq.streamlit.app

## Pertanyaan Bisnis

1. Kategori produk apa yang menghasilkan revenue tertinggi dan terendah dari order berstatus _delivered_ selama September 2016 – Agustus 2018, dan berapa persen kontribusi 5 kategori teratas terhadap total revenue?
2. Berapa selisih rata-rata review score antara order yang terlambat dan yang tepat waktu selama September 2016 – Agustus 2018, dan seberapa kuat korelasi durasi pengiriman (`delivery_time`) dengan review score?
3. Bagaimana segmentasi pelanggan unik berdasarkan RFM (recency, frequency, monetary) selama September 2016 – Agustus 2018, dan segmen mana yang menyumbang spending terbesar sehingga layak menjadi target retensi?

## Ringkasan Temuan

- **Revenue:** `health_beauty`, `watches_gifts`, dan `bed_bath_table` adalah tiga kategori dengan revenue tertinggi. Lima kategori teratas menyumbang 39,8% dari total revenue.
- **Pengiriman:** Order terlambat memiliki rata-rata rating 2,57, sedangkan order tepat waktu 4,29. Korelasi `delivery_time` dengan `review_score` sebesar -0,33.
- **Pelanggan:** Hanya 3,0% pelanggan yang melakukan pembelian ulang. Segmen _At Risk_ dan _Big Spender Baru_ menyumbang sekitar 80% total spending.

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
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

- `data/` berisi dataset mentah.
- `notebook.ipynb` berisi seluruh proses analisis, dari wrangling hingga kesimpulan.
- `dashboard/main_data.csv` adalah data hasil olahan (order _delivered_) yang dipakai dashboard.
- `url.txt` berisi tautan dashboard yang sudah dideploy.

## Setup dan Menjalankan Dashboard

1. Clone atau unduh repositori ini.
2. Buat virtual environment (opsional), lalu pasang dependensi:

   ```
   pip install -r requirements.txt
   ```

3. Jalankan dashboard dari folder `submission`:

   ```
   streamlit run dashboard/dashboard.py
   ```

Dashboard memiliki filter rentang tanggal di sidebar dan menampilkan tiga bagian analisis sesuai pertanyaan bisnis di atas.

## Sumber Data

Brazilian E-Commerce Public Dataset by Olist (tersedia di Kaggle).
