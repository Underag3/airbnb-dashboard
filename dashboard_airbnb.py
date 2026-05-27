import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Laporan Analitik Airbnb NYC",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PREMIUM & KONSISTEN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

    /* Global Font & Background */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
        color: #334155;
    }

    .stApp {
        background-color: #f8fafc;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
        padding-top: 1rem;
    }
    
    /* Custom Styling for Radio Buttons in Sidebar */
    .stRadio > div {
        gap: 15px;
    }

    /* Card Metrics Premium */
    .kpi-wrapper {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border-top: 3px solid #1e3c72;
        border-bottom: 1px solid #e2e8f0;
        border-left: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1.5rem;
    }
    .kpi-wrapper:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
        border-color: #cbd5e1;
    }
    .kpi-title {
        color: #64748b;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        color: #1e3c72;
        font-size: 2.2rem;
        font-family: 'Playfair Display', serif;
        font-weight: 600;
    }

    /* Section Headers */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #1e3c72 !important;
        font-size: 2.4rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 1.5rem !important;
    }
    h2 {
        font-family: 'Playfair Display', serif !important;
        color: #1e3c72 !important;
        font-size: 1.6rem !important;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 0.5rem;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    h3, h4 {
        color: #334155 !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }

    /* Data Insight Boxes */
    .insight-box {
        background-color: #ffffff;
        border-left: 4px solid #2a5298;
        padding: 1.5rem;
        border-radius: 0 6px 6px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        margin: 1rem 0 2rem 0;
        line-height: 1.6;
        color: #475569;
        font-size: 0.95rem;
    }
    .insight-box strong {
        color: #1e3c72;
        font-family: 'Inter', sans-serif;
    }

    /* Filter Container */
    .control-panel {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }

    /* Sidebar Footer */
    .sidebar-footer {
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# --- PENGELOLAAN DATA ---
@st.cache_data
def muat_dan_bersihkan_data():
    path = "AB_NYC_2019.csv"
    try:
        data = pd.read_csv(path)
        if 'reviews_per_month' in data.columns:
            data['reviews_per_month'] = data['reviews_per_month'].fillna(0)
        
        data['host_segment'] = np.where(data['calculated_host_listings_count'] > 1, 'Host Profesional (Multi)', 'Host Individu (Single)')
        data = data[data['price'] > 0]

        # Memastikan kolom teks bersih untuk tooltip
        if 'name' in data.columns:
            data['name'] = data['name'].fillna("Tanpa Nama")
        if 'host_name' in data.columns:
            data['host_name'] = data['host_name'].fillna("Tanpa Nama")

        # Palet Warna Harmonik
        palet_warna = {
            'Entire home/apt': '#1e3c72', # Deep Corporate Blue
            'Private room': '#5499c7',    # Mid Cerulean
            'Shared room': '#94a3b8'      # Slate Gray
        }
        return data, palet_warna
    except Exception as e:
        return None, None

df_raw, WARNA_KAMAR = muat_dan_bersihkan_data()

if df_raw is None:
    st.error("Kritis: Dataset 'AB_NYC_2019.csv' tidak ditemukan di direktori saat ini.")
    st.stop()

def terapkan_tema_grafik(fig):
    fig.update_layout(
        font_family="Inter",
        font_color="#475569",
        title_font_family="Playfair Display",
        title_font_size=16,
        title_font_color="#1e3c72",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=None),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Inter")
    )
    fig.update_xaxes(showgrid=False, linecolor='#e2e8f0', tickfont=dict(color='#64748b'))
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', linecolor='#e2e8f0', tickfont=dict(color='#64748b'))
    return fig

# --- SIDEBAR: NAVIGASI & IDENTITAS ---
with st.sidebar:
    st.markdown("""
        <div style='font-family: "Playfair Display", serif; font-size: 1.6rem; color: #1e3c72; font-weight: 600; line-height: 1.3; margin-bottom: 2rem;'>
            Laporan Analitik<br>Airbnb NYC
        </div>
    """, unsafe_allow_html=True)
    
    menu_aktif = st.radio(
        "Navigasi Laporan",
        [
            "Ringkasan Eksekutif", 
            "Analisis Eksploratif (EDA)", 
            "Wawasan Pemodelan", 
            "Metrik Performa"
        ]
    )
    
    st.markdown("""
        <div class="sidebar-footer">
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.8rem;">Disusun Oleh</div>
            <div style="font-size: 0.9rem; color: #334155; font-weight: 600; line-height: 1.6;">
                Kevin Febrian Widhiarta<br>
                Mohammad Tyas Subianto<br>
                Daris Ikhwana Khoir Suhaya
            </div>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 1rem; font-style: italic;">
                Penelitian Exploratory Data Analysis & Modeling<br>
                Mei 2026
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 1. HALAMAN: RINGKASAN EKSEKUTIF
# ==========================================
if menu_aktif == "Ringkasan Eksekutif":
    
    st.markdown("<h1>Ringkasan Eksekutif</h1>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='font-size: 1.05rem; color: #475569; line-height: 1.7; margin-bottom: 2rem; text-align: justify;'>
            Laporan ini menyajikan hasil analisis mendalam terhadap lanskap pasar penyewaan Airbnb di New York City pada tahun 2019. 
            Melalui pendekatan analitik deskriptif dan pemodelan prediktif menggunakan <strong>Regresi Logistik Multinomial (MLR)</strong> serta 
            <strong>Analisis Diskriminan Linier (LDA)</strong>, penelitian ini bertujuan untuk membongkar faktor-faktor pendorong 
            segmentasi properti—mulai dari strategi penetapan harga, distribusi geospasial, hingga profesionalisasi manajemen tuan rumah.
        </div>
    """, unsafe_allow_html=True)
    
    # Metrik Eksekutif
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-wrapper"><div class="kpi-title">Total Inventaris</div><div class="kpi-value">{len(df_raw):,}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-wrapper"><div class="kpi-title">Rata-rata Harga Pasar</div><div class="kpi-value">${df_raw["price"].mean():.0f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-wrapper"><div class="kpi-title">Akurasi Baseline Model</div><div class="kpi-value">82.9%</div></div>', unsafe_allow_html=True)
    with c4:
        persentase_pro = (df_raw['host_segment'] == 'Host Profesional (Multi)').mean() * 100
        st.markdown(f'<div class="kpi-wrapper"><div class="kpi-title">Penetrasi Host Profesional</div><div class="kpi-value">{persentase_pro:.0f}%</div></div>', unsafe_allow_html=True)

    st.markdown("<h2>Temuan Strategis Utama</h2>", unsafe_allow_html=True)
    
    col_insight1, col_insight2 = st.columns(2)
    with col_insight1:
        st.markdown("""
        <div class="insight-box">
            <strong>1. Privasi sebagai Komoditas Premium</strong><br><br>
            Harga terbukti menjadi determinan terkuat dalam klasifikasi tipe kamar. Properti jenis <i>'Entire home/apt'</i> 
            memiliki harga premium yang signifikan, memvalidasi kecenderungan pasar yang bersedia membayar lebih 
            untuk mendapatkan privasi absolut. Sebaliknya, <i>Shared room</i> tetap berada pada segmen pasar yang sangat <i>niche</i> dan berbiaya rendah.
        </div>
        """, unsafe_allow_html=True)
        
    with col_insight2:
        st.markdown("""
        <div class="insight-box">
            <strong>2. Keunggulan Algoritma pada Data Imbalance</strong><br><br>
            Meskipun metode MLR dan LDA menunjukkan tingkat akurasi menyeluruh yang hampir identik (~82.9%), 
            <strong>Analisis Diskriminan Linier (LDA)</strong> menunjukkan ketahanan yang lebih baik. LDA menghasilkan metrik <i>Macro F1-Score</i> 
            yang lebih tinggi, menandakan kemampuannya yang lebih stabil dalam menangani ketidakseimbangan kelas ekstrem pada kategori <i>Shared room</i>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2>Tinjauan Struktur Dataset</h2>", unsafe_allow_html=True)
    st.dataframe(df_raw.head(8), use_container_width=True)

# ==========================================
# 2. HALAMAN: ANALISIS EKSPLORATIF (EDA)
# ==========================================
elif menu_aktif == "Analisis Eksploratif (EDA)":
    
    st.markdown("<h1>Analisis Eksploratif (EDA)</h1>", unsafe_allow_html=True)
    
    # Panel Kendali (Filter)
    st.markdown("<div style='padding: 1rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 2rem;'><span style='font-size: 1.1rem; font-weight: 600; color: #1e3c72; text-transform: uppercase; letter-spacing: 1px;'>⚙️ Filter Parameter Analisis</span></div>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns([1.5, 2, 1.5])
    with f1:
        pilihan_wilayah = st.selectbox("Fokus Geografis (Wilayah):", ["Seluruh Wilayah NYC"] + list(df_raw['neighbourhood_group'].unique()))
    with f2:
        batas_harga = st.slider("Batasan Analisis Harga ($):", int(df_raw['price'].min()), 1500, (0, 600))
    with f3:
        pilihan_host = st.multiselect("Segmen Operator (Host):", df_raw['host_segment'].unique(), default=list(df_raw['host_segment'].unique()))
    st.markdown("<br>", unsafe_allow_html=True)

    # Memproses Data Sesuai Filter
    df_f = df_raw[(df_raw['price'].between(batas_harga[0], batas_harga[1])) & (df_raw['host_segment'].isin(pilihan_host))]
    if pilihan_wilayah != "Seluruh Wilayah NYC":
        df_f = df_f[df_f['neighbourhood_group'] == pilihan_wilayah]

    # --- SUB-BAGIAN 1: KOMPOSISI PASAR ---
    st.markdown("<h2>1. Komposisi & Konsentrasi Pasar</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Segmentasi Inventaris Properti")
        # Tooltip interaktif kaya
        fig_pie = px.pie(df_f, names='room_type', hole=0.65, color='room_type', color_discrete_map=WARNA_KAMAR)
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Jumlah: %{value:,.0f} Properti<br>Pangsa Pasar: %{percent}<extra></extra>"
        )
        st.plotly_chart(terapkan_tema_grafik(fig_pie), use_container_width=True)
    
    with c2:
        st.markdown("#### Kepadatan Geografis antar Wilayah")
        fig_hist = px.histogram(
            df_f, x='neighbourhood_group', color='room_type', barmode='stack', color_discrete_map=WARNA_KAMAR,
            labels={"neighbourhood_group": "Wilayah Geografis", "room_type": "Tipe Properti"}
        )
        fig_hist.update_xaxes(title_text="Wilayah")
        fig_hist.update_yaxes(title_text="Jumlah Listing")
        fig_hist.update_traces(hovertemplate="<b>Wilayah:</b> %{x}<br><b>Jumlah:</b> %{y:,.0f} Listing<extra></extra>")
        st.plotly_chart(terapkan_tema_grafik(fig_hist), use_container_width=True)

    # --- SUB-BAGIAN 2: DINAMIKA HARGA ---
    st.markdown("<h2>2. Dinamika Harga & Spesifikasi Properti</h2>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### Rentang Harga Berdasarkan Tipe Kamar")
        fig_violin = px.violin(
            df_f, x='room_type', y='price', color='room_type', box=True, points="outliers", color_discrete_map=WARNA_KAMAR,
            hover_data=['neighbourhood', 'host_name']
        )
        fig_violin.update_xaxes(title_text="Tipe Kamar")
        fig_violin.update_yaxes(title_text="Harga Per Malam ($)")
        st.plotly_chart(terapkan_tema_grafik(fig_violin), use_container_width=True)
    
    with c4:
        st.markdown("#### Strategi Penawaran Berdasarkan Tipe Host")
        fig_bar = px.histogram(df_f, x="host_segment", color="room_type", barmode='group', barnorm='percent', color_discrete_map=WARNA_KAMAR)
        fig_bar.update_xaxes(title_text="Segmen Host")
        fig_bar.update_yaxes(title_text="Persentase Penawaran (%)")
        fig_bar.update_traces(hovertemplate="<b>Segmen Host:</b> %{x}<br><b>Persentase:</b> %{y:.1f}%<extra></extra>")
        st.plotly_chart(terapkan_tema_grafik(fig_bar), use_container_width=True)

    # --- SUB-BAGIAN 3: KORELASI & POLA PERILAKU ---
    st.markdown("<h2>3. Hubungan Interaktif: Popularitas, Harga, dan Ketersediaan</h2>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        st.markdown("#### Harga vs Popularitas (Total Ulasan)")
        fig_scatter = px.scatter(
            df_f, x='price', y='number_of_reviews', color='room_type', 
            opacity=0.6, color_discrete_map=WARNA_KAMAR,
            hover_name='name',
            hover_data={
                'neighbourhood': True,
                'price': ':.0f',
                'number_of_reviews': True,
                'room_type': False
            },
            labels={"price": "Harga ($)", "number_of_reviews": "Jumlah Ulasan", "neighbourhood": "Kawasan"}
        )
        fig_scatter.update_xaxes(title_text="Harga Per Malam ($)")
        fig_scatter.update_yaxes(title_text="Total Ulasan")
        st.plotly_chart(terapkan_tema_grafik(fig_scatter), use_container_width=True)
        st.markdown("<div class='insight-box'><strong>Insight Eksekutif:</strong> Properti dengan harga premium memiliki intensitas ulasan yang rendah. Ini mengonfirmasi bahwa segmen mewah memiliki frekuensi pemesanan yang jauh lebih jarang dibandingkan properti ekonomi. <i>(Hover pada titik untuk melihat detail properti)</i></div>", unsafe_allow_html=True)

    with c6:
        st.markdown("#### Distribusi Minimum Menginap (Durasi Sewa)")
        df_nights = df_f[df_f['minimum_nights'] <= 30] 
        fig_hist_nights = px.histogram(
            df_nights, x='minimum_nights', color='room_type', barmode='overlay', color_discrete_map=WARNA_KAMAR, nbins=30
        )
        fig_hist_nights.update_xaxes(title_text="Minimum Menginap (Malam)")
        fig_hist_nights.update_yaxes(title_text="Jumlah Properti")
        fig_hist_nights.update_traces(hovertemplate="<b>Durasi Min:</b> %{x} Malam<br><b>Jumlah:</b> %{y} Properti<extra></extra>")
        st.plotly_chart(terapkan_tema_grafik(fig_hist_nights), use_container_width=True)
        st.markdown("<div class='insight-box'><strong>Insight Eksekutif:</strong> Lonjakan tertinggi berada pada angka 1 hingga 3 malam. Namun, anomali pada angka 30 malam mengindikasikan banyaknya properti yang digunakan untuk penyewaan jangka panjang.</div>", unsafe_allow_html=True)

    # --- SUB-BAGIAN 4: WAWASAN AREA SPESIFIK ---
    st.markdown("<h2>4. Peringkat Sub-Wilayah (Neighbourhood) Teratas</h2>", unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        st.markdown("#### 10 Kawasan Termahal (Rata-rata Harga)")
        top_expensive = df_f.groupby('neighbourhood')['price'].mean().sort_values(ascending=False).head(10).reset_index()
        fig_bar_price = px.bar(
            top_expensive, x='price', y='neighbourhood', orientation='h', color_discrete_sequence=['#1e3c72'],
            text=top_expensive['price'].apply(lambda x: f"${x:.0f}")
        )
        fig_bar_price.update_traces(textposition='outside', hovertemplate="<b>Kawasan:</b> %{y}<br><b>Rata-rata Harga:</b> $%{x:,.2f}<extra></extra>")
        fig_bar_price.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_bar_price.update_xaxes(title_text="Rata-rata Harga ($)")
        fig_bar_price.update_yaxes(title_text="")
        st.plotly_chart(terapkan_tema_grafik(fig_bar_price), use_container_width=True)

    with c8:
        st.markdown("#### 10 Kawasan Terpopuler (Total Ulasan)")
        top_popular = df_f.groupby('neighbourhood')['number_of_reviews'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar_pop = px.bar(
            top_popular, x='number_of_reviews', y='neighbourhood', orientation='h', color_discrete_sequence=['#5499c7'],
            text=top_popular['number_of_reviews'].apply(lambda x: f"{x:,}")
        )
        fig_bar_pop.update_traces(textposition='outside', hovertemplate="<b>Kawasan:</b> %{y}<br><b>Total Ulasan:</b> %{x:,.0f}<extra></extra>")
        fig_bar_pop.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_bar_pop.update_xaxes(title_text="Total Ulasan Terakumulasi")
        fig_bar_pop.update_yaxes(title_text="")
        st.plotly_chart(terapkan_tema_grafik(fig_bar_pop), use_container_width=True)

    # --- SUB-BAGIAN 5: PETA GEOSPASIAL INTERAKTIF ---
    st.markdown("<h2>5. Peta Kepadatan Geospasial (Interaktif Lanjut)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; margin-bottom: 1.5rem;'>Navigasi Peta: Gunakan kursor untuk melihat nama properti, harga, dan kawasan di setiap titik. <strong>Peta ini ditenagai oleh Mapbox</strong>, memungkinkan proses zoom tanpa mengurangi resolusi informasi spasial.</p>", unsafe_allow_html=True)
    
    df_map = df_f.sample(n=min(3000, len(df_f)), random_state=42) 
    fig_map = px.scatter_mapbox(
        df_map, 
        lat="latitude", 
        lon="longitude", 
        color="room_type", 
        size="price",
        color_discrete_map=WARNA_KAMAR, 
        mapbox_style="carto-positron", 
        zoom=10, 
        hover_name="name", 
        hover_data={
            "latitude": False, 
            "longitude": False, 
            "neighbourhood": True,
            "room_type": True, 
            "price": ":$.0f",
            "host_name": True
        },
        labels={"neighbourhood": "Kawasan", "room_type": "Kategori", "price": "Harga/Malam", "host_name": "Tuan Rumah"}
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=600, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=None))
    st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# 3. HALAMAN: WAWASAN PEMODELAN
# ==========================================
elif menu_aktif == "Wawasan Pemodelan":
    st.markdown("<h1>Wawasan Pemodelan Statistik</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='font-size: 1.05rem; color: #475569; margin-bottom: 2rem;'>
            Bagian ini membedah parameter statistik yang dihasilkan oleh model klasifikasi kami. 
            Kategori <strong>Entire home/apt</strong> digunakan sebagai referensi dasar (<i>baseline</i>) untuk mengukur pengaruh setiap variabel.
        </div>
    """, unsafe_allow_html=True)
    
    # Data Koefisien dari Laporan Asli
    data_koefisien = pd.DataFrame({
        'Fitur Analisis': ['(Konstanta/Intercept)', 'Log Harga (Price)', 'Ketersediaan (Availability)', 'Jumlah Ulasan (Reviews)'],
        'Kamar_Pribadi': [-0.6015, -2.5327, 0.3740, -0.1029],
        'Kamar_Berbagi': [-5.0427, -3.9213, 0.7574, -0.4038]
    })

    st.markdown("<div style='padding: 1rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.5rem;'><span style='font-size: 1.1rem; font-weight: 600; color: #1e3c72; text-transform: uppercase; letter-spacing: 1px;'>⚙️ Konfigurasi Target Analisis</span></div>", unsafe_allow_html=True)
    target_analisis = st.selectbox("Pilih Kelas Target untuk Dibandingkan (vs Entire Home):", ["Kamar Pribadi (Private Room)", "Kamar Berbagi (Shared Room)"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    kolom_target = 'Kamar_Pribadi' if "Pribadi" in target_analisis else 'Kamar_Berbagi'
    
    col_tabel, col_grafik = st.columns([1, 1.8])
    with col_tabel:
        st.markdown(f"#### Nilai Estimasi Koefisien")
        st.dataframe(data_koefisien[['Fitur Analisis', kolom_target]], use_container_width=True, hide_index=True)
        
    with col_grafik:
        st.markdown("#### Besaran dan Arah Pengaruh (Visualisasi)")
        fig_koef = px.bar(
            data_koefisien, x=kolom_target, y='Fitur Analisis', orientation='h', color=kolom_target, color_continuous_scale='Tealrose',
            text=data_koefisien[kolom_target].apply(lambda x: f"{x:.4f}")
        )
        fig_koef.add_vline(x=0, line_dash="solid", line_color="#94a3b8", line_width=2)
        fig_koef.update_traces(textposition='auto', hovertemplate="<b>Fitur:</b> %{y}<br><b>Koefisien:</b> %{x:,.4f}<extra></extra>")
        fig_koef.update_layout(coloraxis_showscale=False)
        st.plotly_chart(terapkan_tema_grafik(fig_koef), use_container_width=True)

    nilai_harga = data_koefisien.loc[1, kolom_target]
    st.markdown(f"""
    <div class='insight-box'>
        <strong>Sintesis Statistik:</strong><br><br>
        Keberadaan koefisien negatif yang sangat kuat pada variabel <i>Log Harga</i> ({nilai_harga}) mengonfirmasi secara matematis 
        bahwa semakin tinggi harga suatu aset properti, semakin mustahil properti tersebut masuk ke dalam kategori {target_analisis}. 
        Sebaliknya, nilai positif pada koefisien <i>Ketersediaan</i> mengindikasikan bahwa unit-unit ini cenderung memiliki tingkat okupansi 
        (pesanan) yang lebih rendah dibandingkan penyewaan unit secara utuh.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. HALAMAN: METRIK PERFORMA
# ==========================================
elif menu_aktif == "Metrik Performa":
    st.markdown("<h1>Evaluasi & Metrik Performa</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='font-size: 1.05rem; color: #475569; margin-bottom: 2rem;'>
            Evaluasi kuantitatif untuk membandingkan kemampuan prediktif antara <strong>Regresi Logistik Multinomial (MLR)</strong> 
            dan <strong>Analisis Diskriminan Linier (LDA)</strong>.
        </div>
    """, unsafe_allow_html=True)
    
    data_metrik = pd.DataFrame({
        'Metrik Evaluasi': ['Macro Precision', 'Macro Recall', 'Macro F1-Score'],
        'Regresi Logistik (MLR)': [0.7525, 0.5745, 0.5759],
        'Diskriminan Linier (LDA)': [0.8117, 0.5857, 0.5967]
    })

    c_metrik1, c_metrik2 = st.columns(2)
    with c_metrik1:
        st.markdown("<h2>Matriks Evaluasi Komparatif</h2>", unsafe_allow_html=True)
        # Menambahkan nilai teks pada batang
        df_melt = data_metrik.melt(id_vars='Metrik Evaluasi')
        fig_eval = px.bar(
            df_melt, x='Metrik Evaluasi', y='value', color='variable', barmode='group', 
            color_discrete_sequence=['#5499c7', '#1e3c72'], text=df_melt['value'].apply(lambda x: f"{x:.4f}")
        )
        fig_eval.update_traces(textposition='outside', hovertemplate="<b>Metrik:</b> %{x}<br><b>Skor:</b> %{y:,.4f}<extra></extra>")
        fig_eval.update_layout(legend_title_text="Algoritma Pemodelan", yaxis_title="Skor Nilai", xaxis_title="")
        st.plotly_chart(terapkan_tema_grafik(fig_eval), use_container_width=True)
        
    with c_metrik2:
        st.markdown("<h2>Rekomendasi Strategis</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box" style="border-left-color: #1e3c72;">
            Meskipun tingkat akurasi absolut (*top-line accuracy*) mengisyaratkan kesetaraan antar model (~82.9%), 
            analisis metrik yang lebih dalam mengungkap divergensi kapabilitas yang nyata.<br><br>
            <strong>Analisis Diskriminan Linier (LDA)</strong> direkomendasikan sebagai instrumen operasional yang superior. 
            Keunggulannya pada <i>Macro Precision</i> (0.81 vs 0.75) dan <i>Macro F1-Score</i> membuktikan mekanisme yang jauh lebih 
            tangguh dalam menangani ketidakseimbangan kelas ekstrem di dunia nyata, secara presisi mampu mengidentifikasi segmen 
            minoritas 'Shared room' tanpa melakukan prediksi berlebih (*over-predicting*).
        </div>
        """, unsafe_allow_html=True)
