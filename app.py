import streamlit as st

st.set_page_config(
    page_title="EthicSync",
    page_icon="⚖️",
    layout="wide"
)

# Store cases
if "cases" not in st.session_state:
    st.session_state.cases = []


# ---------------- SIDEBAR ----------------

st.sidebar.title("⚖️ EthicSync")
st.sidebar.write("Ethical Clinical Decision Support System")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "➕ New Case",
        "📁 Cases",
        "🚨 Patient Care Urgency",
        "🩺 Clinical Information",
        "🤖 AI Decision Support",
        "📊 MCDM Analysis",
        "⚖️ Trade-off Analysis",
        "👥 Stakeholder Opinions",
        "🤝 Consensus Management",
        "🔍 Decision Transparency",
        "👤 Final Human Decision",
        "📝 Audit Trail",
        "🔔 Notifications",
        "⚙️ Settings"
    ]
)


# ---------------- DASHBOARD ----------------

if page == "🏠 Dashboard":

    st.title("🏠 Dashboard")
    st.subheader("Overall Case Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Active Cases", len(st.session_state.cases))

    with col2:
        st.metric("Pending Reviews", 5)

    with col3:
        st.metric("Urgent Cases", 3)

    with col4:
        st.metric("Consensus", "78%")

    st.divider()

    st.subheader("Recent Activity")

    st.write("🟢 Clinical review completed")
    st.write("🟡 Case awaiting stakeholder opinion")
    st.write("🔴 Urgent human review required")


# ---------------- NEW CASE ----------------

elif page == "➕ New Case":

    st.title("➕ New Case")

    st.subheader("Patient Information")

    patient_name = st.text_input("Patient ID")

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=30
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
        "Enter relevant clinical information"
    )

    urgency = st.selectbox(
        "Urgency of Patient Care",
        [
            "Routine",
            "Moderate",
            "Urgent",
            "Critical"
        ]
    )
    if st.button("Create Case"):
        urgency_score = 0
    if urgency == "Needs monitoring":
        urgency_score += 1
    elif urgency == "Deteriorating":
        urgency_score += 2
    elif urgency == "Critical":
        urgency_score += 3

    keywords = [
        "severe",
        "unconscious",
        "collapse",
        "breathing difficulty",
        "chest pain",
        "shock",
        "critical"
    ]

    for word in keywords:
        if word in clinical_info.lower():
            urgency_score += 2

    if urgency_score >= 5:
        final_urgency = "CRITICAL"
    elif urgency_score >= 3:
        final_urgency = "URGENT"
    elif urgency_score >= 1:
        final_urgency = "MODERATE"
    else:
        final_urgency = "ROUTINE"

    new_case = {
        "Patient ID": patient_id,
        "Age": age,
        "Health Problem": health_problem,
        "Clinical Information": clinical_info,
        "Urgency": final_urgency,
        "Status": "Pending Review"
    }

    st.session_state.cases.append(new_case)

    st.success("Case created successfully!")

    if final_urgency == "CRITICAL":
        st.error("🚨 CRITICAL CASE — Human clinical review required")
    elif final_urgency == "URGENT":
        st.warning("⚠️ URGENT CASE — Priority review required")
    else:
        st.info(f"Case urgency: {final_urgency}")

        if patient_name == "":
            st.warning("Please enter a Patient ID.")

        else:

            new_case = {
                "patient": patient_name,
                "age": age,
                "health_problem": health_problem,
                "clinical_info": clinical_info,
                "urgency": urgency
            }

            st.session_state.cases.append(new_case)

            st.success("Case created successfully! ✅")


# ---------------- CASES ----------------

