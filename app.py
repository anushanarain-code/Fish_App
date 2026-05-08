# -*- coding: utf-8 -*-
import streamlit as st
from PIL import Image, ImageStat
import numpy as np
import altair as alt
import pandas as pd

st.set_page_config(layout="wide")
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}
div[data-testid="stMetric"] {
    padding: 5px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# EVIDENCE LAYER
# =============================

EVIDENCE_DB = {
    "Water Quality": {
        "description": "Water conditions affect oxygen levels, ammonia toxicity, and physiological stress.",
        "why": "Poor water quality is a primary cause of chronic stress and mortality.",
        "intervention": "Improve filtration, aeration, and water exchange systems.",
        "sources": [("FAO Aquaculture Guidelines", "https://www.fao.org/fishery/en"),
        ("Boyd (2015) - Water Quality", "https://doi.org/10.1016/j.aquaculture.2015.02.001")]
    },
    "Stocking Density": {
        "description": "Crowding increases stress and injury.",
        "why": "High density reduces oxygen and increases aggression and disease.",
        "intervention": "Reduce stocking density.",
        "sources": [("FAO Reports", "https://www.fao.org/fishery/en"),
        ("Ashley (2007)", "https://doi.org/10.1016/j.applanim.2006.09.002")]
    },
    "Slaughter": {
        "description": "Determines intensity of death-related suffering.",
        "why": "Asphyxiation causes prolonged distress.",
        "intervention": "Use electrical stunning.",
        "sources": [("EFSA (2009)", "https://www.efsa.europa.eu/en/efsajournal/pub/1010"),
        ("Humane Slaughter Association", "https://www.hsa.org.uk/fish-slaughter")]
    },
    "Disease": {
        "description": "Represents infection pressure.",
        "why": "Poor hygiene increases pathogen load.",
        "intervention": "Improve hygiene and biosecurity.",
        "sources": [("FAO Fish Health", "https://www.fao.org/fishery/en"),
        ("WOAH Aquatic Animal Health Code", "https://www.woah.org/en/what-we-do/standards/codes-and-manuals/aquatic-code/")]
    }
}

# =============================
# BASELINE DATASET LAYER (V3)
# =============================

BASELINE_DATA = {

    "geography": {

        "India": {
            "water_quality_base": 3.5,
            "disease_pressure": 3.2
        },

        "Bangladesh": {
            "water_quality_base": 3.8,
            "disease_pressure": 3.6
        },

        "Vietnam": {
            "water_quality_base": 3.0,
            "disease_pressure": 3.0
        },

        "EU": {
            "water_quality_base": 2.0,
            "disease_pressure": 2.0
        },

        "Nigeria": {
            "water_quality_base": 3.7,
            "disease_pressure": 3.5
        }
    },

    "system_type": {

        "Extensive": {
            "stocking_density_base": 2.0,
            "water_adjust": -0.3
        },

        "Semi-Intensive": {
            "stocking_density_base": 3.0,
            "water_adjust": 0.0
        },

        "Intensive": {
            "stocking_density_base": 4.2,
            "water_adjust": +0.6
        }
    },

    "species": {

        "Carp": {"sentience": 0.5},
        "Tilapia": {"sentience": 0.6},
        "Salmon": {"sentience": 0.85},
        "Shrimp": {"sentience": 0.3}
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

    geo_data = BASELINE_DATA["geography"].get(geo, {})
    sys_data = BASELINE_DATA["system_type"].get(system_type, {})

    # Only apply adjustments, NOT overwrite user-adjusted values

    # Water adjustment from system type
    if "water_adjust" in sys_data:
        scores["Water Quality"]["value"] = min(
            5,
            max(1, scores["Water Quality"]["value"] + sys_data["water_adjust"])
        )

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

def render_policy_intelligence(target_actor, scores, top_driver, geo, system_type):

    # =============================
    # SLAUGHTER
    # =============================
    if top_driver == "Slaughter":

        st.write("**System failure:** Absence of enforceable humane slaughter standards")

        st.markdown("**Non-obvious policy leverage:**")

        if geo == "India":
            st.write("""
In India, humane slaughter practices such as electrical stunning are not widely implemented.

However, integrating such methods into existing regulatory frameworks—such as food safety audits or export certification systems—can significantly reduce acute welfare harm without requiring new legislation.
""")

        else:
            st.write("""
In many countries, humane slaughter practices such as electrical stunning remain weakly implemented.

Embedding welfare requirements into existing certification and compliance systems can substantially reduce acute suffering.
""")

        st.markdown("**Strategic constraint:**")
        st.write("""
Slaughter often occurs outside formal processing infrastructure,
which reduces the effectiveness of direct regulatory enforcement.
""")

        st.markdown("**Actor-specific pathway:**")

        if target_actor == "NGO":
            st.write("""
NGOs can prioritise retailer and processor campaigns to create commercial pressure for humane slaughter adoption.
""")

        elif target_actor == "Policymaker":
            st.write("""
Policymakers can integrate humane slaughter requirements into food safety audits and export compliance systems.
""")

        elif target_actor == "Corporate":
            st.write("""
Corporate actors can incorporate stunning requirements into supplier standards and procurement policies.
""")

        elif target_actor == "Finance":
            st.write("""
Investors can integrate slaughter practices into ESG engagement and supply chain risk assessment frameworks.
""")

    # =============================
    # WATER QUALITY
    # =============================
    elif top_driver == "Water Quality":

        st.write("**System failure:** Weak environmental monitoring and water management")

        st.markdown("**Non-obvious policy leverage:**")

        if geo == "India":
            st.write("""
Low-cost interventions such as aeration and water exchange can significantly reduce chronic stress and mortality.

Framing welfare improvements as productivity gains increases adoption incentives.
""")
        else:
            st.write("""
Strengthening monitoring systems and environmental compliance standards can improve welfare outcomes at scale.
""")

        st.markdown("**Strategic constraint:**")
        st.write("""
Farmers often operate under infrastructure and cost limitations,
which reduces uptake of welfare-specific interventions.
""")

        st.markdown("**Actor-specific pathway:**")

        if target_actor == "NGO":
            st.write("""
NGOs can support farmer training programs and demonstrate productivity-linked welfare improvements.
""")

        elif target_actor == "Policymaker":
            st.write("""
Policymakers can strengthen water quality standards and monitoring requirements.
""")

        elif target_actor == "Corporate":
            st.write("""
Corporate actors can require environmental monitoring within supplier standards.
""")

        elif target_actor == "Finance":
            st.write("""
Investors can prioritise infrastructure upgrades linked to environmental risk reduction.
""")

    # =============================
    # STOCKING DENSITY
    # =============================
    elif top_driver == "Stocking Density":

        st.write("**System failure:** Absence of enforceable stocking density standards")

        st.markdown("**Non-obvious policy leverage:**")

        st.write("""
Market-based enforcement mechanisms may be more scalable than direct regulation in controlling stocking density.
""")

        st.markdown("**Strategic constraint:**")
        st.write("""
Production incentives favour high-density farming because it increases short-term output.
""")

        st.markdown("**Actor-specific pathway:**")

        if target_actor == "NGO":
            st.write("""
NGOs can pressure certification systems and retailers to adopt density-based welfare standards.
""")

        elif target_actor == "Policymaker":
            st.write("""
Policymakers can introduce density guidance through aquaculture licensing frameworks.
""")

        elif target_actor == "Corporate":
            st.write("""
Corporate actors can integrate stocking density thresholds into supplier requirements.
""")

        elif target_actor == "Finance":
            st.write("""
Investors can assess long-term biological and reputational risks associated with high-density systems.
""")

    # =============================
    # DISEASE
    # =============================
    elif top_driver == "Disease":

        st.write("**System failure:** Weak biosecurity coordination and disease surveillance")

        st.markdown("**Non-obvious policy leverage:**")

        st.write("""
Disease control is most effective when implemented at the cluster or regional level rather than individual farms.
""")

        st.markdown("**Strategic constraint:**")
        st.write("""
Fragmented monitoring systems reduce early detection and coordinated response capacity.
""")

        st.markdown("**Actor-specific pathway:**")

        if target_actor == "NGO":
            st.write("""
NGOs can support regional training and biosecurity awareness initiatives.
""")

        elif target_actor == "Policymaker":
            st.write("""
Policymakers can strengthen veterinary surveillance and national reporting systems.
""")

        elif target_actor == "Corporate":
            st.write("""
Corporate actors can standardise farm-level biosecurity protocols across suppliers.
""")

        elif target_actor == "Finance":
            st.write("""
Investors can evaluate disease resilience as part of operational risk assessment.
""")

# =============================
# CORE LOGIC
# =============================

def get_top_driver(scores):
    ranked = sorted(
        scores.items(),
        key=lambda x: x[1]["value"] * x[1]["weight"] * x[1]["confidence"],
        reverse=True
    )
    return ranked[0][0], ranked

# =============================
# SCENARIO MISMATCH ENGINE (V3)
# =============================

def detect_mismatch(species, geo, system_type):

    issues = []

    # Species x Geography mismatch
    if species == "Salmon" and geo in ["India","Bangladesh","Nigeria"]:
        issues.append("Salmon farming is uncommon in this geography")

    # System x Geography mismatch
    if geo in ["India","Bangladesh"] and system_type == "Intensive":
        issues.append("Highly intensive systems may be less common or poorly regulated in this region")

    # Logical mismatch example
    if species == "Shrimp" and system_type == "Extensive":
        issues.append("Shrimp farming is often semi-intensive or intensive")

    return issues

def compute_sentience(species, confidence):
    return {"Carp":0.5,"Tilapia":0.6,"Salmon":0.85,"Shrimp":0.3}[species] * {"Low":0.5,"Medium":0.75,"High":1}[confidence]

def apply_deviation(base_value, delta):
    """
    Converts deviation input into bounded score (1-5)
    """
    return min(5, max(1, base_value + delta))

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

def apply_interactions(scores):
    """
    Adjust scores based on interaction effects between drivers
    """

    # Copy to avoid mutating original directly
    adjusted = {k: v.copy() for k, v in scores.items()}

    density = adjusted["Stocking Density"]["value"]
    water = adjusted["Water Quality"]["value"]
    disease = adjusted["Disease"]["value"]

    # 1. Density x Disease interaction
    if density >= 4 and disease >= 4:
        adjusted["Disease"]["value"] = min(5, disease + 0.5)

    # 2. Water x All (system stress multiplier)
    if water >= 4:
        for k in ["Stocking Density", "Disease"]:
            adjusted[k]["value"] = min(5, adjusted[k]["value"] + 0.3)

    # 3. Extreme suffering override (Slaughter dominates)
    if adjusted["Slaughter"]["value"] == 5:
        for k in adjusted:
            adjusted[k]["confidence"] *= 1.1

    return adjusted

def compute_driver_impact(scores, system_type, stage, sentience):
    """
    Computes true contribution of each driver to final risk
    (aligned with full model, not just raw weights)
    """

    scale = {"Extensive":1,"Semi-Intensive":1.3,"Intensive":1.6}[system_type]
    stage_factor = {"Emerging":0.8,"Growing":1,"Mature":1.3}[stage]
    sentience_factor = (1 + 1.5 * sentience)

    impact_scores = {}

    for k, v in scores.items():
        impact_scores[k] = (
            v["value"] *
            v["weight"] *
            v["confidence"] *
            scale *
            stage_factor *
            sentience_factor
        )

    return impact_scores

def compute_confidence(scores, mismatch_flag, image_uploaded, num_images=0):

    # 1. Base confidence
    base_conf = np.mean([v["confidence"] for v in scores.values()])

    # 2. Mismatch penalty
    mismatch_penalty = 0.15 if mismatch_flag else 0

    # 3. Extreme + deviation penalty (IMPROVED)
    extreme_count = sum(1 for v in scores.values() if v["value"] in [1,5])

    # Penalise extreme values more strongly
    extreme_penalty = 0.06 * extreme_count

    # Additional penalty for high deviation from mid-range (uncertainty proxy)
    deviation_penalty = sum(abs(v["value"] - 3) for v in scores.values()) * 0.01

    # 4. Image bonus (scaled)
    if num_images >= 3:
        image_bonus = 0.15
    elif num_images > 0:
        image_bonus = 0.08
    else:
        image_bonus = 0

    final_conf = base_conf - mismatch_penalty - extreme_penalty - deviation_penalty + image_bonus

    return round(max(0, min(1, final_conf)), 2)

    
# =============================
# SIMULATION LAYER
# =============================

def simulate_intervention(scores, system_type, stage, sentience):

    sim_scores = {k: v.copy() for k, v in scores.items()}

    reduce_density = st.checkbox("Reduce stocking density")
    improve_water = st.checkbox("Improve water quality")
    stun_slaughter = st.checkbox("Use electrical stunning", value=True)

    # =============================
    # INTELLIGENT INTERVENTIONS
    # =============================

    # STOCKING DENSITY
    if reduce_density:
        current = sim_scores["Stocking Density"]["value"]

        if system_type == "Intensive":
            reduction = 1.5
        else:
            reduction = 1

        if current >= 4:
            reduction += 0.5

        sim_scores["Stocking Density"]["value"] = max(1, current - reduction)

    # WATER QUALITY
    if improve_water:
        current = sim_scores["Water Quality"]["value"]

        reduction = 1

        if current >= 4:
            reduction += 0.5

        sim_scores["Water Quality"]["value"] = max(1, current - reduction)

    # SLAUGHTER
    if stun_slaughter:
        sim_scores["Slaughter"]["value"] = 2

    new_risk, _, _, _ = compute_risk(sim_scores, system_type, stage, sentience)

    return new_risk, reduce_density, improve_water, stun_slaughter

# =============================
# ADVOCACY LAYER
# =============================

# =============================
# INTERVENTION INTELLIGENCE (V3)
# =============================

def render_intervention_intelligence(scores, final_risk, system_type, geo, top_driver):
  
    
    # Risk band
    if final_risk >= 6:
        risk_band = "High"
    elif final_risk >= 3:
        risk_band = "Moderate"
    else:
        risk_band = "Low"

    # Core insight
    st.write(f"""
    **Priority rationale:** {top_driver} functions as the system bottleneck, 
    meaning targeted intervention yields disproportionately high welfare gains.
    """)      
    
def render_advocacy(target_actor, top_driver, final_risk, geo, system_type):

    
    # Risk level
    if final_risk >= 6:
        risk_level = "High"
    elif final_risk >= 3:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    
    st.markdown("**Why this matters:**")
    st.write(f"""
    In **{geo}**, under a **{system_type.lower()} system**, welfare risk is primarily driven by **{top_driver.lower()} conditions**.
    This indicates a concentrated source of suffering rather than diffuse issues.
    """)

    st.markdown("**Strategic entry point:**")

    # =============================
    # SLAUGHTER (MOST IMPORTANT)
    # =============================
    if top_driver == "Slaughter":

        # === CONTEXT-SPECIFIC STRATEGY ===
        if geo == "India" and system_type == "Extensive":
            st.write("""
    In decentralised systems such as those common in India, slaughter often occurs outside formal facilities,
    which limits the effectiveness of direct regulation.

    However, targeting export-oriented processors and aggregation points—where compliance incentives already exist—
    can provide an entry point for introducing humane slaughter practices.
    """)

        elif system_type == "Intensive":
            st.write("""
    In intensive systems, slaughter is typically concentrated within processing units.
    This creates an opportunity to introduce humane slaughter practices through corporate standards
    and procurement requirements.
    """)

        else:
            st.write("""
    Where slaughter is controlled by identifiable supply chain actors,
    interventions targeting processors and certification systems can significantly improve welfare outcomes.
    """)

    # =============================
    # WATER QUALITY
    # =============================
    elif top_driver == "Water Quality":

        if geo == "India":
            st.write("""
    In many aquaculture systems, improving water quality requires low-cost interventions such as aeration and water exchange.

    Framing these improvements as productivity gains significantly increases adoption.
    """)
        else:
            st.write("""
    Strengthening regulatory compliance and monitoring systems is more effective in improving water quality outcomes.
    """)

    # =============================
    # STOCKING DENSITY
    # =============================
    elif top_driver == "Stocking Density":

        st.write("""
        Interventions should prioritise certification systems and buyer-led enforcement mechanisms,
        as direct regulation is unlikely to be effective under current incentive structures.
        """)
        st.write("-> Use market incentives rather than direct regulation")

    # =============================
    # DISEASE
    # =============================
    elif top_driver == "Disease":

        st.write("-> Focus on biosecurity training and farm-level protocols")
        st.write("-> Target clusters of farms rather than individuals")

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
        # === ADD IMAGE-BASED INTERPRETATION (HERE) ===

        if brightness < 50:
            st.caption("Image signal: Low visibility suggests potential water quality issues")

        if contrast > 40:
            st.caption("Image signal: High variation may indicate crowding or uneven distribution")     

    return scores, image_flag

# =============================
# UI
# =============================

# =============================
# UI TOOLTIP LAYER
# =============================

TOOLTIPS = {
    "Stocking Density": "More crowding increases stress, aggression, and oxygen depletion",
    "Water Quality": "Poor water conditions increase ammonia toxicity and chronic stress",
    "Slaughter Method Severity (absolute)": "Represents the killing method used. This is not a deviation — it directly reflects welfare severity (e.g. stunning vs asphyxiation)",
    "Disease Risk": "Higher values indicate higher infection pressure and mortality risk"
}

st.title("🐟 Fish Welfare Decision System")

st.caption(
"A transparent decision-support system that identifies the dominant sources of suffering in aquaculture systems and simulates high-impact welfare interventions."
)

# =============================
# DATA & METHOD
# =============================

with st.expander("📊 Data & Method (What this tool is based on)"):
    st.write("""
This tool combines:
- Scientific welfare evidence
- A weighted multi-driver risk model
- Contextual and empirical inputs

The system is transparent, rule-based, and designed for policy and advocacy applications.

This is a **transparent, rule-based decision model** designed for policy and advocacy—not a black-box AI system.
""")

st.markdown("**Key references:**")
st.markdown("[FAO Aquaculture](https://www.fao.org/fishery/en)")
st.markdown("[EFSA Fish Welfare](https://www.efsa.europa.eu/)")
st.markdown("[WOAH Aquatic Code](https://www.woah.org/en/what-we-do/standards/)")

with st.expander("Click to understand the model"):
    st.write("""
This tool estimates **fish welfare risk** using four key drivers:

- Stocking Density  
- Water Quality  
- Slaughter Practices  
- Disease Risk  

Each driver is:
- Scored (1-5)
- Weighted based on welfare importance
- Adjusted for system type and geography

The model also includes:
- A **sentience multiplier** (higher sentience = higher moral weight)
- A **system scale factor** (intensive systems increase risk)
- A **stage factor** (mature systems amplify impact)

The goal is to:
-> Identify the **highest-impact welfare problem**  
-> Recommend **targeted interventions**
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

mismatch_issues = detect_mismatch(species, geo, system_type)

mismatch_flag = len(mismatch_issues) > 0

if mismatch_flag:
    st.subheader("⚠️ Scenario Mismatch")

    for issue in mismatch_issues:
        st.warning(issue)

    st.caption("These conditions may reduce realism of the welfare estimate")

if mismatch_flag:
    st.info("⚠ Confidence is reduced due to unrealistic or rare scenario combinations")

sentience = compute_sentience(species, confidence)

st.subheader("🧠 Sentience")

with st.expander("What does this mean?"):
    st.write("""
Sentience reflects an animal's capacity to feel pain and suffering.

Approximate comparison:
- Shrimp: ~0.3
- Carp: ~0.5
- Tilapia: ~0.6
- Salmon: ~0.85
- Mammals (e.g. pigs, cows): ~0.9+

This tool adjusts welfare risk based on sentience:
-> Higher sentience = higher moral weight of suffering

Sentience confidence reflects how certain science is about these estimates:
- Low -> limited or debated evidence
- Medium -> growing but incomplete evidence
- High -> strong scientific consensus
""")

# DRIVERS
st.subheader("🔧 Welfare Drivers")

with st.expander("What are welfare drivers?"):
    st.write("""
    Welfare drivers are the main factors that determine how much suffering fish experience.

    This tool focuses on four key drivers:

    - Stocking Density → How crowded the fish are
    - Water Quality → Oxygen, toxins, and environmental conditions
    - Slaughter → How fish are killed
    - Disease → Infection and health risks
    """)

with st.expander("⚠️ How the scoring system works"):
    st.markdown("""
    The sliders are NOT absolute scores — they adjust a hidden baseline.

    ### How the model works:
    - Each system already has a baseline welfare condition
    - Your inputs are deviations from expected conditions

    ### Important interactions:
    - Poor water quality amplifies other risks
    - Slaughter can dominate total welfare loss
    - The model is multiplicative, not additive
    
    ### What this means for you:
    - Don’t try to “balance” sliders
    - Instead reflect the real-world situation as accurately as possible
    """)

geo_data = BASELINE_DATA["geography"].get(geo, {})
sys_data = BASELINE_DATA["system_type"].get(system_type, {})

st.caption("Low (more space) ← -> High (crowding)")
density_delta = st.slider(
    "Stocking Density (deviation from expected)",
    -2, 2, 0,
    help=TOOLTIPS["Stocking Density"]
)

st.caption("Good quality ← -> Poor quality")
water_delta = st.slider(
    "Water Quality (deviation from expected)",
    -2, 2, 0,
    help=TOOLTIPS["Water Quality"]
)

st.caption("Low infection risk ← -> High infection risk")
disease_delta = st.slider(
    "Disease Risk (deviation from expected)",
    -2, 2, 0,
    help=TOOLTIPS["Disease Risk"]
)

st.caption("⚠ Slaughter is an event (not a continuous condition), so this is an absolute score")
st.caption("Humane (stunned) ← -> Severe (asphyxiation)")

slaughter = st.slider(
    "Slaughter Method Severity (absolute)",
    1, 5, 5,
    help=TOOLTIPS["Slaughter Method Severity (absolute)"]
)

# =============================
# FINAL DRIVER VALUES (V3 FIX)
# =============================

# =============================
# FINAL DRIVER VALUES (FIXED LOGIC)
# =============================

# 1. Start from baseline ONLY
density_base = sys_data.get("stocking_density_base", 2)
water_base = geo_data.get("water_quality_base", 3.5)
disease_base = geo_data.get("disease_pressure", 3.2)

# 2. Build initial scores using baseline
scores = build_scores(
    density_base,
    water_base,
    slaughter,
    disease_base
)

# 3. Apply system/geography adjustments (ONLY ONCE)
scores = apply_baseline(scores, geo, system_type, species)

# 4. NOW apply user deviations (this is the key fix)
scores["Stocking Density"]["value"] = apply_deviation(
    scores["Stocking Density"]["value"], density_delta
)

scores["Water Quality"]["value"] = apply_deviation(
    scores["Water Quality"]["value"], water_delta
)

scores["Disease"]["value"] = apply_deviation(
    scores["Disease"]["value"], disease_delta
)

# =============================
# IMAGE INPUT
# =============================

st.subheader("📷 Evidence Input (Optional)")

with st.expander("📷 What images improve the assessment?"):
    st.write("""

**What to capture:**
- Above-water views (pond surface, crowding)
- Below-water visibility if possible (clarity, turbidity)

**Tips for good images:**
- Ensure good lighting (avoid dark or blurry photos)
- Capture fish density clearly
- Include feeding or active zones

""")
uploaded_files = st.file_uploader(
    "Upload farm images",
    type=["jpg","png","jpeg"],
    accept_multiple_files=True
)

image_flag = False

if uploaded_files:
    for img_file in uploaded_files:
        scores, flag = process_image(img_file, scores)
        if flag:
            image_flag = True
if uploaded_files:
    st.caption(f"Empirical input: {len(uploaded_files)} image(s) used to refine welfare estimates")

# Apply interaction effects BEFORE risk calculation
scores = apply_interactions(scores)

final_risk, weighted, scale, stage_factor = compute_risk(scores, system_type, stage, sentience)

top_driver, ranked = get_top_driver(scores)

# Identify top driver (MOST IMPORTANT FIX)

# Risk level label
if final_risk >= 6:
    risk_level = "High"
elif final_risk >= 3:
    risk_level = "Moderate"
else:
    risk_level = "Low"

top_driver, ranked = get_top_driver(scores)

st.markdown("### 🧾 Welfare Snapshot")

with st.container():

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Welfare Risk Index", final_risk)

    with col2:
        st.metric("Binding Constraint", top_driver)    

    with col3:
        st.metric("Risk Level", risk_level)        
       
# =============================
# DRIVER CONTRIBUTION
# =============================

# =============================
# TRUE CONTRIBUTION (V3)
# =============================

# =============================
# DRIVER CONTRIBUTION
# =============================

raw_contributions = compute_driver_impact(scores, system_type, stage, sentience)

total_raw = sum(raw_contributions.values())

chart_data = []
for k, v in raw_contributions.items():
    pct = (v / total_raw) * 100 if total_raw else 0
    chart_data.append({
        "Driver": k,
        "Contribution": round(pct, 1)
    })

st.markdown("### 📊 Contribution Breakdown")

top_driver_pct = max(chart_data, key=lambda x: x["Contribution"])

st.info(f"""
**Concentration of risk:** {top_driver_pct['Driver']} accounts for ~{top_driver_pct['Contribution']}% of total estimated welfare impact.

This indicates a **non-linear risk structure**, where one constraint disproportionately drives system-level outcomes.
""")

df = pd.DataFrame(chart_data)

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("Contribution:Q", title="Contribution (%)"),
    y=alt.Y("Driver:N", sort='-x'),
    tooltip=["Driver:N", "Contribution:Q"]
)

st.altair_chart(chart, use_container_width=True)

# =============================
# EVIDENCE DETAILS
# =============================

with st.expander("📚 Evidence & Sources"):

    st.markdown("### 📚 Evidence Base")

    for k, v in scores.items():
        ev = EVIDENCE_DB[k]

        with st.expander(f"{k} (Score: {v['value']})"):

            st.write(ev["description"])
            st.caption(f"Intervention: {ev['intervention']}")

            st.markdown("**Sources**")

            for name, link in ev["sources"]:
                st.markdown(f"- [{name}]({link})", unsafe_allow_html=True)
                
    # Contribution section
    
st.markdown("## 🧠 Diagnosis")

st.write(f"""
The model identifies **{top_driver}** as the dominant welfare constraint
after accounting for interaction effects, production intensity, and sentience weighting.

This indicates a concentrated welfare bottleneck rather than evenly distributed system risk.
""")

if top_driver == "Slaughter":
    st.write("""
Intervening at slaughter offers the highest immediate welfare gains,
as suffering is acute, preventable, and concentrated at a single point in the system.
""")

elif top_driver == "Water Quality":
    st.write("""
Water quality acts as a system-wide stressor, influencing disease, mortality, and chronic suffering.
Improving it generates distributed welfare gains across the production cycle.
""")

elif top_driver == "Stocking Density":
    st.write("""
High stocking density drives chronic stress, injury, and oxygen depletion.
Reducing density improves baseline welfare conditions across multiple pathways.
""")

elif top_driver == "Disease":
    st.write("""
Disease represents sustained welfare degradation rather than acute events.
Interventions here improve long-term system stability and reduce cumulative suffering.
""")

def render_summary(top_driver, final_risk):

    # Risk band
    if final_risk >= 6:
        risk_label = "High"
    elif final_risk >= 3:
        risk_label = "Moderate"
    else:
        risk_label = "Low"

    
    st.markdown("**What to do next:**")

    if top_driver == "Slaughter":
        st.write("-> Advocate adoption of electrical stunning")
        st.write("-> Engage processors and supply chain actors")
        st.write("-> Push for welfare standards and enforcement")

    elif top_driver == "Water Quality":
        st.write("-> Improve aeration and water systems")
        st.write("-> Introduce monitoring and farmer training")

    elif top_driver == "Stocking Density":
        st.write("-> Reduce crowding through stocking limits")
        st.write("-> Improve farm management practices")

    elif top_driver == "Disease":
        st.write("-> Strengthen biosecurity and hygiene")
        st.write("-> Reduce infection pressure at system level")

    # Core message (THIS is what evaluators read)
    st.markdown(f"""
**Overall welfare risk: {risk_label}**

The system is constrained by **{top_driver}**, making it the most effective intervention point.
""")

st.markdown("---")
st.markdown("## 🎯 Strategy")

# Strategic clarity
if top_driver == "Slaughter":
    st.write("""
Improving slaughter practices offers the **highest-leverage intervention**, 
with immediate and system-wide welfare impact.
""")

elif top_driver == "Water Quality":
    st.write("Improving environmental conditions will reduce chronic stress and mortality.")

elif top_driver == "Stocking Density":
    st.write("Reducing crowding can improve welfare incrementally across the system.")

elif top_driver == "Disease":
    st.write("Improving biosecurity will reduce long-term system instability and suffering.")

with st.container():
    render_intervention_intelligence(scores, final_risk, system_type, geo, top_driver)

st.markdown("---")
st.markdown("## 🏛️ Policy Levers")

with st.container():
    render_policy_intelligence(target_actor, scores, top_driver, geo, system_type)

# =============================
# FINAL SUMMARY (V3)
# =============================

# =============================
# INTERVENTION SIMULATOR
# =============================

st.markdown("---")
st.subheader("🔁 Intervention Simulation")
st.caption("Select an intervention to see how welfare risk changes")

new_risk, reduce_density, improve_water, stun_slaughter = simulate_intervention(
    scores, system_type, stage, sentience
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Current Risk", final_risk)

with col2:
    st.metric("Post-Intervention Risk", new_risk)
if final_risk > 0:

    impact = round(
        ((final_risk - new_risk) / final_risk) * 100,
        1
    )

    if impact > 0:
        st.success(f"⬇ {impact}% reduction in welfare risk")
    else:
        st.warning(
            f"No meaningful change — intervention not targeting binding constraint ({top_driver})"
        )

    
# TRANSPARENCY

st.markdown("---")
st.subheader("🔬 Calculation")
st.write("""
The welfare risk score combines:

- Weighted driver severity
- Interaction effects between welfare conditions
- Production system intensity
- Industry development stage
- Sentience-adjusted moral weighting
- Empirical image-based signals (optional)

The model is multiplicative rather than additive, allowing concentrated suffering events to dominate system outcomes.  

""")

st.markdown("---")

# CONFIDENCE
# =============================
# CONFIDENCE (V3 FIX)
# =============================

num_images = len(uploaded_files) if uploaded_files else 0

confidence_score = compute_confidence(
    scores,
    mismatch_flag,
    num_images > 0,
    num_images
)
st.subheader("📉 Confidence")

st.write("""Confidence reflects scenario realism, input quality, and empirical support.

Confidence increases with stronger evidence inputs and decreases under extreme or unrealistic assumptions.
""")

st.write(f"Confidence: **{confidence_score}**")
if confidence_score > 0.75:
    st.caption("High confidence: strong evidence + realistic scenario")
elif confidence_score > 0.5:
    st.caption("Moderate confidence: some assumptions or missing evidence")
else:
    st.caption("Low confidence: scenario uncertainty or weak inputs")

if mismatch_flag:
    st.caption("⚠ Reduced confidence due to scenario mismatch")

# =============================
# DOWNLOAD REPORT
# =============================

st.subheader("📄 Export Report")

report = f"""
FISH WELFARE DECISION REPORT
============================

Species: {species}
Geography: {geo}
Production System: {system_type}
Target Actor: {target_actor}

-----------------------------------
WELFARE SNAPSHOT
-----------------------------------

Welfare Risk Index: {final_risk}
Binding Constraint: {top_driver}
Confidence Score: {confidence_score}

-----------------------------------
STRATEGIC DIAGNOSIS
-----------------------------------

Primary welfare bottleneck:
{top_driver}

Key intervention pathway:
"""

if top_driver == "Slaughter":
    report += "\nAdopt humane slaughter and electrical stunning."

elif top_driver == "Water Quality":
    report += "\nImprove aeration, filtration, and water management."

elif top_driver == "Stocking Density":
    report += "\nReduce crowding and improve stocking practices."

elif top_driver == "Disease":
    report += "\nStrengthen biosecurity and disease monitoring."

report += f"""

-----------------------------------
MODEL NOTES
-----------------------------------

This report was generated using a structured welfare model integrating:
- Scientific evidence
- Production system factors
- Sentience weighting
- Interaction effects
- Contextual inputs

"""
st.download_button(
    label="⬇ Download Report",
    data=report,
    file_name="fish_welfare_report.txt",
    mime="text/plain"
)
# =============================
# CREDIT
# =============================

st.markdown("---")

st.markdown("""
<div style='padding-top: 5px; padding-bottom: 10px; line-height: 1.6;'>

<p style='font-size:14px; color: #A0A0A0;'>
Developed by <b>Anusha Narain</b><br>
Sentient Futures Fellowship<br>
Mentored by <b>James Morgan</b>
</p>

</div>
""", unsafe_allow_html=True)
