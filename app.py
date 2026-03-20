import streamlit as st

st.set_page_config(page_title="Fish Welfare + Advocacy Tool", layout="wide")

# =========================
# INTRODUCTION
# =========================
st.markdown("""
# Fish Sentience and Welfare Risk + Advocacy Strategy Tool

## What does this tool do?

This tool estimates the **welfare risk experienced by fish** by combining:

- **Sentience** → capacity to feel pain and suffering  
- **Welfare Conditions** → intensity of harmful conditions  
- **Scale** → number of animals and duration of suffering  

It then translates this into:
- A **welfare risk score**
- A **policy-relevant interpretation**
- A **targeted advocacy strategy (BAAMT)**

---

## Why this matters

Fish are among the most numerous animals used by humans, yet they receive minimal welfare protection. Even moderate suffering, when multiplied across large populations and extended durations, results in **extreme cumulative harm**. This tool helps convert complex welfare considerations into structured insights that can inform decisions, advocacy, and policy discussions.

⚠️ This is a decision-support tool, not a precise measurement.
""")

# =========================
# INPUTS
# =========================
st.markdown("## Step 1: Define the Scenario")

species = st.selectbox("Species", ["Carp", "Tilapia", "Salmon"])

geography = st.selectbox("Geography", ["India", "SE Asia", "Europe"])

st.markdown("### Welfare Conditions")

density = st.slider("Stocking Density", 1, 5, 3)
water = st.slider("Water Quality", 1, 5, 3)
handling = st.slider("Handling Stress", 1, 5, 3)
transport = st.slider("Transport Stress", 1, 5, 3)
slaughter = st.slider("Slaughter Conditions", 1, 5, 3)
disease = st.slider("Disease Burden", 1, 5, 3)

st.markdown("### Scale")

number = st.selectbox("Number of Fish", ["Small", "Medium", "Large"])
duration = st.selectbox("Duration", ["Short", "Medium", "Long"])
frequency = st.selectbox("Frequency", ["One-time", "Continuous"], index=1)

# =========================
# SENTIENCE
# =========================
sentience_map = {"Carp": 0.6, "Tilapia": 0.6, "Salmon": 0.8}
sentience = sentience_map[species]

certainty = st.slider("Scientific Certainty about Sentience", 0.3, 1.0, 0.7)

# =========================
# BAAMT INPUTS
# =========================
st.markdown("""
## Step 2: Advocacy Strategy (BAAMT)

The welfare assessment above tells us how severe the problem is.

BAAMT translates that into how to communicate and act on it effectively.

Advocacy is not just about presenting facts. Different audiences respond to different values, beliefs, and priorities. A message that works for the general public may not work for policymakers or corporations.

This section builds a structured strategy by combining:

- Beliefs: What the audience cares about
- Audience: Who you are trying to influence
- Angle: The framing you use
- Message: What you say
- Tone: How you say it

Together, this ensures that welfare insights are translated into targeted, effective advocacy rather than generic messaging.
""")

audience = st.selectbox("Audience", ["Public", "Policymakers", "Corporates", "Advocates"])

st.markdown("""
### How to Answer These Questions

These questions are used to build a moral and psychological profile of your target audience.

You are NOT answering based on your own beliefs.

Instead, think carefully about:
- What motivates this audience?
- What kind of arguments influence their decisions?
- What values they prioritise in real-world situations?

Each question corresponds to a core moral foundation:

- Care → concern for suffering
- Fairness → justice and rights
- Authority → respect for rules and regulation
- Purity → hygiene, contamination, food safety
- Loyalty → tradition and cultural identity

For each question:
- 1 = Not important to this audience
- 5 = Extremely important to this audience

Your responses will directly shape:
- The messaging strategy
- The framing of the issue
- The type of advocacy recommended

Be realistic rather than idealistic — the goal is effectiveness, not agreement.
""")

care = st.slider("Importance of reducing suffering", 1, 5, 3)
fairness = st.slider("Importance of fairness", 1, 5, 3)
authority = st.slider("Trust in authority", 1, 5, 3)
purity = st.slider("Concern about hygiene", 1, 5, 3)
loyalty = st.slider("Importance of tradition", 1, 5, 3)

