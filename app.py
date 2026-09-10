import streamlit as st
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EthicSync",
    page_icon="⚕️",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "cases" not in st.session_state:
    st.session_state.cases = []

if "audit" not in st.session_state:
    st.session_state.audit = []


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def add_audit(message):

    st.session_state.audit.append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        }
    )


def calculate_urgency(
    clinical_info,
    clinical_status,
    time_sensitive
):

    score = 0

    if clinical_status == "Needs monitoring":
        score += 1

    elif clinical_status == "Deteriorating":
        score += 2

    elif clinical_status == "Critical":
        score += 3

    if time_sensitive == "Yes":
        score += 2

    keywords = [
        "severe",
        "unconscious",
        "collapse",
        "breathing difficulty",
        "chest pain",
        "shock",
        "critical"
    ]

    text = clinical_info.lower()

    for word in keywords:

        if word in text:
            score += 2

    if score >= 5:
        return "CRITICAL"

    elif score >= 3:
        return "URGENT"

    elif score >= 1:
        return "MODERATE"

    else:
        return "ROUTINE"


# =========================================================
# AUTOMATIC DECISION OPTIONS
# =========================================================

def generate_options(problem):

    if "Respiratory" in problem:

        return [
            "Immediate clinical intervention",
            "Additional investigation",
            "Supportive monitoring"
        ]

    elif "Diabetes" in problem:

        return [
            "Treatment adjustment",
            "Additional diagnostic assessment",
            "Continued monitoring"
        ]

    elif "Cardiovascular" in problem:

        return [
            "Immediate cardiovascular management",
            "Additional cardiac investigation",
            "Continued monitoring"
        ]

    elif "Infectious" in problem:

        return [
            "Immediate clinical management",
            "Additional diagnostic testing",
            "Supportive monitoring"
        ]

    elif "Cancer" in problem:

        return [
            "Proceed with planned treatment",
            "Additional clinical evaluation",
            "Supportive management"
        ]

    elif "Neurological" in problem:

        return [
            "Immediate neurological assessment",
            "Additional investigation",
            "Continued observation"
        ]

    elif "Trauma" in problem:

        return [
            "Immediate trauma management",
            "Additional diagnostic evaluation",
            "Continued monitoring"
        ]

    else:

        return [
            "Immediate clinical management",
            "Additional investigation",
            "Conservative monitoring"
        ]


# =========================================================
# MCDM SCORING
# =========================================================

def calculate_scores(urgency, options):

    # Default criteria
    weights = {
        "Patient Safety": 40,
        "Clinical Effectiveness": 30,
        "Ethical Acceptability": 15,
        "Resource Availability": 10,
        "Patient Preference": 5
    }

    results = {}

    for i, option in enumerate(options):

        # Prototype scoring
        if i == 0:

            safety = 9
            effectiveness = 9
            ethics = 8
            resources = 6
            preference = 7

        elif i == 1:

            safety = 7
            effectiveness = 7
            ethics = 9
            resources = 8
            preference = 7

        else:

            safety = 5
            effectiveness = 5
            ethics = 8
            resources = 9
            preference = 6

        # Critical cases prioritize safety
        if urgency == "CRITICAL" and i == 0:

            safety = 10
            effectiveness = 10

        score = (
            safety * 0.40
            + effectiveness * 0.30
            + ethics * 0.15
            + resources * 0.10
            + preference * 0.05
        )

        results[option] = round(score * 10, 1)

    return weights, results


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚕️ EthicSync")

st.sidebar.write(
    "Clinical Decision Support System"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "New Case",
        "Cases",
        "Patient Care Urgency",
        "Clinical Information",
        "AI Decision Support",
        "MCDM Analysis",
        "Trade-off Analysis",
        "Stakeholder Opinions",
        "Consensus Management",
        "Decision Transparency",
        "Final Human Decision",
        "Audit Trail",
        "Notifications",
        "Settings"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🏠 Dashboard")

    st.write(
        "Overall case overview"
    )

    total = len(st.session_state.cases)

    urgent = 0
    pending = 0
    critical = 0

    for case in st.session_state.cases:

        if case["Urgency"] in [
            "URGENT",
            "CRITICAL"
        ]:
            urgent += 1

        if case["Urgency"] == "CRITICAL":
            critical += 1

        if case["Status"] == "Pending Review":
            pending += 1

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Active Cases",
            total
        )

    with col2:
        st.metric(
            "Pending Reviews",
            pending
        )

    with col3:
        st.metric(
            "Urgent Cases",
            urgent
        )

    with col4:
        st.metric(
            "Critical Cases",
            critical
        )

    st.divider()

    st.subheader("🔔 Notifications")

    if critical > 0:

        st.error(
            "🚨 Critical case requires human clinical review."
        )

    elif urgent > 0:

        st.warning(
            "⚠️ Urgent case requires priority review."
        )

    else:

        st.success(
            "No urgent notifications."
        )

    st.subheader("🕒 Recent Activity")

    if len(st.session_state.audit) == 0:

        st.info(
            "No recent activity."
        )

    else:

        for activity in st.session_state.audit[-5:]:

            st.write(
                activity["time"]
                + " — "
                + activity["message"]
            )


