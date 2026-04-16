import streamlit as st
from PIL import Image, ImageStat
import numpy as np

st.set_page_config(layout="wide")

# =============================
# EVIDENCE LAYER
# =============================

EVIDENCE_DB = {
    "Water Quality": {
        "description": "Water conditions affect oxygen levels, ammonia toxicity, and physiological stress.",
        "why": "Poor water quality is a primary cause of chronic stress and mortality.",
        "intervention": "Improve filtration, aeration, and water exchange systems.",
        "sources": ["FAO Aquaculture Guidelines", "Boyd (2015)"]
    },
    "Stocking Density": {
        "description": "Crowding increases stress and injury.",
        "why": "High density reduces oxygen and increases aggression and disease.",
        "intervention": "Reduce stocking density.",
        "sources": ["FAO Reports", "Ashley (2007)"]
    },
    "Slaughter": {
        "description": "Determines intensity of death-related suffering.",
        "why": "Asphyxiation causes prolonged distress.",
        "intervention": "Use electrical stunning.",
        "sources": ["EFSA (2009)", "Humane Slaughter Association"]
    },
    "Disease": {
        "description": "Represents infection pressure.",
        "why": "Poor hygiene increases pathogen load.",
        "intervention": "Improve hygiene and biosecurity.",
        "sources": ["FAO Fish Health", "WOAH"]
    }
}

# =============================
# BASELINE
# =============================

BASELINE = {
    "geography": {"India": {"Water Quality": +1}},
    "system_type": {"Intensive": {"Stocking Density": +1, "Disease": +1}},
    "species": {"Shrimp": {"Disease": +1}}
}

def apply_baseline(scores, geo, system_type, species):
    for layer, key in [("geography", geo), ("system_type", system_type), ("species", species)]:
        if key in BASELINE[layer]:
            for driver, adj in BASELINE[layer][key].items():
                scores[driver]["value"] = min(5, max(1, scores[driver]["value"] + adj))
    return scores

# =============================
# POLICY INTELLIGENCE
# =============================

POLICY_DB = {
    "NGO": {
        "Slaughter": {
            "title": "End-of-life welfare failure",
            "problem": ["Prolonged distress", "Preventable harm"],
            "actions": ["Advocate stunning", "Target processors", "Public campaigns"]
        },
        "Water Quality": {
            "title": "Water quality constraint",
            "problem": ["Chronic stress"],
            "actions": ["Farmer training", "Push regulation"]
        }
    }
}

def render_policy_intelligence(target_actor, scores, top_driver):
    st.subheader("🏛️ Policy Intelligence")
    actor_policies = POLICY_DB.get(target_actor, {})

    if top_driver in actor_policies:
        policy = actor_policies[top_driver]
        st.write(f"**{policy['title']}**")
        for p in policy["problem"]:
            st.write(f"- {p}")
        for a in policy["actions"]:
            st.write(f"→ {a}")

# =============================
# ACTOR STRATEGY (NEW)
# =============================

def render_actor_strategy(target_actor, top_driver, final_risk):
    st.subheader("🧭 Why this matters")

    if target_actor == "NGO":
        st.write(f"""
- High-leverage intervention targeting **{top_driver}**
- Severe but preventable harm
→ Strong campaign potential
""")

# =============================
# CORE LOGIC
# =============================

def compute_sentience(species, confidence):
    return {"Carp":0.5,"Tilapia":0.6,"Salmon":0.85,"Shrimp":0.3}[species] * {"Low":0.5,"Medium":0.75,"High":1}[confidence]

def build_scores(density, water, slaughter, disease):
    return {
        "Stocking Density":{"value":density,"weight":0.25,"confidence":0.7},
        "Water Quality":{"value":water,"weight":0.3,"confidence":0.8},
        "Slaughter":{"value":slaughter,"weight":0.3,"confidence":1},
        "Disease":{"value":disease,"weight":0.15,"confidence":0.6}
    }

