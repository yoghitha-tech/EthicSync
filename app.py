import streamlit as st

st.set_page_config(
    page_title="EthicSync",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚖️ EthicSync")
st.sidebar.write("Clinical Decision Support System")

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
        st.metric("Active Cases", 12)

    with col2:
        st.metric("Pending Reviews", 5)

    with col3:
        st.metric("Urgent Cases", 3)

    with col4:
        st.metric("Consensus", "78%")

    st.divider()

    st.subheader("Recent Activity")

    st.write("🟢 Case #001 — Clinical review completed")
    st.write("🟡 Case #002 — Awaiting stakeholder opinion")
    st.write("🔴 Case #003 — Urgent human review required")


# ---------------- NEW CASE ----------------

elif page == "➕ New Case":

    st.title("➕ New Case")

    st.subheader("Patient Information")

    patient_name = st.text_input("Patient ID / Name")

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

        if patient_name == "":
            st.warning("Please enter a Patient ID / Name.")

        else:
            st.success("Case created successfully!")

            st.write("### Case Summary")
            st.write("Patient:", patient_name)
            st.write("Age:", age)
            st.write("Health Problem:", health_problem)
            st.write("Urgency:", urgency)
