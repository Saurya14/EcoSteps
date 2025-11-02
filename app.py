
import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Page config
st.set_page_config(page_title="EcoSteps — Personal Sustainability Tracker", layout="centered")

# --- Emission Factors (India) ---
CAR_KG = 0.12
ELECTRICITY_KG = 0.82
PLASTIC_ITEM_KG = 0.08
PUBLIC_TRANSPORT_SAVING = 0.10

# --- Theme control (simple) ---
theme_choice = st.sidebar.radio("Theme", ("Auto", "Light", "Dark"), index=0)
if theme_choice == "Dark":
    CARD_BG = "#1e293b"
    TEXT_COLOR = "#ffffff"
elif theme_choice == "Light":
    CARD_BG = "#f8fafc"
    TEXT_COLOR = "#000000"
else:
    CARD_BG = None
    TEXT_COLOR = None

st.markdown("<h1 style='text-align:center'>🌱 EcoSteps — Personal Sustainability Tracker (India)</h1>", unsafe_allow_html=True)
st.write("A simple, friendly calculator to estimate weekly CO₂ emissions and get quick suggestions to reduce your impact. Works well on mobile and desktop.")

# Sidebar inputs
st.sidebar.header("Your details & settings")
name = st.sidebar.text_input("Your name (optional)")
st.sidebar.caption("Tip: Leave name empty for anonymous results.")

st.sidebar.markdown("---")
st.sidebar.markdown("**Emission factors (India)**")
st.sidebar.write(f"Car: {CAR_KG} kg CO₂ / km • Electricity: {ELECTRICITY_KG} kg CO₂ / kWh")
st.sidebar.write(f"Plastic item: {PLASTIC_ITEM_KG} kg CO₂ • Public transport saving: {PUBLIC_TRANSPORT_SAVING} kg CO₂ / km")

st.markdown("## Tell us about your weekly habits")
cols = st.columns([1,1])

with cols[0]:
    car_km = st.number_input("1) Car kilometres per week", min_value=0.0, value=20.0, step=1.0)
    plastic_items = st.number_input("3) Single-use plastic items / week", min_value=0, value=5, step=1)
with cols[1]:
    electricity_kwh = st.number_input("2) Electricity (kWh) per month", min_value=0.0, value=120.0, step=1.0)
    public_km = st.number_input("4) km by public/active transport instead of car per week", min_value=0.0, value=5.0, step=1.0, help="Enter kilometres you travel by walking, cycling or public transport instead of private car (savings).")

st.markdown("----")

# Compute
weekly_electricity = electricity_kwh / 4.0
car_emission = car_km * CAR_KG
electricity_emission = weekly_electricity * ELECTRICITY_KG
plastic_emission = int(plastic_items) * PLASTIC_ITEM_KG
savings = public_km * PUBLIC_TRANSPORT_SAVING
total = car_emission + electricity_emission + plastic_emission - savings
if total < 0:
    total = 0.0

# Result card with color-coded badge
def colored_card(title, value, unit="kg CO₂/week", color="#10b981"):
    st.markdown(f"""
    <div style="background:{color}; padding:16px; border-radius:8px; color:white; box-shadow:0 2px 6px rgba(0,0,0,0.08)">
        <h3 style="margin:0">{title}</h3>
        <p style="font-size:20px; margin:4px 0 0 0"><strong>{value:.2f} {unit}</strong></p>
    </div>
    """, unsafe_allow_html=True)

st.subheader("Estimated weekly CO₂ footprint")
if total < 20:
    band_color = "#10b981"
    band_text = "Low"
elif total < 50:
    band_color = "#f59e0b"
    band_text = "Moderate"
else:
    band_color = "#ef4444"
    band_text = "High"

st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center'>", unsafe_allow_html=True)
st.markdown(f"<div style='flex:1'>", unsafe_allow_html=True)
st.markdown(f"<h2 style='margin:4px 0'>{name or 'User'}</h2>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown(f"<div style='width:200px'>", unsafe_allow_html=True)
colored_card(f"Status: {band_text}", total, unit="kg CO₂/week", color=band_color)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Breakdown
st.markdown("### Breakdown")
df = pd.DataFrame({
    "Category": ["Car (weekly)", "Electricity (weekly)", "Plastic (weekly)", "Savings (public/active)"],
    "kg CO₂/week": [round(car_emission,3), round(electricity_emission,3), round(plastic_emission,3), round(-savings,3)]
})
st.table(df)

# Progress indicator (relative scale)
max_scale = max(100, total*2)
progress_val = min(int((total/max_scale)*100), 100)
st.progress(progress_val)

# Suggestions
st.markdown("### Suggestions")
if total < 20:
    st.success("Great job! Your footprint is low. Keep these habits and encourage others.")
elif total < 50:
    st.info("Good effort — small changes can reduce your footprint further:")
    st.write("- Use energy-efficient appliances (LED lights, inverter AC settings)")
    st.write("- Replace single-use plastics with reusables")
    st.write("- Try a few car-free days or carpool")
else:
    st.warning("High footprint — recommended actions:")
    st.write("- Reduce private car kilometers (use public transport or carpool)")
    st.write("- Use AC efficiently; switch to energy-efficient appliances")
    st.write("- Avoid single-use plastics; carry reusable bottle & bags")
    st.write("- Consider green energy plans or rooftop solar if possible")

# Extra: equivalence
trees = total / 0.7
st.markdown(f"**Equivalence:** Your weekly emissions ≈ planting **{max(0,int(trees))}** young trees for a week (illustrative)")

# Download results
st.markdown("---")
st.markdown("### Save / Share your result")
result_dict = {
    "name": name or "",
    "car_km_per_week": car_km,
    "electricity_kwh_per_month": electricity_kwh,
    "plastic_items_per_week": int(plastic_items),
    "public_km_saved_per_week": public_km,
    "estimated_weekly_co2_kg": round(total,3),
    "timestamp": datetime.utcnow().isoformat()
}
results_df = pd.DataFrame([result_dict])
csv_buf = io.StringIO()
results_df.to_csv(csv_buf, index=False)
st.download_button("Download results as CSV", csv_buf.getvalue(), file_name="ecosteps_results.csv", mime="text/csv")

st.caption("Note: Estimates use coarse India-relevant factors and are intended for education only.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:gray'>Made with ❤️ — EcoSteps. Deploy on Streamlit Cloud for easy phone access.</div>", unsafe_allow_html=True)
