import streamlit as st
import numpy as np

# Title
st.title("Arterial Blood Gas (ABG), AKI, and MELD-Na Interpretation Tool")

# Introduction
st.write("""
**Introduction:**
Interpreting an arterial blood gas (ABG) is crucial for healthcare professionals, especially in critically ill patients. 
This tool follows a six-step process to help you interpret ABG values accurately, assess for Acute Kidney Injury (AKI), and calculate the MELD-Na score.
""")

# Step 1: Input ABG Values
st.header("Step 1: Input ABG Values")
pH = st.number_input("Enter pH (normal range: 7.35 - 7.45)", min_value=0.0, max_value=14.0, value=7.4)
pCO2 = st.number_input("Enter PaCO2 (mmHg) (normal range: 35 - 45)", min_value=0.0, value=40.0)
HCO3 = st.number_input("Enter HCO3- (mmol/L) (normal range: 22 - 26)", min_value=0.0, value=24.0)
Na = st.number_input("Enter Sodium (Na+) (mmol/L)", min_value=0.0, value=140.0)
Cl = st.number_input("Enter Chloride (Cl-) (mmol/L)", min_value=0.0, value=100.0)
albumin = st.number_input("Enter Albumin (g/dL)", min_value=0.0, value=4.0)
FiO2 = st.number_input("Enter FiO2 (fraction of inspired oxygen, e.g., 0.21 for room air)", min_value=0.0, value=0.21)
PaO2 = st.number_input("Enter PaO2 (mmHg)", min_value=0.0, value=80.0)

# Step 2: Determine Acidemia/Alkalemia
if pH < 7.35:
    acid_base_status = "Acidemia"
elif pH > 7.45:
    acid_base_status = "Alkalemia"
else:
    acid_base_status = "Normal"

st.write(f"### Acid-Base Status: {acid_base_status}")

# Step 3: Determine if disturbance is respiratory or metabolic
def classify_disturbance(pH, pCO2, HCO3):
    if acid_base_status == "Acidemia":
        if pCO2 > 45:
            return "Respiratory Acidosis"
        elif HCO3 < 22:
            return "Metabolic Acidosis"
    elif acid_base_status == "Alkalemia":
        if pCO2 < 35:
            return "Respiratory Alkalosis"
        elif HCO3 > 26:
            return "Metabolic Alkalosis"
    return "Normal"

disturbance = classify_disturbance(pH, pCO2, HCO3)
st.write(f"### Disturbance Type: {disturbance}")

# Step 4: Compensation Check
def expected_compensation(disturbance, HCO3, pCO2):
    if disturbance == "Metabolic Acidosis":
        expected_pCO2 = (1.5 * HCO3) + 8
        return expected_pCO2
    elif disturbance == "Respiratory Acidosis":
        return HCO3 + (pCO2 - 40) / 10
    elif disturbance == "Metabolic Alkalosis":
        return 40 + 0.6 * (HCO3 - 24)
    elif disturbance == "Respiratory Alkalosis":
        return HCO3 - 2 * (40 - pCO2) / 10
    return None

expected_HCO3 = expected_compensation(disturbance, HCO3, pCO2)
st.write(f"### Expected Compensation: {expected_HCO3}")

# Step 5: Anion Gap Calculation
anion_gap = Na - (Cl + HCO3)
st.write(f"### Anion Gap: {anion_gap:.2f} mEq/L")

# Step 6: Osmolar Gap Calculation
osmolal_gap = st.number_input("Enter measured osmolality (mOsm/kg)", min_value=0.0, value=290.0)
calculated_osmolarity = 2 * Na + (HCO3 / 18) + (Cl / 1.8)
osm_gap = osmolal_gap - calculated_osmolarity
st.write(f"### Osmolar Gap: {osm_gap:.2f}")