# =========================================================
# NEW CASE
# =========================================================

elif page == "New Case":

    st.title("➕ New Case")

    st.write(
        "Create a new clinical case."
    )

    st.subheader("Patient Information")

    patient_id = st.text_input(
        "Patient ID"
    )

    age = st.number_input(
        "Patient Age",
        min_value=0,
        max_value=120,
        value=25
    )

    st.subheader("Health Problem")

    health_problem = st.selectbox(
        "Select Health Problem",
        [
            "Cardiovascular Diseases & Hypertension",
            "Diabetes & Metabolic Disorders",
            "Obesity & Overweight",
            "Respiratory Diseases",
            "Neurological Disorders",
            "Mental Health Disorders",
            "Sleep Disorders",
            "Cancer / Oncology",
            "Infectious Diseases & Sepsis",
            "Antimicrobial Resistance (AMR)",
            "Trauma & Severe Injuries",
            "Organ Failure & Critical Conditions",
            "Severe Burns",
            "Post-operative / Surgical Complications",
            "Digestive & Gastrointestinal Disorders",
            "Nutritional & Vitamin/Mineral Deficiencies",
            "Eye & Vision Disorders",
            "Musculoskeletal Disorders",
            "Allergies & Autoimmune Disorders",
            "Maternal & Obstetric Emergencies",
            "Pediatric / Neonatal Conditions",
            "Pollution & Environmental-Related Illnesses",
            "Other / Unclassified Clinical Condition"
        ]
    )

    st.subheader("Clinical Information")

    clinical_info = st.text_area(
        "Enter clinical information"
    )

    clinical_status = st.selectbox(
        "Current Clinical Status",
        [
            "Stable",
            "Needs monitoring",
            "Deteriorating",
            "Critical"
        ]
    )

    time_sensitive = st.selectbox(
        "Is the case time-sensitive?",
        [
            "No",
            "Yes"
        ]
    )

    st.subheader("Ethical Issue")

    ethical_issue = st.text_area(
        "Describe any ethical concern"
    )

    if st.button("Create Case"):

        if patient_id == "":

            st.error(
                "Please enter Patient ID."
            )

        elif clinical_info == "":

            st.error(
                "Please enter clinical information."
            )

        else:

            urgency = calculate_urgency(
                clinical_info,
                clinical_status,
                time_sensitive
            )

            options = generate_options(
                health_problem
            )

            new_case = {

                "Patient ID": patient_id,

                "Age": age,

                "Health Problem":
                    health_problem,

                "Clinical Information":
                    clinical_info,

                "Clinical Status":
                    clinical_status,

                "Time Sensitive":
                    time_sensitive,

                "Ethical Issue":
                    ethical_issue,

                "Urgency":
                    urgency,

                "Decision Options":
                    options,

                "Status":
                    "Pending Review",

                "Final Decision":
                    "Not Recorded"
            }

            st.session_state.cases.append(
                new_case
            )

            add_audit(
                "New case created for Patient "
                + patient_id
            )

            st.success(
                "✅ Case created successfully!"
            )

            st.write(
                "**Detected Urgency:** "
                + urgency
            )

            st.write(
                "**Automatically Generated Options:**"
            )

            for option in options:

                st.write(
                    "• " + option
                )

            if urgency == "CRITICAL":

                st.error(
                    "🚨 CRITICAL — Human clinical review required"
                )

            elif urgency == "URGENT":

                st.warning(
                    "⚠️ URGENT — Priority review required"
                )

            else:

                st.info(
                    "Case successfully classified as "
                    + urgency
                )


# =========================================================
# CASES
# =========================================================

