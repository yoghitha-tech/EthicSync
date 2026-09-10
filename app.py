import streamlit as st

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="EthicSync",
    page_icon="⚕️",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "cases" not in st.session_state:
    st.session_state.cases = []


# --------------------------------------------------
# URGENCY FUNCTION
# --------------------------------------------------

def calculate_urgency(clinical_info, clinical_status, time_sensitive):

    score = 0

    # Clinical status
    if clinical_status == "Needs monitoring":
        score += 1

    elif clinical_status == "Deteriorating":
        score += 2

    elif clinical_status == "Critical":
        score += 3

    # Time sensitivity
    if time_sensitive == "Yes":
        score += 2

    # Keywords
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

    # Final urgency
    if score >= 5:
        return "CRITICAL"

    elif score >= 3:
        return "URGENT"

    elif score >= 1:
        return "MODERATE"

    else:
        return "ROUTINE"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚕️ EthicSync")
st.sidebar.write("Clinical Decision Support System")

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


# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    st.title("🏠 Dashboard")
    st.write("Overall case overview")

    total_cases = len(st.session_state.cases)

    urgent_cases = 0

    pending_cases = 0

    for case in st.session_state.cases:

        if case["Urgency"] in ["CRITICAL", "URGENT"]:
            urgent_cases += 1

        if case["Status"] == "Pending Review":
            pending_cases += 1

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Active Cases",
            total_cases
        )

    with col2:
        st.metric(
            "Pending Reviews",
            pending_cases
        )

    with col3:
        st.metric(
            "Urgent Cases",
            urgent_cases
        )

    with col4:
        st.metric(
            "Consensus Status",
            "78%"
        )

    st.divider()

    st.subheader("🔔 Notifications")

    if urgent_cases > 0:
        st.warning(
            str(urgent_cases) +
            " urgent/critical case(s) require priority review."
        )
    else:
        st.success("No urgent cases currently flagged.")

    st.subheader("🕒 Recent Activity")

    if total_cases == 0:
        st.info("No cases created yet.")

    else:

        for case in st.session_state.cases[-5:]:

            st.write(
                "Patient "
                + case["Patient ID"]
                + " — "
                + case["Urgency"]
                + " — "
                + case["Status"]
            )


# ==================================================
# NEW CASE
# ==================================================

