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

# --- TAMBAHKAN KODE INI DI BAWAH BIAYA EKSTRAKSI PADA SIDEBAR ---

st.sidebar.markdown("---")
st.sidebar.subheader("Parameter Struktur Pasar")
permintaan_max = st.sidebar.slider("Permintaan Maksimum (Choke Price)", 1000000, 3000000, 2000000)
slope = st.sidebar.slider("Slope Permintaan (Sensitivity)", 0.01, 0.50, 0.10)
jumlah_perusahaan = st.sidebar.slider("Jumlah Perusahaan di Pasar", 1, 10, 3)

# ----------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.write("💡 *Parameter di atas akan otomatis mengubah seluruh perhitungan di grafik.*")

st.sidebar.markdown("---")
st.sidebar.subheader("Parameter Struktur Pasar")
permintaan_max = st.sidebar.slider("Permintaan Maksimum (A)", 1000000, 3000000, 2000000)
slope = st.sidebar.slider("Slope Permintaan (B)", 0.01, 0.50, 0.10)
# Slider 'n' inilah yang akan mengubah struktur pasar secara otomatis
jumlah_perusahaan = st.sidebar.slider("Jumlah Perusahaan (n)", 1, 50, 3)

st.sidebar.markdown("<br><br>", unsafe_allow_html=True) 
st.sidebar.markdown("<h4 style='text-align: center; color: gray;'>FEB UNISBA | Ekonomi Sumber Daya Alam</h4>", unsafe_allow_html=True)

# ==========================================
# 4. MENU TABS & KONTEN UTAMA
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 Data & Cadangan", 
    "📈 Analisis Hotelling", 
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
    st.title("Simulasi Dinamis Struktur Pasar")
    
    # --- LANDASAN TEORI (Sesuai Permintaan Dosen) ---
    st.info("""
    **Landasan Teoritis:** Struktur pasar menentukan bagaimana harga dan kuantitas produksi ditetapkan, yang pada gilirannya memengaruhi kecepatan deplesi cadangan. 
    Tiga struktur yang dianalisis:
    1. **Persaingan Sempurna ($P = MC$):** Efisien secara statik namun mengakibatkan deplesi (pengurasan) cadangan tercepat.
    2. **Oligopoli Cournot ($n$ perusahaan):** Perusahaan bersaing dalam kuantitas, menghasilkan output di antara monopoli dan persaingan sempurna.
    3. **Monopoli ($MR = MC$):** Harga ditetapkan di atas MC, produksi ditekan — secara paradoks memperlambat deplesi cadangan namun menciptakan kerugian kesejahteraan (*deadweight loss*).
    """)

    st.markdown("---")

    # --- LOGIKA PERHITUNGAN EKONOMI (MODEL COURNOT) ---
    # Rumus Umum Kuantitas Ekuilibrium: Q = (n / (n+1)) * ((A - MC) / B)
    n = jumlah_perusahaan
    A = permintaan_max
    B = slope
    MC = biaya_ekstraksi

    # 1. Menghitung Kuantitas (Q) dan Harga (P) Ekuilibrium
    if n >= 50: # Asumsi Persaingan Sempurna jika n besar
        q_ekuilibrium = (A - MC) / B
        label_pasar = "Persaingan Sempurna"
    elif n == 1:
        q_ekuilibrium = (A - MC) / (2 * B)
        label_pasar = "Monopoli"
    else:
        q_ekuilibrium = (n / (n + 1)) * ((A - MC) / B)
        label_pasar = f"Oligopoli Cournot (n={n})"

    p_ekuilibrium = A - (B * q_ekuilibrium)
    profit_total = (p_ekuilibrium - MC) * q_ekuilibrium

    # --- VISUALISASI GRAFIK BERGERAK ---
    # Membuat rentang Sumbu X (Kuantitas)
    batas_q = (A - MC) / B # Titik di mana P = MC (Persaingan Sempurna)
    q_axis = np.linspace(0, batas_q * 1.2, 100)
    
    # Kurva Permintaan (P = A - BQ)
    p_demand = A - (B * q_axis)
    # Kurva Marginal Revenue (MR = A - 2BQ) - Hanya muncul untuk Monopoli
    p_mr = A - (2 * B * q_axis)
    
    df_grafik = pd.DataFrame({
        "Kuantitas": q_axis,
        "Harga Permintaan (P)": p_demand,
        "Biaya Marginal (MC)": [MC] * 100,
        "Marginal Revenue (MR)": p_mr
    }).set_index("Kuantitas")

    st.subheader(f"Grafik Ekuilibrium: {label_pasar}")
    
    # Menampilkan grafik yang bergerak mengikuti slider
    st.line_chart(df_grafik, color=["#2563eb", "#ef4444", "#f59e0b"])

    # --- OUTPUT METRIK ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Kuantitas Produksi (Q)", f"{q_ekuilibrium:,.0f} Ton")
    col2.metric("Harga Pasar (P)", f"Rp {p_ekuilibrium:,.0f}")
    col3.metric("Total Profit Industri", f"Rp {profit_total:,.0f}")

    # --- PENJELASAN DINAMIS ---
    if n == 1:
        st.warning("⚠️ **Efek Monopoli:** Produksi ditekan rendah agar harga tetap tinggi. Deplesi cadangan batu kapur menjadi yang paling lambat, namun terjadi *Deadweight Loss* yang tinggi.")
    elif n >= 50:
        st.error("⚠️ **Efek Persaingan Sempurna:** Produksi sangat tinggi dengan harga rendah (P=MC). Cadangan batu kapur akan habis dalam waktu paling singkat (Deplesi Tercepat).")
    else:
        st.success(f"✅ **Efek Oligopoli:** Dengan {n} perusahaan, tingkat deplesi dan kesejahteraan berada pada titik moderat.")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("Tabel Perbandingan Skenario Struktur Pasar")
    st.write("Berikut adalah perbandingan metrik ekonomi antara Monopoli, Oligopoli (berdasarkan *slider*), dan Persaingan Sempurna dengan menggunakan parameter saat ini:")

    # 1. Perhitungan Skenario Monopoli Mutlak (n = 1)
    q_monopoli = (A - MC) / (2 * B)
    p_monopoli = A - (B * q_monopoli)
    profit_monopoli = (p_monopoli - MC) * q_monopoli

    # 2. Perhitungan Skenario Persaingan Sempurna Mutlak (P = MC)
    q_sempurna = (A - MC) / B
    p_sempurna = MC
    profit_sempurna = 0

    # 3. Skenario Oligopoli diambil dari variabel yang sudah dihitung sebelumnya di atas
    # (q_ekuilibrium, p_ekuilibrium, dan profit_total)

    # Membuat DataFrame untuk Tabel Perbandingan
    df_perbandingan = pd.DataFrame({
        "Indikator Ekonomi": [
            "Kuantitas Produksi / Ekstraksi (Q)", 
            "Harga Pasar (P)", 
            "Total Profit Industri", 
            "Kecepatan Deplesi Cadangan"
        ],
        "Skenario Monopoli": [
            f"{q_monopoli:,.0f} Ton", 
            f"Rp {p_monopoli:,.0f}", 
            f"Rp {profit_monopoli:,.0f}", 
            "Paling Lambat"
        ],
        f"Skenario Saat Ini (n={n})": [
            f"{q_ekuilibrium:,.0f} Ton", 
            f"Rp {p_ekuilibrium:,.0f}", 
            f"Rp {profit_total:,.0f}", 
            "Moderat"
        ],
        "Persaingan Sempurna": [
            f"{q_sempurna:,.0f} Ton", 
            f"Rp {p_sempurna:,.0f}", 
            "Rp 0 (Break-Even)", 
            "Paling Cepat"
        ]
    }).set_index("Indikator Ekonomi")

    # Menampilkan tabel perbandingan
    st.table(df_perbandingan)

    # Menambahkan rangkuman kesimpulan di bawah tabel
    st.info("""
    **Kesimpulan Analisis:**
    * **Monopoli** menghasilkan profit tertinggi bagi perusahaan ekstraktif, namun sangat merugikan konsumen karena harga yang tinggi.
    * **Persaingan Sempurna** memberikan harga ekuilibrium terendah bagi konsumen, namun memicu eksploitasi besar-besaran yang mengancam ketahanan cadangan (deplesi masif).
    * Dalam industri batu kapur dengan hambatan masuk tinggi (*barrier to entry*), struktur **Oligopoli** merupakan kondisi paling realistis yang terjadi di lapangan.
    """)
    
