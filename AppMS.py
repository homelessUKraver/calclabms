import streamlit as st

st.set_page_config(page_title="Kalkulator MS PRO"")
st.title("Kalkulator Izotopów MS")
st.write("Wprowadź intensywności (np. w % lub z detektora). Jeśli jakiegoś piku nie ma na widmie, zostaw 0.")

st.divider()

# --- POLA WEJŚCIOWE (5 KOLUMN) ---
st.subheader("Wprowadź wysokości pików")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    pik_m = st.number_input("M", value=100.0, step=10.0, format="%.1f")
with c2:
    pik_m1 = st.number_input("M+1 (Węgiel)", value=1.1, step=0.1, format="%.1f")
with c3:
    pik_m2 = st.number_input("M+2", value=66.0, step=1.0, format="%.1f") # Domyślnie pod Cl2
with c4:
    pik_m4 = st.number_input("M+4", value=11.0, step=1.0, format="%.1f") # Domyślnie pod Cl2
with c5:
    pik_m6 = st.number_input("M+6", value=0.0, step=1.0, format="%.1f")

if st.button("Analizuj klaster izotopowy 🚀"):
    
    # Normalizacja względem piku M (M = 100%)
    m_norm = 100.0
    m1_norm = (pik_m1 / pik_m) * 100.0
    m2_norm = (pik_m2 / pik_m) * 100.0
    m4_norm = (pik_m4 / pik_m) * 100.0 if pik_m > 0 else 0.0
    m6_norm = (pik_m6 / pik_m) * 100.0 if pik_m > 0 else 0.0
    
    st.divider()
    st.subheader("📊 Wyniki analizy")
    
    # 1. Obliczanie węgla
    liczba_wegli = round(m1_norm / 1.1)
    st.info(f"**Szacowana liczba atomów węgla (C):** ~{liczba_wegli}")
    
    # 2. Silnik detekcji wzorców izotopowych
    # Tolerancja na błędy detektora (10% dla dużych pików, 5% dla małych)
    tol = 10.0 
    
    # Sprawdzamy wzorce od najbardziej złożonych do najprostszych
    
    # Wzorzec 3x Cl (27:27:9:1 -> Znormalizowane do M: 100% : 100% : 33% : 4%)
    if abs(m2_norm - 100.0) < tol and abs(m4_norm - 33.0) < tol:
        st.warning("🚨 **WYKRYTO 3 ATOMY CHLORU (Cl3):** Pasuje do wzorca 27:27:9:1 (np. chloroform).")
        
    # Wzorzec 2x Br (1:2:1 -> Znormalizowane do M: 100% : 200% : 100%)
    elif abs(m2_norm - 200.0) < 15.0 and abs(m4_norm - 100.0) < tol:
        st.error("🚨 **WYKRYTO 2 ATOMY BROMU (Br2):** Pasuje do wzorca 1:2:1.")
        
    # Wzorzec 1x Cl i 1x Br (3:4:1 -> Znormalizowane do M: 100% : 133% : 33%)
    elif abs(m2_norm - 133.0) < 15.0 and abs(m4_norm - 33.0) < tol:
        st.error("🚨 **WYKRYTO 1 CHLOR I 1 BROM (ClBr):** Pasuje do wzorca 3:4:1.")
        
    # Wzorzec 2x Cl (9:6:1 -> Znormalizowane do M: 100% : 66% : 11%)
    elif abs(m2_norm - 66.0) < tol and abs(m4_norm - 11.0) < 5.0:
        st.warning("🚨 **WYKRYTO 2 ATOMY CHLORU (Cl2):** Pasuje do wzorca 9:6:1 (np. dichlorometan).")
        
    # Wzorzec 1x Br (1:1 -> Znormalizowane do M: 100% : 100%)
    elif abs(m2_norm - 100.0) < tol and m4_norm < 5.0:
        st.error("🚨 **WYKRYTO 1 ATOM BROMU (Br):** Pasuje do wzorca 1:1.")
        
    # Wzorzec 1x Cl (3:1 -> Znormalizowane do M: 100% : 33%)
    elif abs(m2_norm - 33.0) < tol and m4_norm < 5.0:
        st.warning("🚨 **WYKRYTO 1 ATOM CHLORU (Cl):** Pasuje do wzorca 3:1.")
        
    # Detekcja Siarki, jeśli nie ma potężnych halogenów zagłuszających wynik
    elif abs(m2_norm - 4.4) < 1.0:
        st.success("⚠️ **WYKRYTO SIARKĘ (S):** Obecny pik izotopu 34S.")
        
    else:
        st.write("ℹ️ *Brak rozpoznanego wzorca izotopowego dla wielokrotnych halogenów.*")
