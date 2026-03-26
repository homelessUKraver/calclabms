def analizuj_widmo_ms(pik_m, pik_m1, pik_m2):
    """
    Funkcja analizuje intensywności pików izotopowych i szacuje skład cząsteczki.
    Wartości podajemy jako surowe liczby z detektora (funkcja sama je znormalizuje).
    """
    print("--- 🔬 WYNIKI AUTOMATYCZNEJ ANALIZY MS ---")
    
    # 1. Normalizacja danych (ustawiamy główny pik M jako 100%)
    m_norm = 100.0
    m1_norm = (pik_m1 / pik_m) * 100.0
    m2_norm = (pik_m2 / pik_m) * 100.0
    
    print(f"Znormalizowane intensywności:")
    print(f"M   : {m_norm:.1f}%")
    print(f"M+1 : {m1_norm:.1f}%")
    print(f"M+2 : {m2_norm:.1f}%\n")

    # 2. Szacowanie liczby atomów węgla (C)
    # Dzielimy intensywność M+1 przez naturalne występowanie 13C (1.1%)
    liczba_wegli = round(m1_norm / 1.1)
    print(f"➡️ Szacowana liczba atomów węgla (C): ~{liczba_wegli}")

    # 3. Analiza piku M+2 (Szukanie Cl, Br, S) z marginesem tolerancji
    tolerancja_halogenow = 5.0  # Pozwalamy na 5% błędu maszyny
    tolerancja_siarki = 1.0     # Siarka daje mały pik, tu tolerancja musi być mniejsza

    if abs(m2_norm - 100.0) <= tolerancja_halogenow:
        print("🚨 WYKRYTO BROM (Br): Stosunek pików ok. 1:1 wskazuje na 1 atom bromu.")
        
    elif abs(m2_norm - 33.0) <= tolerancja_halogenow:
        print("🚨 WYKRYTO CHLOR (Cl): Stosunek pików ok. 3:1 wskazuje na 1 atom chloru.")
        
    elif abs(m2_norm - 4.4) <= tolerancja_siarki:
        print("⚠️ WYKRYTO SIARKĘ (S): Widoczny charakterystyczny pik izotopu 34S.")
        
    else:
        print("ℹ️ Brak wyraźnych sygnatur wskazujących na obecność 1 atomu Cl, Br lub S.")

# --- TESTOWANIE SKRYPTU ---

# Przykład 1: Chlorobenzen (wzór C6H5Cl)
# Oczekujemy: ok. 6 węgli i 1 atomu chloru
print("Test 1: Chlorobenzen")
analizuj_widmo_ms(pik_m=5000, pik_m1=330, pik_m2=1640)
print("\n" + "="*40 + "\n")

# Przykład 2: Jakaś substancja z siarką (np. prosta cząsteczka tiofenu C4H4S)
# Oczekujemy: ok. 4 węgli i atomu siarki
print("Test 2: Tiofen")
analizuj_widmo_ms(pik_m=12000, pik_m1=530, pik_m2=540)
