import streamlit as st
import pandas as pd

# --- PAGE SETTINGS ---
st.set_page_config(page_title="MS Calculator PRO", page_icon="🔬")
st.title("🔬 MS Isotope Calculator (PRO Version)")
st.write("Enter the mass (m/z) of the main peak and the heights of the individual peaks.")

st.divider()

# --- INPUT FIELDS ---
st.subheader("1. Enter the molecule mass")
mz_m = st.number_input("m/z of peak M (Total mass):", min_value=1.0, value=146.0, step=1.0)

st.subheader("2. Enter peak heights (e.g., raw detector data)")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    peak_m = st.number_input("M", value=8200.0, step=10.0, format="%.1f")
with c2:
    peak_m1 = st.number_input("M+1 (C)", value=550.0, step=1.0, format="%.1f")
with c3:
    peak_m2 = st.number_input("M+2", value=5400.0, step=10.0, format="%.1f") 
with c4:
    peak_m4 = st.number_input("M+4", value=920.0, step=10.0, format="%.1f") 
with c5:
    peak_m6 = st.number_input("M+6", value=0.0, step=1.0, format="%.1f")

# --- ANALYSIS BUTTON ---
if st.button("Analyze spectrum 🚀"):
    
    # Normalization relative to peak M
    m_norm = 100.0
    m1_norm = (peak_m1 / peak_m) * 100.0 if peak_m > 0 else 0.0
    m2_norm = (peak_m2 / peak_m) * 100.0 if peak_m > 0 else 0.0
    m4_norm = (peak_m4 / peak_m) * 100.0 if peak_m > 0 else 0.0
    m6_norm = (peak_m6 / peak_m) * 100.0 if peak_m > 0 else 0.0
    
    st.divider()
    st.subheader("📊 Analysis Results")
    
    # 1. Carbon Estimation
    carbon_count = round(m1_norm / 1.1)
    st.info(f"**Estimated number of Carbon (C) atoms:** ~{carbon_count}")
    
    # Variables to track detected heteroatoms
    cl_count = 0
    br_count = 0
    s_count = 0
    
    # 2. Isotope Pattern Detection Engine
    tol = 10.0 
    
    if abs(m2_norm - 100.0) < tol and abs(m4_norm - 33.0) < tol:
        st.warning("🚨 **DETECTED 3 CHLORINE ATOMS (Cl3)**")
        cl_count = 3
    elif abs(m2_norm - 200.0) < 15.0 and abs(m4_norm - 100.0) < tol:
        st.error("🚨 **DETECTED 2 BROMINE ATOMS (Br2)**")
        br_count = 2
    elif abs(m2_norm - 133.0) < 15.0 and abs(m4_norm - 33.0) < tol:
        st.error("🚨 **DETECTED 1 CHLORINE AND 1 BROMINE (ClBr)**")
        cl_count = 1
        br_count = 1
    elif abs(m2_norm - 66.0) < tol and abs(m4_norm - 11.0) < 5.0:
        st.warning("🚨 **DETECTED 2 CHLORINE ATOMS (Cl2)**")
        cl_count = 2
    elif abs(m2_norm - 100.0) < tol and m4_norm < 5.0:
        st.error("🚨 **DETECTED 1 BROMINE ATOM (Br)**")
        br_count = 1
    elif abs(m2_norm - 33.0) < tol and m4_norm < 5.0:
        st.warning("🚨 **DETECTED 1 CHLORINE ATOM (Cl)**")
        cl_count = 1
    elif abs(m2_norm - 4.4) < 1.0:
        st.success("⚠️ **DETECTED SULFUR (S)**")
        s_count = 1
    else:
        st.write("ℹ️ *No clear halogen/sulfur pattern detected.*")

    # --- MISSING MASS CALCULATOR ---
    st.divider()
    st.subheader("🧩 Molecular Formula Assembly")
    
    # Using monoisotopic masses (the lightest isotopes in the cluster)
    mass_c = carbon_count * 12
    mass_cl = cl_count * 35
    mass_br = br_count * 79
    mass_s = s_count * 32
    
    identified_mass = mass_c + mass_cl + mass_br + mass_s
    missing_mass = int(mz_m - identified_mass)
    
    st.write(f"Total mass (m/z): **{mz_m}**")
    st.write(f"Mass of identified fragments (Carbon + Halogens/S): **{identified_mass}**")
    
    if missing_mass >= 0:
        st.write(f"Missing mass: **{missing_mass}** *(Assuming these are Hydrogen 'H' atoms)*")
        
        # Generating a clean molecular formula string
        formula = f"C{carbon_count}" if carbon_count > 0 else ""
        formula += f" H{missing_mass}" if missing_mass > 0 else ""
        formula += f" Cl{cl_count}" if cl_count > 0 else ""
        formula += f" Br{br_count}" if br_count > 0 else ""
        formula += f" S{s_count}" if s_count > 0 else ""
        
        st.success(f"### Proposed formula: {formula.strip()}")
    else:
        st.error(f"Error! Identified fragments ({identified_mass} Da) weigh more than the whole molecule ({mz_m} Da). Check your input data!")

    # --- VISUALIZATION ---
    st.divider()
    st.subheader("📈 Cluster Visualization")
    chart_data = pd.DataFrame({
        "Peak": ["M", "M+1", "M+2", "M+4", "M+6"],
        "Intensity [%]": [m_norm, m1_norm, m2_norm, m4_norm, m6_norm]
    }).set_index("Peak")
    
    st.bar_chart(chart_data)