# =========================
# CALCULATIONS (UNCHANGED)
# =========================
welfare = (density + water + handling + transport + slaughter + disease) / 6

scale_map = {"Small": 1, "Medium": 2, "Large": 3}
duration_map = {"Short": 1, "Medium": 2, "Long": 3}

scale_score = scale_map[number] * duration_map[duration]

risk = sentience * welfare * scale_score * certainty

# =========================
# OUTPUT
# =========================
st.markdown("# Results")

full_report = ""  # accumulator

# SCORE SUMMARY
summary_text = f"""
## Score Summary
Sentience: {sentience:.2f}
Welfare: {welfare:.2f}
Scale: {scale_score}
Final Risk Index: {risk:.2f}

The overall welfare risk score is {risk:.2f}, indicating that fish in this system are likely experiencing meaningful levels of suffering when biological capacity, environmental conditions, and scale are considered together. This arises because multiple stressors interact rather than operate independently, compounding physiological strain and behavioural restriction. At larger scales and longer durations, even moderate welfare deficits translate into substantial cumulative harm, which makes the system ethically significant. This means interventions targeting the main drivers could yield disproportionately large reductions in total suffering.
"""
st.markdown(summary_text)
full_report += summary_text + "\n\n"

# WELFARE ANALYSIS
conditions = {
    "Stocking Density": density,
    "Water Quality": water,
    "Handling": handling,
    "Transport": transport,
    "Slaughter": slaughter,
    "Disease": disease
}

top2 = sorted(conditions, key=conditions.get, reverse=True)[:2]

welfare_text = f"""
## Welfare Analysis

The most severe welfare challenges are {top2[0]} and {top2[1]}, which appear to be the dominant contributors to overall suffering. Elevated {top2[0].lower()} is associated with chronic stress responses, reduced immune competence, and constrained natural behaviours, while high {top2[1].lower()} adds episodic or sustained distress that further destabilises physiological functioning. These factors interact in ways that amplify harm, meaning the combined impact is greater than the sum of individual stressors. At scale, such conditions can result in large populations experiencing prolonged suffering, making targeted reforms in these areas especially impactful and urgent.
"""
st.markdown(welfare_text)
full_report += welfare_text + "\n\n"

# SCALE ANALYSIS
scale_text = f"""
## Scale Analysis

This system involves a {number.lower()} number of fish, with a {duration.lower()} duration of exposure and a {frequency.lower()} frequency pattern. Because the system is { 'continuous' if frequency=='Continuous' else 'episodic' }, the resulting suffering is { 'ongoing and accumulative over time' if frequency=='Continuous' else 'concentrated but still significant during events' }. Scale matters because it converts individual welfare impacts into population-level harm, especially when exposure is prolonged. In continuous systems, even moderate welfare deficits persist and compound, which elevates ethical urgency and strengthens the case for systemic interventions rather than isolated fixes.
"""
st.markdown(scale_text)
full_report += scale_text + "\n\n"

# SENTIENCE
sentience_text = f"""
## Sentience Interpretation

The selected species, {species}, has an estimated sentience level of {sentience:.2f}, based on current scientific understanding of fish neurobiology and behaviour. Evidence suggests many fish possess mechanisms consistent with experiencing pain and distress, although the exact degree remains debated. Higher sentience increases moral weight because it implies a greater capacity for negative experiences under harmful conditions. The certainty level of {certainty:.2f} indicates how confident we are in this estimate, which affects how strongly we interpret the ethical implications of the observed welfare conditions.
"""
st.markdown(sentience_text)
full_report += sentience_text + "\n\n"

# MORAL UNCERTAINTY
uncertainty_text = f"""
## Moral Uncertainty

Scientific certainty in this case is {certainty:.2f}, meaning that while some uncertainty exists, the possibility of meaningful suffering cannot be dismissed. When uncertainty is combined with large-scale exposure, the ethical risk increases because the potential downside involves extensive harm across many individuals. The precautionary principle suggests that uncertainty should not justify inaction when stakes are high. In this scenario, the combination of scale and non-trivial sentience implies that even under uncertainty, proactive intervention is justified to prevent potentially large-scale suffering.
"""
st.markdown(uncertainty_text)
full_report += uncertainty_text + "\n\n"

