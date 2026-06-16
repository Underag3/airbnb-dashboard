# Airbnb Data Dashboard - New York City 2019

Repositori ini berisi aplikasi dashboard interaktif yang dibangun menggunakan **Python** dan **Streamlit** untuk menganalisis dan memvisualisasikan data listing Airbnb di New York City sepanjang tahun 2019. 

Dashboard ini dirancang untuk memberikan wawasan mendalam mengenai tren harga, distribusi geografis, preferensi tipe kamar, serta aktivitas review di berbagai wilayah (borough) di NYC.

---

## 🚀 Fitur Utama
* **Ringkasan KPI Utama:** Menampilkan metrik penting seperti total listing, rata-rata harga, dan total ulasan secara *real-time*.
* **Analisis Geografis:** Visualisasi interaktif sebaran akomodasi berdasarkan kelompok wilayah (`neighbourhood_group`).
* **Tren Harga & Kamar:** Analisis perbandingan harga berdasarkan tipe kamar (`room_type`) dan wilayah.
* **Filter Interaktif:** Memudahkan pengguna untuk menyaring data berdasarkan wilayah, rentang harga, atau ketersediaan kamar.

---

## 📂 Struktur Repositori
* `.devcontainer/` : Konfigurasi lingkungan pengembangan (Dev Container) untuk konsistensi *environment*.
* `AB_NYC_2019.csv` : Dataset mentah Airbnb New York City tahun 2019.
* `dashboard_airbnb.py` : Skrip utama aplikasi dashboard berbasis Streamlit.
* `requirements.txt` : Daftar pustaka (dependencies) Python yang dibutuhkan untuk menjalankan proyek ini.

---

## 🛠️ Cara Menjalankan Proyek secara Lokal

### 1. Prasyarat
Pastikan Anda sudah menginstal **Python 3.8+** di komputer Anda.

### 2. Kloning Repositori
```bash
git clone [https://github.com/Underag3/airbnb-dashboard.git](https://github.com/Underag3/airbnb-dashboard.git)
cd airbnb-dashboard

```
3. Buat Virtual Environment (Opsional tetapi Direkomendasikan)
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
4. Instal Dependencies
Instal semua pustaka Python yang diperlukan dengan menjalankan perintah:

Bash
pip install -r requirements.txt
5. Jalankan Dashboard
Setelah proses instalasi selesai, luncurkan aplikasi Streamlit menggunakan perintah berikut:

Bash
streamlit run dashboard_airbnb.py
Aplikasi otomatis akan terbuka di peramban (browser) Anda, biasanya pada alamat http://localhost:8501.

📊 Dataset
Dataset yang digunakan dalam proyek ini berasal dari data publik Airbnb New York City tahun 2019 (AB_NYC_2019.csv). Atribut utama yang dianalisis meliputi:

id & name: Identifikasi listing

neighbourhood_group & neighbourhood: Lokasi wilayah dan lingkungan sekitar

room_type: Tipe akomodasi (Private room, Entire home/apt, Shared room)

price: Harga per malam

minimum_nights: Batas minimum menginap

number_of_reviews: Jumlah ulasan yang diterima

👤 Kontributor
Mohammad Tyas Subianto
