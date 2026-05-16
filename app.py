import streamlit as st
import pandas as pd
import numpy as np

# 1. Konfigurasi Halaman
st.set_page_config(page_title="PBL Ekonomi SDA - Kelompok Kapur", layout="wide")

# 2. Header dengan Logo, Judul, dan Identitas
col_logo, col_judul = st.columns([1, 5])
with col_logo:
    st.image("logo unisba.png", width=110) 

with col_judul:
    st.title("Analisis Intertemporal Sumber Daya Alam: Komoditas Batu Kapur")
    st.markdown("#### **PT. Solusi Bangun Indonesia**")
    
    col_identitas1, col_identitas2 = st.columns([2, 1])
    with col_identitas1:
        st.markdown("### **Kelompok 8 - Ekonomi Pembangunan**")
    with col_identitas2:
        st.markdown("### **Dosen Pengampu: Yukha Sundaya S.E., M.Si.**")
    
    st.markdown("""
    **Anggota Kelompok:** Muhamad Bagya Adytia (10090224006) &nbsp; | &nbsp; Ridho Ahmad Fauzi (10090224031)
    """)

st.markdown("---")

# ==========================================
# 3. SIDEBAR (PANEL KIRI)
# ==========================================
st.sidebar.header("⚙️ Kontrol Simulasi")

harga_kapur = st.sidebar.slider("Harga Batu Kapur (Rp/ton)", min_value=500000, max_value=2000000, value=910000, step=10000)
diskonto = st.sidebar.slider("Tingkat Diskonto (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5) / 100
muc_awal = st.sidebar.slider("MUC Awal (Rp)", min_value=0, max_value=500000, value=150000, step=5000)
pajak_karbon = st.sidebar.slider("Pajak Karbon Future (Rp)", min_value=0, max_value=100000, value=30000, step=1000)
biaya_ekstraksi = st.sidebar.number_input("Biaya Ekstraksi (MC) - Rp/ton", value=500000, step=10000)

st.sidebar.markdown("---")
st.sidebar.write("💡 *Parameter di atas akan otomatis mengubah seluruh perhitungan di grafik.*")

st.sidebar.markdown("<br><br>", unsafe_allow_html=True) 
st.sidebar.markdown("<h4 style='text-align: center; color: gray;'>FEB UNISBA | Ekonomi Sumber Daya Alam</h4>", unsafe_allow_html=True)

# ==========================================
# 4. MENU TABS & KONTEN UTAMA
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 Data & Cadangan", 
    "📈 Analisis Hostelling", 
    "🏢 Struktur Pasar", 
    "🔋 Simulasi Stok", 
    "🌿 Green Paradox"
])

# Data Historis Kapur
data_kapur = {
    "Tahun": list(range(2014, 2025)),
    "P": [1130000, 1110000, 915000, 835000, 812000, 916000, 903000, 834000, 935000, 924000, 910000],
    "Q": [8.4, 9.1, 10.2, 11.1, 11.9, 11.8, 11.5, 13.4, 13.1, 13.5, 13.8]
}
df = pd.DataFrame(data_kapur)

# ==========================================
# ISI MASING-MASING TAB
# ==========================================

with tab1:
    st.header("📂 Data Historis & Parameter Dasar")
    
    # --- BAGIAN BARU: KOTAK PARAMETER DASAR ANALISIS ---
    st.subheader("Parameter Dasar Analisis")
    st.info("Nilai parameter di bawah ini terhubung langsung dengan panel di sebelah kiri dan data historis.")
    
    # Membuat 4 kotak berdampingan (seperti visual dashboard profesional)
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    
    with col_p1:
        rata_harga = df['P'].mean()
        st.metric(label="Rata-rata Harga Historis", value=f"Rp {rata_harga:,.0f}")
    
    with col_p2:
        rata_q = df['Q'].mean()
        st.metric(label="Rata-rata Ekstraksi (Q)", value=f"{rata_q:.1f} Ton")
        
    with col_p3:
        st.metric(label="Tingkat Diskonto (r)", value=f"{diskonto * 100:.1f} %")
        
    with col_p4:
        st.metric(label="Biaya Ekstraksi (MC)", value=f"Rp {biaya_ekstraksi:,.0f}")
    
    st.markdown("---")
    
    # --- BAGIAN DATA DAN GRAFIK ---
    col_a, col_b = st.columns([2, 3])
    with col_a:
        st.subheader("Tabel Data Historis")
        st.dataframe(df, use_container_width=True)
    with col_b:
        st.subheader("Tren Produksi (Q)")
        st.bar_chart(df.set_index("Tahun")["Q"], color="#795548") # Diberi warna cokelat kapur