# Step 7: Calculate PaO2/FiO2 Ratio and ARDS Assessment
if FiO2 > 0:
    paO2_fiO2_ratio = PaO2 / FiO2
    st.write(f"### PaO2/FiO2 Ratio: {paO2_fiO2_ratio:.2f} mmHg")

    # ARDS Assessment
    if paO2_fiO2_ratio > 300:
        ards_severity = "Not ARDS"
    elif paO2_fiO2_ratio >= 201:
        ards_severity = "Mild ARDS"
    elif paO2_fiO2_ratio >= 101:
        ards_severity = "Moderate ARDS"
    else:
        ards_severity = "Severe ARDS"

    st.write(f"### ARDS Severity: {ards_severity}")
else:
    st.write("### Additional Information Needed: FiO2 cannot be zero for PaO2/FiO2 calculation.")

# Step 8: Total Oxygen Content Calculation
Hgb = st.number_input("Enter Hemoglobin (g/dL)", min_value=0.0, value=15.0)
SaO2 = st.number_input("Enter SaO2 (%)", min_value=0.0, value=95.0)

if Hgb > 0 and SaO2 > 0:
    CaO2 = (1.34 * Hgb * (SaO2 / 100)) + (0.003 * PaO2)
    st.write(f"### Total Oxygen Content (CaO2): {CaO2:.2f} mL O2/dL")
else:
    st.write("### Additional Information Needed for CaO2 Calculation:")
    st.write("To calculate total oxygen content (CaO2), provide Hemoglobin (Hgb) and SaO2 values.")

# Step 9: FENa Calculation for AKI
st.header("Step 9: FENa Calculation for AKI")
baseline_creatinine = st.number_input("Enter Baseline Serum Creatinine (mg/dL)", min_value=0.0, value=1.0)
current_creatinine = st.number_input("Enter Current Serum Creatinine (mg/dL)", min_value=0.0, value=1.5)
BUN = st.number_input("Enter Blood Urea Nitrogen (BUN) (mg/dL)", min_value=0.0, value=30.0)

# Check for AKI
if (current_creatinine - baseline_creatinine) > 0.3:
    aki_status = "AKI Detected"
else:
    aki_status = "No AKI Detected"
st.write(f"### AKI Status: {aki_status}")

# Input for urine values
urine_sodium = st.number_input("Enter Urine Sodium (mEq/L)", min_value=0.0, value=150.0)
urine_creatinine = st.number_input("Enter Urine Creatinine (mg/dL)", min_value=0.0, value=50.0)
serum_sodium = st.number_input("Enter Serum Sodium (mEq/L)", min_value=0.0, value=140.0)

if serum_sodium > 0:  # Prevent division by zero
    FENa = (urine_sodium * current_creatinine) / (urine_creatinine * serum_sodium) * 100
    st.write(f"### Fractional Excretion of Sodium (FENa): {FENa:.2f}%")

    # Assess Etiology based on FENa and BUN/Cr ratio
    bun_cr_ratio = BUN / current_creatinine

    if bun_cr_ratio > 20 and FENa < 1:
        etiology = "Likely Pre-Renal Etiology"
    elif bun_cr_ratio < 20 and FENa > 2:
        etiology = "Likely Intrinsic Renal Etiology"
    else:
        etiology = "Further evaluation needed"
    st.write(f"### AKI Etiology: {etiology}")
else:
    st.write("### Additional Information Needed: Serum Sodium cannot be zero for FENa calculation.")

# Step 10: MELD-Na Calculation
st.header("Step 10: MELD-Na Calculation")
bilirubin = st.number_input("Enter Bilirubin (mg/dL)", min_value=0.0, value=1.0)
INR = st.number_input("Enter INR", min_value=0.0, value=1.0)

# Calculate MELD Score
MELD = (0.957 * np.log(current_creatinine) + 0.378 * np.log(bilirubin) + 1.120 * np.log(INR) + 0.6431)
st.write(f"### MELD Score: {MELD:.2f}")

# Calculate MELD-Na Score
if Na > 0:
    MELD_Na = MELD + (1.32 * (137 - Na)) - (0.033 * MELD * (137 - Na))
    st.write(f"### MELD-Na Score: {MELD_Na:.2f}")
else:
    st.write("### Additional Information Needed: Sodium cannot be zero for MELD-Na calculation.")
