import streamlit as st

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="Kalkulator MS", page_icon="🔬")

st.title("🔬 Kalkulator Izotopów MS")
st.write("Wprowadź surowe wartości intensywności pików z detektora (np. wysokość lub pole pod pikiem), aby zautomatyzować dedukcję.")

st.divider()

# --- POLA WEJŚCIOWE (KOLUMNY) ---
st.subheader("Wprowadź dane z widma")
col1, col2, col3 = st.columns(3)

with col1:
    pik_m = st.number_input("Intensywność piku M", min_value=0.1, value=10000.0, step=100.0, format="%.1f")
with col2:
    pik_m1 = st.number_input("Intensywność piku M+1", min_value=0.0, value=600.0, step=10.0, format="%.1f")
with col3:
    pik_m2 = st.number_input("Intensywność piku M+2", min_value=0.0, value=3300.0, step=100.0, format="%.1f")

# --- PRZYCISK ANALIZY ---
if st.button("Analizuj widmo 🚀"):
    
    # 1. Obliczenia i normalizacja
    m_norm = 100.0
    m1_norm = (pik_m1 / pik_m) * 100.0
    m2_norm = (pik_m2 / pik_m) * 100.0
    
    st.divider()
    st.subheader("📊 Wyniki analizy")
    
    # Wyświetlanie znormalizowanych wartości w ładnych kafelkach (metrics)
    st.write("**Znormalizowane intensywności względem piku głównego:**")
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Pik M", value=f"{m_norm:.1f}%")
    c2.metric(label="Pik M+1", value=f"{m1_norm:.1f}%")
    c3.metric(label="Pik M+2", value=f"{m2_norm:.1f}%")
    
    st.write("---")
    
    # 2. Szacowanie liczby atomów węgla (C)
    liczba_wegli = round(m1_norm / 1.1)
    st.info(f"**Szacowana liczba atomów węgla (C):** ~{liczba_wegli}")
    
    # 3. Analiza piku M+2 (Szukanie Cl, Br, S) z marginesem błędu
    tolerancja_halogenow = 5.0  
    tolerancja_siarki = 1.0     
    
    if abs(m2_norm - 100.0) <= tolerancja_halogenow:
        st.error("🚨 **WYKRYTO BROM (Br):** Stosunek pików ok. 1:1 wskazuje na 1 atom bromu.")
        
    elif abs(m2_norm - 33.0) <= tolerancja_halogenow:
        st.warning("🚨 **WYKRYTO CHLOR (Cl):** Stosunek pików ok. 3:1 wskazuje na 1 atom chloru.")
        
    elif abs(m2_norm - 4.4) <= tolerancja_siarki:
        st.success("⚠️ **WYKRYTO SIARKĘ (S):** Widoczny charakterystyczny pik izotopu 34S.")
        
    else:
        st.write("ℹ️ *Brak wyraźnych sygnatur wskazujących na obecność 1 atomu Cl, Br lub S.*")
