import streamlit as st
from PIL import Image, ImageStat
import numpy as np

st.set_page_config(layout="wide")

# -----------------------------
# HEADER
# -----------------------------
st.title("🐟 Fish Welfare Decision System")
st.caption("Inspection + Welfare Intelligence + Policy Output")

st.info("""
This tool is a **decision-support system** for evaluating fish welfare risk.

It combines:
- Biological factors (sentience)
- Farming system characteristics
- Environmental context
- Image-based observational signals

To generate:
→ A **transparent welfare risk score**
→ **Driver-level explanations**
→ **Targeted intervention recommendations**

This is an early-stage semi-empirical model designed for inspection, policy, and strategy use.
""")

with st.expander("ℹ️ How the system works"):
    st.write("""
Risk = Severity × System Factors × Sentience × Scenario Fit

- Severity = weighted welfare risks (density, water, slaughter, disease)
- System Factors = production intensity and maturity
- Sentience = species-specific capacity for suffering
- Scenario Fit = realism of species-geography combination

Drivers are derived from:
- Context inputs
- System configuration
- Image-based signals (if uploaded)

Output is a relative welfare risk score (0–10)
""")

# -----------------------------
# INPUTS
# -----------------------------
st.subheader("📍 Context")

species = st.selectbox("Species", ["Carp","Tilapia","Salmon","Shrimp"],
    help="Determines biological sensitivity and sentience")

geo = st.selectbox("Geography", ["India","Nigeria","Vietnam","Bangladesh","EU"],
    help="Affects baseline environmental risks")

system_type = st.selectbox("Production System", ["Extensive","Semi-Intensive","Intensive"],
    help="Higher intensity increases density and stress")

slaughter_method = st.selectbox("Slaughter Method",
    ["Asphyxiation (Air)", "Ice Slurry", "Electrical Stunning"],
    help="Major determinant of suffering")

target_actor = st.selectbox(
    "Target Actor",
    ["NGO","Policymaker","Corporate","Finance","Animal Welfare","Environment"]
)

stage = st.selectbox("System Stage", ["Emerging","Growing","Mature"])
dev_finance = st.selectbox("Development Finance", ["Low","Medium","High"])
confidence = st.selectbox("Sentience Confidence", ["Low","Medium","High"])

# -----------------------------
# SCENARIO
# -----------------------------
st.subheader("🌍 Scenario Check")

mismatch_penalty = 0

if species == "Salmon" and geo in ["India","Bangladesh"]:
    st.warning("⚠ Mismatch: Salmon rare here")
    mismatch_penalty = 0.3
else:
    st.success("✔ Scenario realistic")

# -----------------------------
# SENTIENCE
# -----------------------------
sentience_map = {"Carp":0.5,"Tilapia":0.6,"Salmon":0.85,"Shrimp":0.3}
conf_map = {"Low":0.5,"Medium":0.75,"High":1}

sentience = sentience_map[species] * conf_map[confidence]

st.subheader("🧠 Sentience")
st.write(f"Effective sentience: {round(sentience,2)}")

# -----------------------------
# SCORES
# -----------------------------
explanations = {}

disease_base = 2 if system_type == "Extensive" else 3 if system_type == "Semi-Intensive" else 4

scores = {
    "Stocking Density": {
        "value": 2 if system_type=="Extensive" else 3 if system_type=="Semi-Intensive" else 4,
        "weight": 0.25,
        "confidence": 0.7
    },
    "Water Quality": {
        "value": 3 if geo=="India" else 2,
        "weight": 0.3,
        "confidence": 0.8
    },
    "Slaughter": {
        "value": 5 if slaughter_method=="Asphyxiation (Air)" else 3,
        "weight": 0.3,
        "confidence": 1
    },
    "Disease": {
        "value": disease_base,
        "weight": 0.15,
        "confidence": 0.6
    }
}

explanations["Stocking Density"] = f"Derived from system type: {system_type}"
explanations["Water Quality"] = f"Baseline from geography: {geo}"
explanations["Slaughter"] = f"Derived from method: {slaughter_method}"
explanations["Disease"] = f"Derived from system intensity: {system_type}"

# -----------------------------
# IMAGE INPUT
# -----------------------------
st.subheader("📸 Image (Optional)")

img_file = st.file_uploader("Upload", type=["jpg","png"])
image_effects = []