with tab4:
    st.title("Simulasi Deplesi Stok: Persaingan vs Oligopoli vs Monopoli")
    
    st.info("""
    **Model Intertemporal Dinamis:** Bagian ini mensimulasikan bagaimana ketiga struktur pasar menguras cadangan batu kapur dari tahun ke tahun. 
    Menggabungkan **Aturan Hotelling** ($MUC_t = MUC_0(1+r)^t$) dengan perilaku pasar untuk melihat proyeksi Produksi, Harga, dan Sisa Cadangan.
    """)
    
    # 1. Input Parameter Khusus Simulasi Stok
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        stok_awal_kapur = st.number_input("Estimasi Total Cadangan Awal (Ton)", min_value=10000000, value=100000000, step=10000000)
    with col_input2:
        tahun_simulasi = st.slider("Durasi Proyeksi (Tahun)", 5, 30, 15)

    st.markdown("---")

    # 2. Setup Data Time-Series
    T_years = np.arange(2025, 2025 + tahun_simulasi)
    
    # Variabel Penyimpanan (Arrays)
    q_pc, p_pc, s_pc = [], [], []
    q_oli, p_oli, s_oli = [], [], []
    q_mono, p_mono, s_mono = [], [], []
    
    # Inisialisasi Stok Berjalan
    curr_s_pc = stok_awal_kapur
    curr_s_oli = stok_awal_kapur
    curr_s_mono = stok_awal_kapur
    
    n_perusahaan = jumlah_perusahaan # Mengambil nilai dari slider sidebar
    
    # 3. Looping Simulasi (Menghitung dinamika pasar dari tahun ke tahun)
    for t in range(tahun_simulasi):
        # MUC naik setiap tahun sesuai diskonto
        muc_t = muc_awal * (1 + diskonto)**t 
        biaya_total_t = biaya_ekstraksi + muc_t
        
        # A. PASAR PERSAINGAN SEMPURNA (P = MC + MUC)
        if curr_s_pc > 0:
            # Q = (A - Biaya) / B
            q_tmp_pc = max(0, (permintaan_max - biaya_total_t) / slope)
            # Jika Q produksi melebihi sisa stok, maka produksi = sisa stok
            if curr_s_pc < q_tmp_pc: q_tmp_pc = curr_s_pc
            p_tmp_pc = permintaan_max - (slope * q_tmp_pc)
            curr_s_pc -= q_tmp_pc
        else:
            q_tmp_pc, p_tmp_pc = 0, 0
        
        q_pc.append(q_tmp_pc); p_pc.append(p_tmp_pc); s_pc.append(curr_s_pc)
        
        # B. PASAR OLIGOPOLI (Model Cournot)
        if curr_s_oli > 0:
            # Q = (n/(n+1)) * ((A - Biaya) / B)
            q_tmp_oli = max(0, (n_perusahaan / (n_perusahaan + 1)) * ((permintaan_max - biaya_total_t) / slope))
            if curr_s_oli < q_tmp_oli: q_tmp_oli = curr_s_oli
            p_tmp_oli = permintaan_max - (slope * q_tmp_oli)
            curr_s_oli -= q_tmp_oli
        else:
            q_tmp_oli, p_tmp_oli = 0, 0
            
        q_oli.append(q_tmp_oli); p_oli.append(p_tmp_oli); s_oli.append(curr_s_oli)
        
        # C. PASAR MONOPOLI (MR = MC + MUC)
        if curr_s_mono > 0:
            # Q = (A - Biaya) / 2B
            q_tmp_mono = max(0, (permintaan_max - biaya_total_t) / (2 * slope))
            if curr_s_mono < q_tmp_mono: q_tmp_mono = curr_s_mono
            p_tmp_mono = permintaan_max - (slope * q_tmp_mono)
            curr_s_mono -= q_tmp_mono
        else:
            q_tmp_mono, p_tmp_mono = 0, 0
            
        q_mono.append(q_tmp_mono); p_mono.append(p_tmp_mono); s_mono.append(curr_s_mono)

    # 4. Membungkus Data ke dalam DataFrame
    df_produksi = pd.DataFrame({
        "Tahun": T_years,
        "Persaingan Sempurna": q_pc,
        f"Oligopoli (n={n_perusahaan})": q_oli,
        "Monopoli": q_mono
    }).set_index("Tahun")

    df_stok = pd.DataFrame({
        "Tahun": T_years,
        "Persaingan Sempurna": s_pc,
        f"Oligopoli (n={n_perusahaan})": s_oli,
        "Monopoli": s_mono
    }).set_index("Tahun")

    df_harga = pd.DataFrame({
        "Tahun": T_years,
        "Persaingan Sempurna": p_pc,
        f"Oligopoli (n={n_perusahaan})": p_oli,
        "Monopoli": p_mono
    }).set_index("Tahun")

    # 5. Menampilkan 3 Grafik Utama (Menggunakan Native Streamlit Chart)
    warna_grafik = ["#ef4444", "#3b82f6", "#10b981"] # Merah (PC), Biru (Oligo), Hijau (Mono)
    
    st.subheader("1. Laju Produksi Ekstraksi Batu Kapur (Ton/Tahun)")
    st.line_chart(df_produksi, color=warna_grafik)
    
    st.subheader("2. Penurunan Sisa Stok Cadangan (Ton)")
    st.line_chart(df_stok, color=warna_grafik)
    
    st.subheader("3. Simulasi Pergerakan Harga Pasar (Rp/Ton)")
    st.line_chart(df_harga, color=warna_grafik)

    # 6. Tabel Rangkuman Data Terakhir (Tahun ke-N)
    st.markdown("---")
    st.subheader(f"Tabel Rekapitulasi Kondisi Tahun {T_years[-1]}")
    
    df_rekap = pd.DataFrame({
        "Struktur Pasar": ["Persaingan Sempurna", f"Oligopoli (n={n_perusahaan})", "Monopoli"],
        "Sisa Cadangan (Ton)": [s_pc[-1], s_oli[-1], s_mono[-1]],
        "Harga Akhir (Rp)": [p_pc[-1], p_oli[-1], p_mono[-1]],
        "Status Cadangan": [
            "Habis (Terkuras)" if s_pc[-1] <= 0 else "Masih Ada",
            "Habis (Terkuras)" if s_oli[-1] <= 0 else "Masih Ada",
            "Habis (Terkuras)" if s_mono[-1] <= 0 else "Masih Ada"
        ]
    })
    
    st.dataframe(df_rekap.style.format({
        "Sisa Cadangan (Ton)": "{:,.0f}",
        "Harga Akhir (Rp)": "{:,.0f}"
    }), use_container_width=True)
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