def compute_risk(scores, system_type, stage, sentience):
    weighted = sum(v["value"] * v["weight"] * v["confidence"] for v in scores.values())
    scale = {"Extensive":1,"Semi-Intensive":1.3,"Intensive":1.6}[system_type]
    stage_factor = {"Emerging":0.8,"Growing":1,"Mature":1.3}[stage]
    risk = weighted * scale * stage_factor * (1 + 1.5 * sentience)

    if scores["Slaughter"]["value"] >= 5:
        risk = max(risk, weighted * 0.8 + 2)

    return round(min(10, risk),2), weighted, scale, stage_factor

def compute_confidence(scores, mismatch_flag):

    confidence_score = np.mean([v["confidence"] for v in scores.values()])

    # Reduce confidence if scenario mismatch
    if mismatch_flag:
        confidence_score *= 0.8

    confidence_score = round(confidence_score, 2)

    if confidence_score > 0.75:
        label = "High"
    elif confidence_score > 0.5:
        label = "Moderate"
    else:
        label = "Low"

    return confidence_score, label

# =============================
# SIMULATION LAYER
# =============================

def simulate_intervention(scores, system_type, stage, sentience):

    sim_scores = {k: v.copy() for k, v in scores.items()}

    reduce_density = st.checkbox("Reduce stocking density")
    improve_water = st.checkbox("Improve water quality")
    stun_slaughter = st.checkbox("Use electrical stunning")

    if reduce_density:
        sim_scores["Stocking Density"]["value"] = max(1, sim_scores["Stocking Density"]["value"] - 1)

    if improve_water:
        sim_scores["Water Quality"]["value"] = max(1, sim_scores["Water Quality"]["value"] - 1)

    if stun_slaughter:
        sim_scores["Slaughter"]["value"] = 2

    new_risk, _, _, _ = compute_risk(sim_scores, system_type, stage, sentience)

    return new_risk, reduce_density, improve_water, stun_slaughter

# =============================
# ADVOCACY LAYER
# =============================

def render_advocacy(target_actor, top_driver, final_risk):

    st.subheader("📢 Advocacy Framing")

    if final_risk >= 6:
        risk_level = "High"
    elif final_risk >= 3:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    st.write(f"{risk_level} risk driven by **{top_driver}**.")

    if target_actor == "NGO":
        st.write("""
→ Focus on preventable suffering  
→ Highlight scale and invisibility of fish suffering  
→ Use clear villains (e.g. slaughter practices)  
→ Combine campaigns with corporate pressure  
""")

    elif target_actor == "Corporate":
        st.write("""
→ Frame as operational + reputational risk  
→ Link welfare to efficiency and product quality  
→ Emphasize future regulation and buyer expectations  
""")

    elif target_actor == "Finance":
        st.write("""
→ Frame as ESG and regulatory exposure  
→ Highlight risk shocks  
→ Position welfare as long-term risk  
""")

    elif target_actor == "Policymaker":
        st.write("""
→ Frame as regulatory gap  
→ Link welfare to environment and public interest  
→ Emphasize system-wide impact  
""")

# =============================
# IMAGE INPUT LAYER
# =============================

def process_image(img_file, scores):

    image_flag = False

    if img_file is not None:
        img = Image.open(img_file)
        st.image(img, width=250)

        stat = ImageStat.Stat(img)
        brightness = np.mean(stat.mean)
        contrast = np.std(stat.mean)

        # Simple heuristics (transparent, not black-box)
        if brightness < 40:
            scores["Water Quality"]["value"] = min(5, scores["Water Quality"]["value"] + 1)

        if contrast < 20:
            scores["Disease"]["value"] = min(5, scores["Disease"]["value"] + 1)

        # Low-quality image reduces confidence
        if brightness < 30 or contrast < 10:
            image_flag = True
            st.warning("⚠️ Low-quality image — results less reliable")

    return scores, image_flag

# =============================
# UI
# =============================

st.title("🐟 Fish Welfare Decision System")

st.markdown("### 📚 How this tool works")

# =============================
# DATA & METHOD
# =============================

