import streamlit as st

# Function to calculate A-a gradient
def calculate_a_gradient(PaO2, FiO2):
    # Adjust the FiO2 to be a fraction
    if FiO2 > 1:
        FiO2 /= 100
    PAO2 = (FiO2 * 760) - (PaO2 / 0.8)  # Approximation of PAO2
    return PAO2 - PaO2

# Function to calculate Winter's formula
def winters_formula(HCO3):
    return (HCO3 * 1.5) + 8

# Streamlit app layout
st.title("A-a Gradient and Winter's Formula Calculator")

# Input fields
PaO2 = st.number_input("Enter PaO2 (mmHg)", min_value=0.0)
FiO2 = st.number_input("Enter FiO2 (%)", min_value=0.0, max_value=100.0)
SpO2 = st.number_input("Enter SpO2 (%)", min_value=0.0, max_value=100.0)
SaO2 = st.number_input("Enter SaO2 (%)", min_value=0.0, max_value=100.0)
HCO3 = st.number_input("Enter HCO3 (mEq/L)", min_value=0.0)
pH = st.number_input("Enter pH", min_value=0.0, max_value=14.0)

# Calculate results
if st.button("Calculate"):
    a_gradient = calculate_a_gradient(PaO2, FiO2)
    winters_result = winters_formula(HCO3)

    # Display results
    st.write(f"A-a Gradient: {a_gradient:.2f} mmHg")
    st.write(f"Winter's Formula Result: {winters_result:.2f} mmHg")