# POLICY
policy_text = "## Policy Recommendations\n\n"

if geography == "India":
    policy_text += "In India, gaps in enforcement and monitoring often limit the effectiveness of welfare regulations, which means harmful conditions can persist without accountability. Strengthening inspection systems and establishing enforceable minimum standards would directly address systemic weaknesses. "

if slaughter > 3:
    policy_text += "Slaughter practices appear to be a major contributor to suffering, indicating a need for humane slaughter protocols that minimise distress and time to unconsciousness. "

if density > 3:
    policy_text += "High stocking density suggests chronic stress conditions, making stocking limits and space requirements a key policy lever for improving welfare outcomes. "

policy_text += "If these issues remain unaddressed, the system is likely to continue generating large-scale suffering, particularly under continuous production conditions."

st.markdown(policy_text)
full_report += policy_text + "\n\n"

# BAAMT OUTPUT
baamt_text = f"""
## Advocacy Strategy (BAAMT)

### Moral Profile Summary

This audience shows a distribution across moral priorities: care ({care}), fairness ({fairness}), authority ({authority}), purity ({purity}), and loyalty ({loyalty}). This indicates that their decision-making is influenced by both harm-based reasoning and structural or cultural considerations. As a result, messaging should combine ethical concern with institutional or practical framing. Understanding this profile helps ensure that advocacy aligns with existing values rather than attempting to override them.

### Primary Message

The scale of this system means that large numbers of fish are exposed to conditions that likely generate sustained suffering, particularly given the sentience of species like {species}. This creates an ethical and practical concern that cannot be ignored, especially in systems where exposure is continuous. Addressing these issues aligns not only with compassion but also with responsible governance and long-term risk management. Framing the issue in terms of both welfare impact and systemic responsibility increases relevance for this audience.

### Strategic Notes

For {audience} in {geography}, advocacy should reflect both institutional context and welfare severity. In high-scale or continuous systems, emphasis should be placed on systemic reform rather than isolated fixes, as this is where the greatest reduction in suffering can be achieved. Where certainty is moderate, precautionary framing should be used to highlight that inaction carries potential ethical and reputational risks. Tailoring messaging to align with audience values increases the likelihood of engagement and meaningful response.
"""
st.markdown(baamt_text)
full_report += baamt_text + "\n\n"

# WHAT YOU CAN DO
what_text = """
## What You Can Do With This

This report is designed to support real-world action across multiple domains. It can be used to inform policy discussions by highlighting areas of regulatory weakness and welfare concern, or to support advocacy campaigns by providing structured and evidence-based arguments. Corporates can use it to assess supply chain risks, while researchers and funders can identify priority areas for intervention. In systems where suffering is continuous and large-scale, the findings suggest that systemic change is more effective than incremental adjustments.
"""
st.markdown(what_text)
full_report += what_text + "\n\n"

# LIMITATIONS
limit_text = """
## Limitations and Interpretation

This tool provides a structured approximation based on simplified inputs and current scientific understanding. Welfare conditions are represented in a reduced form and may not capture the full complexity of real-world systems, while sentience estimates vary across scientific literature. Additionally, actual conditions may differ from those reported in the inputs. Despite these limitations, the model is designed to highlight areas of potentially large-scale suffering, particularly where uncertainty and scale interact. Results should therefore be interpreted as guidance for decision-making rather than precise measurement.
"""
st.markdown(limit_text)
full_report += limit_text + "\n\n"

# DOWNLOAD
st.markdown("## Download Report")

st.markdown("""
You can download the full report below. This can be used for sharing, policy discussions, or further analysis.
""")

st.download_button(
    label="Download Full Report (Markdown)",
    data=full_report,
    file_name="fish_welfare_advocacy_report.md",
    mime="text/markdown"
)