elif page == "Cases":

    st.title("📁 Cases")

    search = st.text_input(
        "🔍 Search Patient ID"
    )

    urgency_filter = st.selectbox(
        "Filter by Urgency",
        [
            "All",
            "CRITICAL",
            "URGENT",
            "MODERATE",
            "ROUTINE"
        ]
    )

    filtered = st.session_state.cases

    if search:

        filtered = [

            case for case in filtered

            if search.lower()
            in case["Patient ID"].lower()

        ]

    if urgency_filter != "All":

        filtered = [

            case for case in filtered

            if case["Urgency"]
            == urgency_filter

        ]

    st.divider()

    if len(filtered) == 0:

        st.info(
            "No cases found."
        )

    else:

        for case in filtered:

            with st.expander(
                "Patient "
                + case["Patient ID"]
                + " — "
                + case["Urgency"]
            ):

                st.write(
                    "**Patient ID:**",
                    case["Patient ID"]
                )

                st.write(
                    "**Age:**",
                    case["Age"]
                )

                st.write(
                    "**Health Problem:**",
                    case["Health Problem"]
                )

                st.write(
                    "**Clinical Information:**",
                    case["Clinical Information"]
                )

                st.write(
                    "**Urgency:**",
                    case["Urgency"]
                )

                st.write(
                    "**Status:**",
                    case["Status"]
                )

                st.write(
                    "**Decision Options:**"
                )

                for option in case["Decision Options"]:

                    st.write(
                        "• " + option
                    )


# =========================================================
# PATIENT CARE URGENCY
# =========================================================

elif page == "Patient Care Urgency":

    st.title("🚨 Patient Care Urgency")

    clinical_info = st.text_area(
        "Clinical Signs / Symptoms"
    )

    clinical_status = st.selectbox(
        "Current Clinical Status",
        [
            "Stable",
            "Needs monitoring",
            "Deteriorating",
            "Critical"
        ]
    )

    time_sensitive = st.selectbox(
        "Is the situation time-sensitive?",
        [
            "No",
            "Yes"
        ]
    )

    if st.button("Assess Urgency"):

        result = calculate_urgency(
            clinical_info,
            clinical_status,
            time_sensitive
        )

        if result == "CRITICAL":

            st.error(
                "🚨 CRITICAL"
            )

        elif result == "URGENT":

            st.warning(
                "⚠️ URGENT"
            )

        elif result == "MODERATE":

            st.info(
                "🟡 MODERATE"
            )

        else:

            st.success(
                "🟢 ROUTINE"
            )

    st.caption(
        "Prototype decision-support logic. "
        "Final clinical decisions require qualified human review."
    )


# =========================================================
# CLINICAL INFORMATION
# =========================================================

elif page == "Clinical Information":

    st.title("🩺 Clinical Information")

    st.write(
        "Clinical information management."
    )

    st.info(
        "Clinical information is captured during case creation "
        "and used by the decision-support modules."
    )

    st.write("• Medical history")

    st.write("• Current clinical status")

    st.write("• Relevant findings")

    st.write("• Investigations")

    st.write("• Current care information")

    st.write("• Available decision options")


# =========================================================
# AI DECISION SUPPORT
# =========================================================

elif page == "AI Decision Support":

    st.title("🤖 AI Decision Support")

    if len(st.session_state.cases) == 0:

        st.info(
            "Create a case first."
        )

    else:

        patient_ids = [

            case["Patient ID"]

            for case in st.session_state.cases

        ]

        selected = st.selectbox(
            "Select Patient Case",
            patient_ids
        )

        case = None

        for item in st.session_state.cases:

            if item["Patient ID"] == selected:

                case = item

        st.divider()

        st.subheader("📋 Case Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                "**Patient:**",
                case["Patient ID"]
            )

        with col2:

            st.write(
                "**Condition:**",
                case["Health Problem"]
            )

        with col3:

            st.write(
                "**Urgency:**",
                case["Urgency"]
            )

        st.write(
            "**Clinical Information:**",
            case["Clinical Information"]
        )

        st.subheader(
            "💡 Suggested Decision Options"
        )

        for option in case["Decision Options"]:

            st.write(
                "• " + option
            )

        if st.button("🤖 Analyze Case"):

            st.divider()

            if case["Urgency"] == "CRITICAL":

                suggestion = case[
                    "Decision Options"
                ][0]

                reason = (
                    "The case is classified as CRITICAL. "
                    "The prototype prioritizes patient safety "
                    "and timely human clinical review."
                )

            elif case["Urgency"] == "URGENT":

                suggestion = case[
                    "Decision Options"
                ][0]

                reason = (
                    "The case is classified as URGENT. "
                    "Priority clinical review is recommended."
                )

            else:

                suggestion = case[
                    "Decision Options"
                ][1]

                reason = (
                    "The case does not currently meet the "
                    "critical urgency threshold. Further "
                    "assessment may help compare available options."
                )

            st.success(
                "🤖 Suggested Option: "
                + suggestion
            )

            st.subheader("🧠 Reasoning")

            st.write(reason)

            st.subheader(
                "📊 Confidence / Uncertainty"
            )

            st.info(
                "Prototype confidence based on available "
                "case information. Additional clinical data "
                "may change the recommendation."
            )

            st.warning(
                "AI output is decision support only. "
                "Final decisions require qualified human review."
            )