elif page == "Cases":

    st.title("📁 Cases")
    st.write("View and manage clinical cases.")

    # Search
    search = st.text_input("🔍 Search by Patient ID")

    # Filter
    urgency_filter = st.selectbox(
        "Filter by Urgency",
        ["All", "CRITICAL", "URGENT", "MODERATE", "ROUTINE"]
    )

    filtered_cases = st.session_state.cases

    # Search filtering
    if search:
        filtered_cases = [
            case for case in filtered_cases
            if search.lower() in case["Patient ID"].lower()
        ]

    # Urgency filtering
    if urgency_filter != "All":
        filtered_cases = [
            case for case in filtered_cases
            if case["Urgency"] == urgency_filter
        ]

    # Display cases
    if len(filtered_cases) == 0:

        st.info("No cases found.")

    else:

        for case in filtered_cases:

            with st.expander(
                f"Patient {case['Patient ID']} — {case['Urgency']}"
            ):

                st.write("**Patient ID:**", case["Patient ID"])
                st.write("**Age:**", case["Age"])
                st.write("**Health Problem:**", case["Health Problem"])
                st.write("**Clinical Information:**", case["Clinical Information"])
                st.write("**Urgency:**", case["Urgency"])
                st.write("**Status:**", case["Status"])


# ---------------- OTHER PAGES ----------------

elif page == "🚨 Patient Care Urgency":

    st.title("🚨 Patient Care Urgency")

    st.subheader("Urgency Assessment")

    symptoms = st.text_area(
        "Enter clinical signs or symptoms"
    )

    vital_status = st.selectbox(
        "Current clinical status",
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

        urgency_score = 0

        # Check clinical status
        if vital_status == "Needs monitoring":
            urgency_score += 1

        elif vital_status == "Deteriorating":
            urgency_score += 2

        elif vital_status == "Critical":
            urgency_score += 3

        # Check time sensitivity
        if time_sensitive == "Yes":
            urgency_score += 2

        # Check keywords
        text = symptoms.lower()

        critical_words = [
            "severe",
            "unconscious",
            "collapse",
            "breathing difficulty",
            "chest pain",
            "shock",
            "critical"
        ]

        for word in critical_words:

            if word in text:
                urgency_score += 2

        # Determine urgency
        if urgency_score >= 5:

            urgency = "CRITICAL"
            st.error("🚨 CRITICAL — Immediate human clinical review required.")

        elif urgency_score >= 3:

            urgency = "URGENT"
            st.warning("⚠️ URGENT — Prompt clinical review recommended.")

        elif urgency_score >= 1:

            urgency = "MODERATE"
            st.info("🟡 MODERATE — Clinical monitoring/review recommended.")

        else:

            urgency = "ROUTINE"
            st.success("🟢 ROUTINE — No immediate urgency detected by the prototype rules.")

        st.write("### Assessment Result")

        st.metric(
            "Urgency Level",
            urgency
        )

        st.caption(
            "Prototype rule-based assessment. Final clinical decisions require qualified human review."
        )


elif page == "🩺 Clinical Information":

    st.title("🩺 Clinical Information")
    st.write("Clinical information analysis will be developed next.")


elif page == "🤖 AI Decision Support":

    st.title("🤖 AI Decision Support")
    st.write("AI decision support will be developed next.")


elif page == "📊 MCDM Analysis":

    st.title("📊 MCDM Analysis")
    st.write("MCDM analysis will be developed next.")


elif page == "⚖️ Trade-off Analysis":

    st.title("⚖️ Trade-off Analysis")
    st.write("Trade-off analysis will be developed next.")


elif page == "👥 Stakeholder Opinions":

    st.title("👥 Stakeholder Opinions")
    st.write("Stakeholder opinion system will be developed next.")


elif page == "🤝 Consensus Management":

    st.title("🤝 Consensus Management")
    st.write("Consensus management will be developed next.")


elif page == "🔍 Decision Transparency":

    st.title("🔍 Decision Transparency")
    st.write("Decision transparency will be developed next.")


elif page == "👤 Final Human Decision":

    st.title("👤 Final Human Decision")
    st.write("Final human decision module will be developed next.")


elif page == "📝 Audit Trail":

    st.title("📝 Audit Trail")
    st.write("Audit trail will be developed next.")


elif page == "🔔 Notifications":

    st.title("🔔 Notifications")
    st.write("Notifications will be developed next.")


elif page == "⚙️ Settings":

    st.title("⚙️ Settings")
    st.write("Settings will be developed next.")