elif page == "New Case":

    st.title("➕ New Case")

    st.write(
        "Create a new clinical case for decision support."
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

    st.subheader("Case Description")

    case_description = st.text_area(
        "Describe the case"
    )

    st.subheader("Clinical Decision Options")

    decision_options = st.text_area(
        "Enter possible clinical decision options"
    )

    st.subheader("Ethical Issue")

    ethical_issue = st.text_area(
        "Describe any ethical issue"
    )

    if st.button("Create Case"):

        if patient_id == "":
            st.error("Please enter a Patient ID.")

        elif clinical_info == "":
            st.error("Please enter clinical information.")

        else:

            final_urgency = calculate_urgency(
                clinical_info,
                clinical_status,
                time_sensitive
            )

            new_case = {
                "Patient ID": patient_id,
                "Age": age,
                "Health Problem": health_problem,
                "Clinical Information": clinical_info,
                "Clinical Status": clinical_status,
                "Time Sensitive": time_sensitive,
                "Case Description": case_description,
                "Decision Options": decision_options,
                "Ethical Issue": ethical_issue,
                "Urgency": final_urgency,
                "Status": "Pending Review"
            }

            st.session_state.cases.append(
                new_case
            )

            st.success(
                "✅ Case created successfully!"
            )

            if final_urgency == "CRITICAL":

                st.error(
                    "🚨 CRITICAL CASE — Human clinical review required"
                )

            elif final_urgency == "URGENT":

                st.warning(
                    "⚠️ URGENT CASE — Priority review required"
                )

            elif final_urgency == "MODERATE":

                st.info(
                    "🟡 MODERATE CASE — Review recommended"
                )

            else:

                st.success(
                    "🟢 ROUTINE CASE"
                )


# ==================================================
# CASES
# ==================================================

elif page == "Cases":

    st.title("📁 Cases")

    st.write(
        "View and manage clinical cases."
    )

    search = st.text_input(
        "🔍 Search by Patient ID"
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

    filtered_cases = st.session_state.cases

    # Search
    if search:

        filtered_cases = [
            case
            for case in filtered_cases
            if search.lower()
            in case["Patient ID"].lower()
        ]

    # Urgency filter
    if urgency_filter != "All":

        filtered_cases = [
            case
            for case in filtered_cases
            if case["Urgency"] == urgency_filter
        ]

    st.divider()

    if len(filtered_cases) == 0:

        st.info("No cases found.")

    else:

        for case in filtered_cases:

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
                    "**Clinical Status:**",
                    case["Clinical Status"]
                )

                st.write(
                    "**Time Sensitive:**",
                    case["Time Sensitive"]
                )

                st.write(
                    "**Urgency:**",
                    case["Urgency"]
                )

                st.write(
                    "**Status:**",
                    case["Status"]
                )

                if case["Ethical Issue"]:

                    st.write(
                        "**Ethical Issue:**",
                        case["Ethical Issue"]
                    )


# ==================================================
# PATIENT CARE URGENCY
# ==================================================

elif page == "Patient Care Urgency":

    st.title("🚨 Patient Care Urgency")

    st.write(
        "Prototype rule-based urgency assessment."
    )

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

        st.subheader(
            "Urgency Result"
        )

        if result == "CRITICAL":

            st.error(
                "🚨 CRITICAL"
            )

            st.warning(
                "Human clinical review required."
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


# ==================================================
# CLINICAL INFORMATION
# ==================================================

elif page == "Clinical Information":

    st.title("🩺 Clinical Information")

    st.write("Clinical information management.")

    st.checkbox("Medical History")

    st.checkbox("Current Clinical Status")

    st.checkbox("Relevant Findings")

    st.checkbox("Investigations")

    st.checkbox("Current Care Information")

    st.checkbox("Available Decision Options")

    st.info(
        "Detailed clinical information module will be developed next."
    )


# ==================================================
# AI DECISION SUPPORT
# ==================================================

elif page == "AI Decision Support":

    st.title("🤖 AI Decision Support")

    st.write(
        "AI-assisted analysis of clinical cases and decision options."
    )

    # Check whether cases exist
    if len(st.session_state.cases) == 0:

        st.info(
            "No cases available. Please create a case first."
        )

    else:

        # Select case
        patient_ids = []

        for case in st.session_state.cases:
            patient_ids.append(case["Patient ID"])

        selected_patient = st.selectbox(
            "Select Patient Case",
            patient_ids
        )

        # Find selected case
        selected_case = None

        for case in st.session_state.cases:

            if case["Patient ID"] == selected_patient:
                selected_case = case

        st.divider()

        # ------------------------------------------
        # CASE INFORMATION
        # ------------------------------------------

        st.subheader("📋 Case Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(
                "**Patient ID:**",
                selected_case["Patient ID"]
            )

        with col2:
            st.write(
                "**Age:**",
                selected_case["Age"]
            )

        with col3:
            st.write(
                "**Urgency:**",
                selected_case["Urgency"]
            )

        st.write(
            "**Health Problem:**",
            selected_case["Health Problem"]
        )

        st.write(
            "**Clinical Information:**",
            selected_case["Clinical Information"]
        )

        # ------------------------------------------
        # ETHICAL ISSUE
        # ------------------------------------------

        st.subheader("⚖️ Ethical Issue")

        if selected_case["Ethical Issue"]:

            st.warning(
                selected_case["Ethical Issue"]
            )

        else:

            st.info(
                "No ethical issue has been recorded."
            )

        # ------------------------------------------
        # DECISION OPTIONS
        # ------------------------------------------

        st.subheader("💡 Clinical Decision Options")

        options_text = selected_case["Decision Options"]

        if options_text:

            options = options_text.split("\n")

            for i, option in enumerate(options):

                if option.strip():

                    st.write(
                        str(i + 1) + ". " + option
                    )

        else:

            options = []

            st.info(
                "No decision options have been entered."
            )

        # ------------------------------------------
        # AI ANALYSIS
        # ------------------------------------------

        if st.button("🤖 Analyze Case"):

            st.divider()

            st.subheader("🧠 AI Analysis")

            urgency = selected_case["Urgency"]

            clinical_text = selected_case[
                "Clinical Information"
            ].lower()

            # Basic prototype reasoning
            if urgency == "CRITICAL":

                recommendation = (
                    "Prioritize immediate clinical review "
                    "and the safest available intervention."
                )

                reasoning = (
                    "The case has been classified as CRITICAL. "
                    "The system therefore prioritizes patient safety "
                    "and immediate human clinical review."
                )

                confidence = "High urgency signal"

            elif urgency == "URGENT":

                recommendation = (
                    "Prioritize timely clinical intervention "
                    "with human review."
                )

                reasoning = (
                    "The case has been classified as URGENT. "
                    "The system recommends priority review "
                    "before a final decision is made."
                )

                confidence = "Moderate-high urgency signal"

            elif urgency == "MODERATE":

                recommendation = (
                    "Review available options and obtain "
                    "additional clinical information if required."
                )

                reasoning = (
                    "The case has a MODERATE urgency level. "
                    "Additional clinical review can help "
                    "differentiate between available options."
                )

                confidence = "Moderate urgency signal"

            else:

                recommendation = (
                    "Proceed with routine clinical review "
                    "and compare available options."
                )

                reasoning = (
                    "The case has been classified as ROUTINE. "
                    "The system recommends standard review "
                    "of the available decision options."
                )

                confidence = "Routine urgency signal"

            # --------------------------------------
            # RESULTS
            # --------------------------------------

            st.success(
                "Suggested Decision Approach"
            )

            st.write(
                recommendation
            )

            st.subheader("Why?")

            st.write(
                reasoning
            )

            st.subheader("📊 Uncertainty / Confidence")

            st.info(
                confidence
            )

            # --------------------------------------
            # CLINICAL KEYWORD CHECK
            # --------------------------------------

            st.subheader(
                "🔍 Clinical Information Analysis"
            )

            important_terms = [
                "severe",
                "critical",
                "chest pain",
                "breathing difficulty",
                "shock",
                "collapse",
                "unconscious"
            ]

            detected = []

            for term in important_terms:

                if term in clinical_text:
                    detected.append(term)

            if len(detected) > 0:

                st.warning(
                    "Important clinical terms detected: "
                    + ", ".join(detected)
                )

            else:

                st.info(
                    "No predefined high-risk keywords detected."
                )

            # --------------------------------------
            # HUMAN REVIEW
            # --------------------------------------

            st.subheader(
                "👨‍⚕️ Human Review"
            )

            st.warning(
                "AI output is decision support only. "
                "A qualified human decision-maker must "
                "review and approve the final clinical decision."
            )


# ==================================================
# MCDM ANALYSIS
# ==================================================

elif page == "MCDM Analysis":

    st.title("📊 MCDM Analysis")

    st.write(
        "Multi-Criteria Decision Making"
    )

    st.info(
        "MCDM calculation module will be developed next."
    )

    st.write("Planned features:")

    st.write("• Criteria selection")

    st.write("• Criteria weighting")

    st.write("• Option scoring")

    st.write("• Weighted-score calculation")

    st.write("• Option ranking")

    st.write("• Sensitivity analysis")

    st.write("• Calculation transparency")


# ==================================================
# TRADE-OFF ANALYSIS
# ==================================================

elif page == "Trade-off Analysis":

    st.title("⚖️ Trade-off Analysis")

    st.write(
        "Compare benefits, risks and ethical considerations."
    )

    st.info(
        "Trade-off analysis module will be developed next."
    )

    st.write("Planned comparisons:")

    st.write("• Benefits")

    st.write("• Risks and limitations")

    st.write("• Resources")

    st.write("• Ethical trade-offs")

    st.write("• Patient preferences")

    st.write("• Clinical priorities")


# ==================================================
# STAKEHOLDER OPINIONS
# ==================================================

elif page == "Stakeholder Opinions":

    st.title("👥 Stakeholder Opinions")

    stakeholder = st.selectbox(
        "Select Stakeholder",
        [
            "Treating Doctor",
            "Appointed Doctor",
            "Patient",
            "Medical Official"
        ]
    )

    opinion = st.text_area(
        "Enter opinion"
    )

    preferred_option = st.text_input(
        "Preferred Decision Option"
    )

    if st.button("Submit Opinion"):

        st.success(
            stakeholder
            + " opinion recorded."
        )


# ==================================================
# CONSENSUS MANAGEMENT
# ==================================================

elif page == "Consensus Management":

    st.title("🤝 Consensus Management")

    st.write(
        "Track stakeholder agreement and disagreement."
    )

    agreement = st.slider(
        "Consensus Percentage",
        0,
        100,
        78
    )

    st.metric(
        "Current Consensus",
        str(agreement) + "%"
    )

    if agreement >= 75:

        st.success(
            "Consensus level: Good"
        )

    elif agreement >= 50:

        st.warning(
            "Consensus level: Moderate"
        )

    else:

        st.error(
            "Further review may be required."
        )


# ==================================================
# DECISION TRANSPARENCY
# ==================================================

elif page == "Decision Transparency":

    st.title("🔎 Decision Transparency")

    st.write(
        "View the factors considered during decision-making."
    )

    st.write("• Evidence considered")

    st.write("• Data sources")

    st.write("• Ethical criteria")

    st.write("• Criteria weights")

    st.write("• Option scores")

    st.write("• AI reasoning")

    st.write("• Stakeholder contributions")

    st.write("• Trade-offs")

    st.write("• Disagreements")

    st.write("• Human review status")


# ==================================================
# FINAL HUMAN DECISION
# ==================================================

elif page == "Final Human Decision":

    st.title("👨‍⚕️ Final Human Decision")

    st.write(
        "Final decision must be reviewed and recorded by an authorized human decision-maker."
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

    approved = st.checkbox(
        "Human review completed"
    )

    if st.button("Record Final Decision"):

        if approved:

            st.success(
                "✅ Final human decision recorded."
            )

        else:

            st.warning(
                "Human review confirmation is required."
            )


# ==================================================
# AUDIT TRAIL
# ==================================================

elif page == "Audit Trail":

    st.title("📜 Audit Trail")

    st.write(
        "Track case and decision history."
    )

    st.write("• User activity tracking")

    st.write("• Decision history")

    st.write("• Data-change history")

    st.write("• Timestamp tracking")

    st.write("• User-role tracking")

    st.write("• AI analysis history")

    st.write("• Final decision history")


# ==================================================
# NOTIFICATIONS
# ==================================================

elif page == "Notifications":

    st.title("🔔 Notifications")

    urgent_count = 0

    for case in st.session_state.cases:

        if case["Urgency"] in ["CRITICAL", "URGENT"]:

            urgent_count += 1

    if urgent_count > 0:

        st.warning(
            str(urgent_count)
            + " urgent/critical case(s) require review."
        )

    else:

        st.success(
            "No urgent notifications."
        )

    st.write("• Urgent-case alerts")

    st.write("• Pending-review alerts")

    st.write("• New opinion notifications")

    st.write("• Disagreement alerts")

    st.write("• Consensus notifications")

    st.write("• Human-review notifications")


# ==================================================
# SETTINGS
# ==================================================

elif page == "Settings":

    st.title("⚙️ Settings")

    st.write("System configuration")

    st.write("• User Profile")

    st.write("• Role Management")

    st.write("• Notification Settings")

    st.write("• Decision Criteria")

    st.write("• MCDM Weight Configuration")

    st.write("• Access Permissions")

    st.write("• Security Settings")

    st.info(
        "Security and authentication features will be implemented in the next development stage."
    )