# =========================================================
# MCDM ANALYSIS
# =========================================================

elif page == "MCDM Analysis":

    st.title("📊 MCDM Analysis")

    st.write(
        "Multi-Criteria Decision Making"
    )

    if len(st.session_state.cases) == 0:

        st.info(
            "Create a case first."
        )

    else:

        patient_ids = [

            case["Patient ID"]

            for case in st.session_state.cases

        ]

        selected = st.selectbox(
            "Select Case",
            patient_ids
        )

        selected_case = None

        for case in st.session_state.cases:

            if case["Patient ID"] == selected:

                selected_case = case

        st.subheader(
            "Automatically Selected Criteria"
        )

        weights, scores = calculate_scores(
            selected_case["Urgency"],
            selected_case["Decision Options"]
        )

        for criterion, weight in weights.items():

            st.write(
                criterion
                + " — "
                + str(weight)
                + "%"
            )

        st.divider()

        st.subheader(
            "🏆 Decision Option Ranking"
        )

        ranking = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for position, item in enumerate(
            ranking,
            start=1
        ):

            option = item[0]
            score = item[1]

            if position == 1:

                st.success(
                    "🥇 "
                    + option
                    + " — "
                    + str(score)
                    + "/100"
                )

            elif position == 2:

                st.info(
                    "🥈 "
                    + option
                    + " — "
                    + str(score)
                    + "/100"
                )

            else:

                st.write(
                    "🥉 "
                    + option
                    + " — "
                    + str(score)
                    + "/100"
                )

        st.divider()

        st.subheader(
            "🧮 Calculation Transparency"
        )

        st.write(
            "Weighted Score = "
            "(Safety × 40%) + "
            "(Effectiveness × 30%) + "
            "(Ethics × 15%) + "
            "(Resources × 10%) + "
            "(Patient Preference × 5%)"
        )

        st.caption(
            "Prototype MCDM scoring for demonstration purposes."
        )


# =========================================================
# TRADE-OFF ANALYSIS
# =========================================================

elif page == "Trade-off Analysis":

    st.title("⚖️ Trade-off Analysis")

    st.write(
        "Compare decision options across major factors."
    )

    if len(st.session_state.cases) == 0:

        st.info(
            "Create a case first."
        )

    else:

        patient_ids = [

            case["Patient ID"]

            for case in st.session_state.cases

        ]

        selected = st.selectbox(
            "Select Case",
            patient_ids
        )

        case = None

        for item in st.session_state.cases:

            if item["Patient ID"] == selected:

                case = item

        for option in case["Decision Options"]:

            st.subheader(
                option
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    "✅ Potential Benefit"
                )

                st.write(
                    "May address the immediate clinical objective."
                )

            with col2:

                st.write(
                    "⚠️ Potential Limitation"
                )

                st.write(
                    "Requires appropriate clinical assessment."
                )

            with col3:

                st.write(
                    "⚖️ Ethical Consideration"
                )

                st.write(
                    "Patient safety and preferences should be considered."
                )


# =========================================================
# STAKEHOLDER OPINIONS
# =========================================================

elif page == "Stakeholder Opinions":

    st.title("👥 Stakeholder Opinions")

    stakeholder = st.selectbox(
        "Stakeholder",
        [
            "Treating Doctor",
            "Appointed Doctor",
            "Patient",
            "Medical Official"
        ]
    )

    preferred_option = st.text_input(
        "Preferred Decision Option"
    )

    reasoning = st.text_area(
        "Reasoning / Opinion"
    )

    if st.button("Submit Opinion"):

        st.success(
            stakeholder
            + " opinion recorded."
        )

        add_audit(
            stakeholder
            + " submitted an opinion."
        )


# =========================================================
# CONSENSUS MANAGEMENT
# =========================================================