with st.expander("📊 Data & Method (What this tool is based on)"):
    st.write("""
This tool combines three types of inputs:

**1. Scientific Evidence Base**
- FAO aquaculture guidelines
- EFSA fish welfare reports
- WOAH animal health standards
- Academic welfare literature

**2. Structured Welfare Model**
- Four core drivers: Density, Water, Slaughter, Disease
- Each scored (1–5), weighted, and combined
- Adjusted for system type and geography

**3. Empirical Inputs (User + Context)**
- User-provided scores
- Optional farm images (visual indicators of water quality and disease risk)
- Scenario validation (species × geography)

This is a **decision-support model**, not a predictive AI system.
It is designed for:
→ Transparency  
→ Explainability  
→ Policy and advocacy use
""")

with st.expander("Click to understand the model"):
    st.write("""
This tool estimates **fish welfare risk** using four key drivers:

- Stocking Density  
- Water Quality  
- Slaughter Practices  
- Disease Risk  

Each driver is:
- Scored (1–5)
- Weighted based on welfare importance
- Adjusted for system type and geography

The model also includes:
- A **sentience multiplier** (higher sentience = higher moral weight)
- A **system scale factor** (intensive systems increase risk)
- A **stage factor** (mature systems amplify impact)

The goal is to:
→ Identify the **highest-impact welfare problem**  
→ Recommend **targeted interventions**
""")

st.subheader("📍 Context")

species = st.selectbox(
    "Species",
    ["Carp","Tilapia","Salmon","Shrimp"],
    help="Species determines baseline sentience and biological sensitivity."
)

geo = st.selectbox(
    "Geography",
    ["India","Nigeria","Vietnam","Bangladesh","EU"],
    help="Geography affects baseline risks like water quality and regulatory conditions."
)

system_type = st.selectbox(
    "Production System",
    ["Extensive","Semi-Intensive","Intensive"],
    help="More intensive systems typically increase density, disease risk, and stress."
)

target_actor = st.selectbox(
    "Target Actor",
    ["NGO","Corporate","Finance","Policymaker"],
    help="Determines the type of intervention strategy generated."
)

stage = st.selectbox(
    "System Stage",
    ["Emerging","Growing","Mature"],
    help="Mature systems have larger scale and higher cumulative welfare impact."
)

confidence = st.selectbox(
    "Sentience Confidence",
    ["Low","Medium","High"],
    help="Reflects scientific certainty about the species' capacity to feel pain. Lower confidence = more uncertainty in sentience estimates."
)

# =============================
# SCENARIO CHECK
# =============================

mismatch_flag = False
if species == "Salmon" and geo in ["India","Bangladesh","Nigeria"]:
    st.warning("⚠️ Scenario mismatch: Salmon farming uncommon in this geography")
    mismatch_flag = True

sentience = compute_sentience(species, confidence)

st.subheader("🧠 Sentience")

st.write(f"Effective sentience: {round(sentience,2)}")

with st.expander("What does this mean?"):
    st.write("""
Sentience reflects an animal's capacity to feel pain and suffering.

Approximate comparison:
- Shrimp: ~0.3  
- Carp: ~0.5  
- Tilapia: ~0.6  
- Salmon: ~0.85  
- Mammals (e.g. pigs): ~0.9+

This tool adjusts welfare risk based on sentience:
→ Higher sentience = higher moral weight of suffering

Sentience confidence reflects how certain science is about these estimates:
- Low → limited or debated evidence  
- Medium → growing but incomplete evidence  
- High → strong scientific consensus  
""")

# DRIVERS
st.subheader("🔧 Welfare Drivers")

st.caption("Low (more space) ← → High (crowding)")
density = st.slider(
    "Stocking Density", 1, 5, 2,
    help=EVIDENCE_DB["Stocking Density"]["description"]
)
st.caption("Good quality ← → Poor quality")
water = st.slider(
    "Water Quality", 1, 5, 3,
    help=EVIDENCE_DB["Water Quality"]["description"]
)
st.caption("Humane (stunned) ← → Severe (asphyxiation)")
slaughter = st.slider(
    "Slaughter Severity", 1, 5, 5,
    help=EVIDENCE_DB["Slaughter"]["description"]
)
st.caption("Low infection risk ← → High infection risk")
disease = st.slider(
    "Disease Risk", 1, 5, 2,
    help=EVIDENCE_DB["Disease"]["description"]
)