if img_file:
    img = Image.open(img_file)
    st.image(img, width=200)

    stat = ImageStat.Stat(img)
    brightness = np.mean(stat.mean)
    contrast = np.std(stat.mean)

    img_array = np.array(img)
    variation = np.std(img_array)
    avg_color = np.mean(img_array, axis=(0,1))

    st.caption(f"Brightness: {round(brightness,1)} | Contrast: {round(contrast,1)} | Variation: {round(variation,1)}")

    if brightness < 40:
        scores["Water Quality"]["value"] += 1
        explanations["Water Quality"] += " + turbidity signal"
        image_effects.append("Water Quality ↑")

    if contrast < 20:
        scores["Disease"]["value"] += 1
        explanations["Disease"] += " + stress/disease signal"
        image_effects.append("Disease ↑")

    if variation < 50:
        scores["Stocking Density"]["value"] += 1
        explanations["Stocking Density"] += " + crowding signal"
        image_effects.append("Density ↑")

    st.subheader("🧠 Image Insight (Experimental)")

    if avg_color[0] > avg_color[2]:
        st.info("Likely environment: sediment-heavy / inland system (carp/tilapia typical)")
    elif avg_color[2] > avg_color[0]:
        st.info("Likely environment: clearer/open water (possible marine or controlled system)")

    st.warning("Image-based signals are low-confidence and should be validated with field data")

# -----------------------------
# RISK
# -----------------------------
weighted_sum = sum(v["value"] * v["weight"] * v["confidence"] for v in scores.values())

scale = {"Extensive":1,"Semi-Intensive":1.3,"Intensive":1.6}[system_type]
persistence = {"Emerging":0.8,"Growing":1,"Mature":1.3}[stage]

if dev_finance == "High":
    scale += 0.3

risk = weighted_sum * scale * persistence * (1 + sentience)
risk *= (1 + mismatch_penalty)

if scores["Slaughter"]["value"] >= 5:
    risk = max(risk, 5)

risk = round(min(10, risk),2)

# -----------------------------
# OUTPUT
# -----------------------------
st.subheader("📊 Welfare Intelligence")

st.metric("Risk Score", risk)
st.progress(risk/10)

# -----------------------------
# CONTRIBUTION
# -----------------------------
st.subheader("📊 Contribution to Risk")

for k, v in scores.items():
    contrib = v["value"] * v["weight"]
    st.write(f"{k}: {round(contrib,2)}")

# -----------------------------
# CONFIDENCE
# -----------------------------
avg_conf = np.mean([v["confidence"] for v in scores.values()])
st.subheader("⚖️ Confidence in Assessment")
st.write(f"Overall confidence: {round(avg_conf,2)}")

# -----------------------------
# IMAGE IMPACT
# -----------------------------
if img_file:
    st.subheader("🧾 Image Impact")
    st.write("Drivers affected by image:")
    for e in image_effects:
        st.write(f"- {e}")

# -----------------------------
# DRIVERS
# -----------------------------
st.subheader("🔍 Risk Drivers")

for k, v in scores.items():
    st.write(f"**{k}** → {v['value']}")
    st.caption(explanations[k])

# -----------------------------
# SIMULATOR
# -----------------------------
st.subheader("🔁 Intervention Simulator")

improve_slaughter = st.checkbox("Apply humane slaughter")
reduce_density = st.checkbox("Reduce stocking density")

sim_scores = {k: v.copy() for k, v in scores.items()}

if improve_slaughter:
    sim_scores["Slaughter"]["value"] = 2

if reduce_density:
    sim_scores["Stocking Density"]["value"] = max(1, sim_scores["Stocking Density"]["value"] - 1)

new_weighted = sum(v["value"] * v["weight"] * v["confidence"] for v in sim_scores.values())
new_risk = new_weighted * scale * persistence * (1 + sentience)
new_risk = round(min(10, new_risk),2)

st.write(f"New Risk Score: {new_risk}")

impact = (risk - new_risk) / risk if risk > 0 else 0
st.write(f"Impact: {round(impact*100,1)}% risk reduction")

# -----------------------------
# DECISION
# -----------------------------
st.subheader("🧠 Decision Recommendation")

if risk > 7:
    st.write("Immediate intervention required")
elif risk > 4:
    st.write("Targeted improvements recommended")
else:
    st.write("Monitor system, no urgent intervention")

# -----------------------------
# REPORT
# -----------------------------
st.subheader("📄 Welfare Report Summary")

top = sorted(scores.items(), key=lambda x: x[1]["value"], reverse=True)

st.write(f"**Risk Score:** {risk}")
st.write(f"**Priority Intervention Area:** {top[0][0]}")

# -----------------------------
# POLICY
# -----------------------------
st.subheader("🏛️ Policy Output")

if target_actor == "NGO":
    if scores["Slaughter"]["value"] > 4:
        st.write("• Campaign against inhumane slaughter")

    if scores["Disease"]["value"] > 3:
        st.write("• Highlight suffering in intensive systems")

    if scores["Stocking Density"]["value"] > 3:
        st.write("• Advocate density reforms")

    st.write("• Build public pressure")
    st.write("• Engage retailers")