elif page == "Consensus Management":

    st.title("🤝 Consensus Management")

    st.write(
        "Track stakeholder agreement."
    )

    doctor_agreement = st.slider(
        "Treating Doctor Agreement",
        0,
        100,
        80
    )

    appointed_agreement = st.slider(
        "Appointed Doctor Agreement",
        0,
        100,
        75
    )

    patient_agreement = st.slider(
        "Patient Agreement",
        0,
        100,
        70
    )

    official_agreement = st.slider(
        "Medical Official Agreement",
        0,
        100,
        80
    )

    consensus = round(
        (
            doctor_agreement
            + appointed_agreement
            + patient_agreement
            + official_agreement
        ) / 4
    )

    st.divider()

    st.metric(
        "Overall Consensus",
        str(consensus) + "%"
    )

    if consensus >= 75:

        st.success(
            "✅ Consensus achieved."
        )

    elif consensus >= 50:

        st.warning(
            "⚠️ Partial consensus — further discussion recommended."
        )

    else:

        st.error(
            "🚨 Significant disagreement detected."
        )


# =========================================================
# DECISION TRANSPARENCY
# =========================================================

elif page == "Decision Transparency":

    st.title("🔎 Decision Transparency")

    st.write(
        "Factors considered during the decision process."
    )

    st.write("📌 Clinical information")

    st.write("📌 Urgency assessment")

    st.write("📌 Ethical considerations")

    st.write("📌 Decision options")

    st.write("📌 MCDM criteria and weights")

    st.write("📌 Weighted option scores")

    st.write("📌 AI reasoning")

    st.write("📌 Stakeholder opinions")

    st.write("📌 Trade-offs")

    st.write("📌 Consensus")

    st.write("📌 Human review")


# =========================================================
# FINAL HUMAN DECISION
# =========================================================

elif page == "Final Human Decision":

    st.title("👨‍⚕️ Final Human Decision")

    if len(st.session_state.cases) == 0:

        st.info(
            "Create a case first."
        )

    else:

        patient_ids = [

            case["Patient ID"]

            for case in st.session_state.cases

        ]

        selected = st.selectbox(
            "Select Case",
            patient_ids
        )

        decision = st.selectbox(
            "Final Decision",
            [
                "Accept AI suggestion",
                "Modify AI suggestion",
                "Reject AI suggestion",
                "Further Review Required"
            ]
        )

        justification = st.text_area(
            "Decision Justification"
        )

        human_review = st.checkbox(
            "I confirm that human review has been completed."
        )

        if st.button("Record Final Decision"):

            if human_review:

                for case in st.session_state.cases:

                    if case["Patient ID"] == selected:

                        case["Final Decision"] = decision

                        case["Status"] = "Decision Recorded"

                add_audit(
                    "Final human decision recorded for Patient "
                    + selected
                )

                st.success(
                    "✅ Final human decision recorded."
                )

            else:

                st.warning(
                    "Human review confirmation is required."
                )


# =========================================================
# AUDIT TRAIL
# =========================================================

elif page == "Audit Trail":

    st.title("📜 Audit Trail")

    if len(st.session_state.audit) == 0:

        st.info(
            "No audit activity yet."
        )

    else:

        for activity in st.session_state.audit:

            st.write(
                "🕒 "
                + activity["time"]
                + " — "
                + activity["message"]
            )


# =========================================================
# NOTIFICATIONS
# =========================================================

elif page == "Notifications":

    st.title("🔔 Notifications")

    critical = 0
    urgent = 0

    for case in st.session_state.cases:

        if case["Urgency"] == "CRITICAL":
            critical += 1

        elif case["Urgency"] == "URGENT":
            urgent += 1

    if critical > 0:

        st.error(
            "🚨 "
            + str(critical)
            + " critical case(s) require human review."
        )

    if urgent > 0:

        st.warning(
            "⚠️ "
            + str(urgent)
            + " urgent case(s) require priority review."
        )

    if critical == 0 and urgent == 0:

        st.success(
            "No urgent notifications."
        )


# =========================================================
# SETTINGS
# =========================================================

elif page == "Settings":

    st.title("⚙️ Settings")

    st.write(
        "System configuration"
    )

    st.checkbox(
        "Enable urgent-case notifications",
        value=True
    )

    st.checkbox(
        "Require human review before final decision",
        value=True
    )

    st.checkbox(
        "Enable audit logging",
        value=True
    )

    st.subheader(
        "Decision Criteria"
    )

    st.write(
        "Patient Safety — 40%"
    )

    st.write(
        "Clinical Effectiveness — 30%"
    )

    st.write(
        "Ethical Acceptability — 15%"
    )

    st.write(
        "Resource Availability — 10%"
    )

    st.write(
        "Patient Preference — 5%"
    )

    st.success(
        "Settings loaded."
    )