scores = apply_baseline(build_scores(density, water, slaughter, disease), geo, system_type, species)

# =============================
# IMAGE INPUT
# =============================

st.subheader("📷 Evidence Input (Optional)")

st.info("""
Upload 2–5 images of the farm for better assessment.

Guidelines:
- Show water surface clearly
- Capture fish density (crowding)
- Ensure good lighting (avoid dark/blurred images)
- Include feeding or active zones if possible

Images are used as supporting evidence and improve confidence in future versions.
""")
img_file = st.file_uploader("Upload farm image", type=["jpg","png","jpeg"])

scores, image_flag = process_image(img_file, scores)

# RISK
final_risk, weighted, scale, stage_factor = compute_risk(scores, system_type, stage, sentience)

st.subheader("📊 Welfare Risk")
st.metric("Welfare Risk Score", final_risk)

# =============================
# DRIVER CONTRIBUTION
# =============================

st.subheader("📊 Driver Contribution (%)")

total = sum(v["value"] * v["weight"] for v in scores.values())

for k, v in scores.items():
    contrib = (v["value"] * v["weight"]) / total if total else 0
    st.write(f"{k}: {round(contrib * 100, 1)}%")
# DRIVER EXPLAINER
st.subheader("📚 Driver Evidence")
for k,v in scores.items():
    st.write(f"**{k} (Score: {v['value']})**")
    ev = EVIDENCE_DB[k]
    st.write(f"What: {ev['description']}")
    st.write(f"Why: {ev['why']}")
    st.write(f"Intervention: {ev['intervention']}")
    for src in ev["sources"]:
        st.caption(f"- {src}")

# TOP DRIVER
top_driver = max(scores, key=lambda k: scores[k]["value"])

# POLICY + STRATEGY
render_policy_intelligence(target_actor, scores, top_driver)
render_actor_strategy(target_actor, top_driver, final_risk)
render_advocacy(target_actor, top_driver, final_risk)

# =============================
# INTERVENTION SIMULATOR
# =============================

st.subheader("🔁 Intervention Simulation")
st.caption("Select an intervention to see how welfare risk changes")

new_risk, reduce_density, improve_water, stun_slaughter = simulate_intervention(
    scores, system_type, stage, sentience
)

st.write(f"New Welfare Risk: {new_risk}")

if final_risk > 0:
    impact = round((final_risk - new_risk) / final_risk * 100, 1)
    st.write(f"Impact: {impact}% reduction")

if stun_slaughter and scores["Slaughter"]["value"] >= 4:
    st.caption("Major impact driven by improving slaughter practices")

if improve_water:
    st.caption("Moderate impact from improving water conditions")

if reduce_density:
    st.caption("Incremental improvement from reducing density")

# TRANSPARENCY
st.subheader("🔬 Calculation")
st.write(f"Weighted score: {round(weighted,2)} | Scale: {scale} | Stage: {stage_factor}")

# CONFIDENCE
confidence_score, label = compute_confidence(
    scores,
    mismatch_flag or ('image_flag' in locals() and image_flag)
)
st.subheader("📉 Confidence")

st.caption("""
What affects confidence?
- Quality of input data (slider assumptions)
- Availability of evidence
- Scenario realism (species × geography)
- Presence of supporting images
""")

st.write(f"Confidence: **{confidence_score} ({label})**")

if mismatch_flag:
    st.caption("⚠ Reduced confidence due to scenario mismatch")

with st.expander("What affects confidence?"):
    st.write("""
Confidence depends on:
- Data quality of each welfare driver
- Strength of scientific evidence
- Scenario realism (species × geography)

Lower confidence does NOT mean low risk  
→ It means more uncertainty in the estimate
""")
