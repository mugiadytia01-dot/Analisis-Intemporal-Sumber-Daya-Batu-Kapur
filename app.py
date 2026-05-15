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
    st.title("Analisis Intemporal Sumber Daya Alam: Komoditas Batu Kapur")
    st.markdown("#### **PT. Solusi Bangun Indonesia**")
    
    col_identitas1, col_identitas2 = st.columns([2, 1])
    with col_identitas1:
        st.markdown("### **Kelompok 8 - Ekonomi Pembangunan**")
    with col_identitas2:
        st.markdown("### **Dosen Pengampu: Yukha Sundaya**")
    
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
    st.header("Analisis Aturan Hostelling (Hostelling Rule)")
    st.latex(r"P_t = P_0 (1 + r)^t")
    st.write("Aturan Hostelling menyatakan bahwa dalam pasar persaingan sempurna, harga bersih (net price) dari SDA tidak terbarukan akan meningkat sesuai tingkat diskonto.")
    
    tahun_proyeksi = np.arange(2024, 2035)
    t_step = np.arange(0, 11)
    
    proyeksi_harga = harga_kapur * (1 + diskonto)**t_step
    net_price = proyeksi_harga - biaya_ekstraksi
    
    df_hostelling = pd.DataFrame({
        "Tahun": tahun_proyeksi,
        "Proyeksi Harga (P)": proyeksi_harga,
        "Biaya Ekstraksi (MC)": biaya_ekstraksi,
        "Net Price (MUC)": net_price
    })

    col_grafik, col_tabel = st.columns([3, 2])
    with col_grafik:
        st.subheader("Grafik Lintasan Harga Optimal")
        st.line_chart(df_hostelling.set_index("Tahun")[["Proyeksi Harga (P)", "Net Price (MUC)"]])
    with col_tabel:
        st.subheader("Tabel Proyeksi")
        st.dataframe(df_hostelling.style.format("{:,.0f}"), use_container_width=True)

with tab3:
    st.header("Analisis Struktur Pasar")
    pilihan_pasar = st.selectbox("Pilih Model:", ["Persaingan Sempurna", "Monopoli", "Oligopoli"])
    q_sim = np.linspace(1, 20, 20)
    mc_sim = 2 + 1 * q_sim
    if pilihan_pasar == "Persaingan Sempurna":
        p_sim = np.full_like(q_sim, 15)
        df_p = pd.DataFrame({"Q": q_sim, "P=D": p_sim, "MC": mc_sim}).set_index("Q")
    elif pilihan_pasar == "Monopoli":
        p_sim = 30 - 1 * q_sim
        mr_sim = 30 - 2 * q_sim
        df_p = pd.DataFrame({"Q": q_sim, "D": p_sim, "MR": mr_sim, "MC": mc_sim}).set_index("Q")
    else:
        p_sim = np.where(q_sim <= 10, 25 - 0.5 * q_sim, 40 - 2 * q_sim)
        df_p = pd.DataFrame({"Q": q_sim, "D": p_sim, "MC": mc_sim}).set_index("Q")
    st.line_chart(df_p)

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