with tab2:
   # 1. Judul Utama Komponen
    st.title("Model Optimasi Hotelling")
    
    # 2. Menghitung Data Proyeksi (7 Tahun: 2025 - 2031)
    tahun_proyeksi = np.arange(2025, 2032)
    t_step = np.arange(0, 7)
    
    # Perhitungan Kaidah Hotelling Akurat
    proyeksi_muc = muc_awal * (1 + diskonto)**t_step
    proyeksi_harga = biaya_ekstraksi + proyeksi_muc
    
    # Membuat DataFrame Utama
    df_hotelling = pd.DataFrame({
        "Tahun": tahun_proyeksi,
        "MUC (Rp)": proyeksi_muc,
        "Harga (Rp)": proyeksi_harga
    })

    # 3. Membagi Layout Menjadi 2 Kolom (Kiri: Tabel, Kanan: Grafik)
    col_kiri, col_kanan = st.columns([2, 3])
    
    with col_kiri:
        st.markdown("**Tabel Proyeksi Harga & MUC**")
        # Menampilkan tabel dengan format ribuan tanpa desimal agar rapi
        st.dataframe(
            df_hotelling.style.format({
                "Tahun": "{:.0f}",
                "MUC (Rp)": "{:,.0f}",
                "Harga (Rp)": "{:,.0f}"
            }), 
            use_container_width=True
        )
        
    with col_kanan:
        st.markdown("**Keseimbangan Nilai Intertemporal**")
        
        # MEMBUAT GRAFIK TANPA MATPLOTLIB (MENGGUNAKAN BAWAAN STREAMLIT)
        # Mengatur kolom 'Tahun' menjadi index agar otomatis menjadi Sumbu X di grafik
        df_grafik = df_hotelling.set_index("Tahun")
        
        # Menampilkan line chart dengan pilihan warna khusus (Hijau untuk Harga, Biru untuk MUC)
        st.line_chart(
            df_grafik[["Harga (Rp)", "MUC (Rp)"]], 
            color=["#16a34a", "#2563eb"]
        )
        
        # 4. Kotak Deskripsi Biru Gelap di Bawah Grafik
        st.markdown("""
        <div style="background-color: #12233c; padding: 15px; border-radius: 4px; border-left: 4px solid #1d4ed8; margin-top: 10px;">
            <p style="color: #38bdf8; margin: 0; font-size: 13.5px; line-height: 1.5;">
                <strong>Deskripsi:</strong> Grafik Kaidah Hotelling ini menggambarkan bahwa seiring menipisnya cadangan, 
                nilai kelangkaan (MUC) meningkat secara eksponensial searah tingkat diskonto, yang mendorong harga proyeksi 
                batu kapur terus naik di masa depan.
            </p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    with tab3:
    st.title("Simulasi Dinamis Struktur Pasar")
    st.write("Gunakan slider di sidebar untuk melihat perubahan ekuilibrium pasar secara real-time.")

    # 1. LOGIKA PERHITUNGAN DINAMIS
    # Menghitung output Cournot atau Monopoli berdasarkan input
    q_range = np.linspace(0, permintaan_max / slope, 100)
    
    # Fungsi Permintaan: P = A - B*Q
    def hitung_harga(q):
        return permintaan_max - (slope * q)

    # Ekuilibrium Pasar (Penyederhanaan Model Cournot)
    q_opt_total = (permintaan_max - biaya_marginal) / (slope * (jumlah_perusahaan + 1))
    p_opt = hitung_harga(q_opt_total)
    profit_per_perusahaan = (p_opt - biaya_marginal) * (q_opt_total / jumlah_perusahaan)

    # 2. VISUALISASI DINAMIS (Menggunakan st.line_chart agar ringan & bergerak)
    df_plot = pd.DataFrame({
        "Kuantitas": q_range,
        "Harga Permintaan": [hitung_harga(q) for q in q_range],
        "Biaya Marginal (MC)": [biaya_marginal] * 100
    }).set_index("Kuantitas")

    st.subheader("Kurva Permintaan vs Biaya")
    st.line_chart(df_plot)

    # 3. OUTPUT METRIK DINAMIS
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Output Pasar", f"{q_opt_total:,.2f} Ton")
    col2.metric("Harga Ekuilibrium", f"Rp {p_opt:,.0f}")
    col3.metric("Profit Per Perusahaan", f"Rp {profit_per_perusahaan:,.0f}")

    st.info(f"Saat ini pasar diasumsikan sebagai **{'Monopoli' if jumlah_perusahaan == 1 else 'Oligopoli'}**.")

with tab4:
    st.header("Simulasi Penurunan Stok Sumber Daya (Deplesi)")
    cadangan_awal = st.number_input("Masukkan Estimasi Cadangan Awal Tahun 2014 (Ton / Juta Ton)", min_value=50.0, value=250.0, step=10.0)
    
    df_stok = df[['Tahun', 'Q']].copy()
    df_stok.rename(columns={'Q': 'Ekstraksi Tahunan'}, inplace=True)
    
    rata_ekstraksi = df_stok['Ekstraksi Tahunan'].mean()
    tahun_proyeksi_stok = np.arange(2025, 2035)
    ekstraksi_proyeksi = np.full(10, rata_ekstraksi) 
    
    df_proyeksi_stok = pd.DataFrame({'Tahun': tahun_proyeksi_stok, 'Ekstraksi Tahunan': ekstraksi_proyeksi})
    df_full_stok = pd.concat([df_stok, df_proyeksi_stok], ignore_index=True)
    df_full_stok['Sisa Cadangan'] = cadangan_awal - df_full_stok['Ekstraksi Tahunan'].cumsum()
    df_full_stok['Sisa Cadangan'] = df_full_stok['Sisa Cadangan'].apply(lambda x: max(0, x))
    
    col_graf_stok, col_tab_stok = st.columns([3, 2])
    with col_graf_stok:
        st.subheader("Grafik Sisa Cadangan")
        st.area_chart(df_full_stok.set_index("Tahun")["Sisa Cadangan"], color="#00C853")
    with col_tab_stok:
        st.subheader("Tabel Laju Deplesi")
        st.dataframe(df_full_stok.style.format("{:,.1f}"), use_container_width=True)

with tab5:
    st.header("🌿 Analisis Green Paradox")
    st.write("Fenomena **Green Paradox** terjadi ketika pengumuman kebijakan lingkungan di masa depan (misal: pajak karbon) justru memicu produsen untuk mempercepat ekstraksi sumber daya saat ini demi menghindari beban pajak tersebut, yang malah meningkatkan emisi dalam jangka pendek.")
    st.markdown("---")
    
    col_gp1, col_gp2 = st.columns([3, 2])
    with col_gp1:
        st.subheader("Simulasi Laju Ekstraksi (Q): Baseline vs Green Paradox")
        tahun_gp = np.arange(2024, 2035)
        rata_q = df['Q'].mean()
        
        q_baseline = rata_q * (1 - 0.01)**np.arange(11) 
        faktor_panik = min(pajak_karbon / 100000, 1.5) 
        
        q_gp = np.zeros(11)
        q_gp[:5] = q_baseline[:5] * (1 + faktor_panik) 
        q_gp[5:] = q_baseline[5:] * 0.4 
        
        df_gp = pd.DataFrame({
            "Tahun": tahun_gp,
            "Baseline (Skenario Normal)": q_baseline,
            "Green Paradox (Efek Pengumuman Pajak)": q_gp
        }).set_index("Tahun")
        
        st.line_chart(df_gp, color=["#A9A9A9", "#D32F2F"])
        
    with col_gp2:
        st.subheader("Dampak Kebijakan")
        st.info(f"**Pajak Karbon Future:** Rp {pajak_karbon:,.0f} / ton")
        
        st.markdown(f"""
        **Interpretasi Grafik:**
        * 📈 **Kurva Merah (Green Paradox):** Karena ada pengumuman pajak sebesar **Rp {pajak_karbon:,.0f}** di masa depan, perusahaan batu kapur memilih untuk mengekstraksi lebih banyak di masa sekarang.
        * 📉 **Kurva Abu-abu (Baseline):** Adalah proyeksi ekstraksi jika pemerintah tidak mengumumkan pajak karbon.
        * ⚠️ **Kesimpulan:** Niat pemerintah menekan emisi berpotensi menjadi bumerang jangka pendek jika transisinya tidak diatur.
        """)

# ==========================================
# 5. FOOTER (BAGIAN BAWAH HALAMAN)
# ==========================================
st.markdown("<br><br><br>", unsafe_allow_html=True) # Memberi jarak kosong dari konten di atasnya
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>"
    "Dashboard Analisis Ekonomi SDA | PBL 3 | FEB UNISBA | 2026"
    "</p>", 
    unsafe_allow_html=True
)
