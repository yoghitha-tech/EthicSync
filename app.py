import streamlit as st
from datetime import datetime
import html

# ============================================================
# ETHICSYNC - CLINICAL DECISION SUPPORT PROTOTYPE
# ============================================================

st.set_page_config(
    page_title="EthicSync",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# HEALTH PROBLEMS
# ============================================================

HEALTH_PROBLEMS = [
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

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f9fc;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #123b5d;
}

[data-testid="stSidebar"] {
    background-color: #092f50;
}

[data-testid="stSidebar"] * {
    color: white;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #dbe7ef;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

.metric-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #dbe7ef;
    text-align: center;
}

.option-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border-left: 6px solid #1687c7;
    margin-bottom: 12px;
}

.warning-card {
    background: #fff8e6;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #f1d58a;
}

.danger-card {
    background: #fff0f0;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e8a3a3;
}

.success-card {
    background: #edf9f2;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #9bd4af;
}

.info-card {
    background: #edf7ff;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #a8d5f0;
}

.small-text {
    color: #687987;
    font-size: 14px;
}

.big-score {
    font-size: 32px;
    font-weight: bold;
    color: #123b5d;
}

.stakeholder {
    background: white;
    border: 1px solid #dbe7ef;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "cases" not in st.session_state:
    st.session_state.cases = []

if "audit" not in st.session_state:
    st.session_state.audit = []

if "notifications" not in st.session_state:
    st.session_state.notifications = []

if "case_counter" not in st.session_state:
    st.session_state.case_counter = 1


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def now():
    return datetime.now().strftime("%d-%m-%Y %H:%M")


def add_audit(case_id, user, action, details):
    st.session_state.audit.insert(0, {
        "time": now(),
        "case_id": case_id,
        "user": user,
        "action": action,
        "details": details
    })


def add_notification(message, level="Info"):
    st.session_state.notifications.insert(0, {
        "time": now(),
        "message": message,
        "level": level
    })


def calculate_urgency(urgency_input, time_sensitive, critical):
    if critical:
        return "Critical"

    if urgency_input == "High" or time_sensitive == "Within 24 hours":
        return "High"

    if urgency_input == "Medium" or time_sensitive == "Within 72 hours":
        return "Medium"

    return "Low"


def urgency_color(level):
    if level == "Critical":
        return "🔴"
    if level == "High":
        return "🟠"
    if level == "Medium":
        return "🟡"
    return "🟢"


def generate_options(problem):
    """
    Short, generic decision alternatives.
    This is a prototype and does NOT prescribe treatment.
    """

    if problem in [
        "Trauma & Severe Injuries",
        "Organ Failure & Critical Conditions",
        "Severe Burns",
        "Maternal & Obstetric Emergencies",
        "Pediatric / Neonatal Conditions",
        "Infectious Diseases & Sepsis"
    ]:
        return [
            {
                "name": "A — Immediate Intervention",
                "urgency": "High",
                "benefit": 9,
                "risk": 7,
                "resource": 8,
                "ethics": 8,
                "preference": 6,
                "description": "Act immediately to address the time-sensitive clinical concern."
            },
            {
                "name": "B — Further Investigation",
                "urgency": "Moderate",
                "benefit": 8,
                "risk": 4,
                "resource": 6,
                "ethics": 9,
                "preference": 7,
                "description": "Collect additional information before selecting the next clinical action."
            },
            {
                "name": "C — Conservative Management",
                "urgency": "Low",
                "benefit": 6,
                "risk": 3,
                "resource": 4,
                "ethics": 8,
                "preference": 6,
                "description": "Continue supportive monitoring while avoiding immediate escalation."
            }
        ]

    return [
        {
            "name": "A — Immediate Intervention",
            "urgency": "High",
            "benefit": 8,
            "risk": 7,
            "resource": 8,
            "ethics": 8,
            "preference": 6,
            "description": "Proceed with timely clinical intervention based on the available information."
        },
        {
            "name": "B — Further Investigation",
            "urgency": "Moderate",
            "benefit": 8,
            "risk": 4,
            "resource": 6,
            "ethics": 9,
            "preference": 8,
            "description": "Gather additional evidence before making the next clinical decision."
        },
        {
            "name": "C — Conservative Management",
            "urgency": "Low",
            "benefit": 6,
            "risk": 3,
            "resource": 4,
            "ethics": 8,
            "preference": 7,
            "description": "Use continued monitoring and supportive management where appropriate."
        }
    ]


def calculate_mcdm(options):
    weights = {
        "Expected Benefit": 0.30,
        "Safety": 0.25,
        "Recovery Probability": 0.20,
        "Resource Availability": 0.10,
        "Ethical Acceptability": 0.10,
        "Patient Preference": 0.05
    }

    scores = {}

    for option in options:
        # Transparent prototype scoring
        safety_score = 10 - option["risk"]

        scores[option["name"]] = {
            "Expected Benefit": option["benefit"],
            "Safety": safety_score,
            "Recovery Probability": option["benefit"],
            "Resource Availability": 10 - option["resource"],
            "Ethical Acceptability": option["ethics"],
            "Patient Preference": option["preference"]
        }

    totals = {}

    for option_name, criteria in scores.items():
        total = 0

        for criterion, value in criteria.items():
            total += value * weights[criterion]

        totals[option_name] = round(total / 10, 2)

    ranking = sorted(
        totals.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return weights, scores, totals, ranking


def stakeholder_summary(case):
    opinions = case.get("stakeholders", {})

    counts = {}

    for data in opinions.values():
        choice = data.get("choice")

        if choice:
            counts[choice] = counts.get(choice, 0) + 1

    total = len(opinions)

    if not counts or total == 0:
        return 0, None, counts

    most_common = max(counts, key=counts.get)
    agreement = round((counts[most_common] / total) * 100)

    return agreement, most_common, counts


def get_selected_case(case_id):
    for case in st.session_state.cases:
        if case["case_id"] == case_id:
            return case
    return None


# ============================================================
# DEFAULT DEMO CASE P001
# ============================================================

if len(st.session_state.cases) == 0:

    demo_options = generate_options(
        "Cardiovascular Diseases & Hypertension"
    )

    demo_case = {
        "case_id": "CASE-001",
        "patient_id": "P001",
        "age": 45,
        "gender": "Male",

        "problem": "Cardiovascular Diseases & Hypertension",

        "medical_history": [
            "Hypertension — 5 years",
            "Type 2 Diabetes — 3 years",
            "No known drug allergies",
            "Family history of heart disease"
        ],

        "allergies": "No known drug allergies",

        "medications": "Current antihypertensive and diabetic medication",

        "symptoms": "Chest pain, fatigue and shortness of breath",

        "vitals": {
            "Blood Pressure": "150/95 mmHg",
            "Heart Rate": "96 bpm",
            "Temperature": "37.5 °C",
            "SpO₂": "94%"
        },

        "findings": [
            "Chest pain",
            "Fatigue",
            "Shortness of breath"
        ],

        "investigations": [
            "ECG — requires clinical interpretation",
            "Blood pressure monitoring",
            "Blood glucose assessment",
            "Cardiac biomarker assessment"
        ],

        "current_care": "Currently under clinical observation and routine management.",

        "response_to_care": "Symptoms require further clinical review.",

        "time_sensitive": "Within 24 hours",

        "initial_urgency": "High",

        "critical_flag": False,

        "urgency": "High",

        "ethical_issue": "Balancing timely intervention with patient safety and resource considerations.",

        "options": demo_options,

        "stakeholders": {
            "Treating Doctor": {
                "choice": "A — Immediate Intervention",
                "reason": "Concern about the patient's symptoms and need for timely clinical action.",
                "risk": "Moderate"
            },

            "Independent Physician": {
                "choice": "B — Further Investigation",
                "reason": "Would prefer additional evidence before escalation.",
                "risk": "Moderate"
            },

            "Ethics Committee": {
                "choice": "B — Further Investigation",
                "reason": "Supports proportional decision-making while considering safety and patient autonomy.",
                "risk": "Low"
            },

            "Patient": {
                "choice": "C — Conservative Management",
                "reason": "Prefers to avoid immediate escalation unless clearly necessary.",
                "risk": "Moderate"
            }
        },

        "status": "Active",
        "assigned_to": "Dr. Sharma",
        "final_decision": "",
        "decision_justification": "",
        "human_reviewed": False,
        "created": now()
    }

    st.session_state.cases.append(demo_case)

    add_audit(
        "CASE-001",
        "System",
        "Case Created",
        "Demo case P001 created for prototype demonstration."
    )

    add_audit(
        "CASE-001",
        "System",
        "Clinical Analysis",
        "Clinical information loaded for decision-support analysis."
    )

    add_audit(
        "CASE-001",
        "System",
        "Urgency Assessment",
        "Urgency classified as High based on time-sensitive clinical inputs."
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "<h2 style='color:white;'>⚕️ EthicSync</h2>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<p style='color:#b8d4e8;'>Clinical Decision Support</p>",
    unsafe_allow_html=True
)

pages = [
    "🏠 Dashboard",
    "➕ New Case",
    "📁 Cases",
    "🚨 Patient Care Urgency",
    "🧬 Clinical Information",
    "🤖 AI Decision Support",
    "📊 MCDM Analysis",
    "⚖️ Trade-off Analysis",
    "👥 Stakeholder Opinions",
    "🤝 Consensus Management",
    "🔍 Decision Transparency",
    "✅ Final Human Decision",
    "📜 Audit Trail",
    "🔔 Notifications",
    "⚙️ Settings"
]

page = st.sidebar.radio("Navigation", pages)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**EthicSync Prototype**\n\n"
    "AI-assisted clinical decision support with "
    "human oversight."
)


# ============================================================
# COMMON CASE SELECTOR
# ============================================================

case_ids = [case["case_id"] for case in st.session_state.cases]

if "selected_case_id" not in st.session_state:
    st.session_state.selected_case_id = case_ids[0]

if st.session_state.selected_case_id not in case_ids:
    st.session_state.selected_case_id = case_ids[0]

selected_case = get_selected_case(
    st.session_state.selected_case_id
)


# ============================================================
# 1. DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("Welcome, Dr. Priya 👋")
    st.caption("Better decisions. Clearer reasoning. Human oversight.")

    total_cases = len(st.session_state.cases)
    active = len([
        c for c in st.session_state.cases
        if c["status"] == "Active"
    ])

    urgent = len([
        c for c in st.session_state.cases
        if c["urgency"] in ["High", "Critical"]
    ])

    pending = len([
        c for c in st.session_state.cases
        if not c["human_reviewed"]
    ])

    agreements = []

    for c in st.session_state.cases:
        agreement, _, _ = stakeholder_summary(c)
        agreements.append(agreement)

    consensus_count = len([
        a for a in agreements
        if a >= 75
    ])

    st.subheader("Overall Case Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
            <h4>Active Cases</h4>
            <h1>{active}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
            <h4>Pending Reviews</h4>
            <h1>{pending}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
            <h4>Urgent Cases</h4>
            <h1>{urgent}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
            <h4>Consensus Status</h4>
            <h1>{consensus_count}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Quick Access")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("➕ New Case", use_container_width=True):
            st.info("Use 'New Case' from the sidebar.")

    with q2:
        if st.button("📁 Cases", use_container_width=True):
            st.info("Use 'Cases' from the sidebar.")

    with q3:
        if st.button("🚨 Patient Urgency", use_container_width=True):
            st.info("Use 'Patient Care Urgency' from the sidebar.")

    with q4:
        if st.button("🤖 AI Decision Support", use_container_width=True):
            st.info("Use 'AI Decision Support' from the sidebar.")

    st.subheader("Recent Activity")

    if st.session_state.audit:

        for item in st.session_state.audit[:5]:

            st.markdown(
                f"""
                <div class="card">
                <b>{item['action']}</b><br>
                <span class="small-text">
                {item['case_id']} · {item['time']} · {item['user']}
                </span><br>
                {item['details']}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# 2. NEW CASE
# ============================================================

elif page == "➕ New Case":

    st.title("Create New Case")

    st.markdown(
        '<div class="info-card">'
        'Enter the available clinical information. '
        'The system will automatically generate the decision-support workflow.'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader("Patient Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        patient_id = st.text_input(
            "Patient ID",
            value="P002"
        )

    with col2:
        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=40
        )

    with col3:
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other / Not specified"]
        )

    problem = st.selectbox(
        "Health Problem",
        HEALTH_PROBLEMS
    )

    st.subheader("Clinical Information")

    history = st.text_area(
        "Medical History",
        placeholder="Previous diseases, family history, allergies..."
    )

    symptoms = st.text_area(
        "Current Symptoms / Clinical Status",
        placeholder="Describe current symptoms and important findings..."
    )

    investigations = st.text_area(
        "Investigations",
        placeholder="ECG, laboratory findings, imaging, etc."
    )

    current_care = st.text_area(
        "Current Care",
        placeholder="Current management / observation / treatment status..."
    )

    response = st.text_area(
        "Response to Current Care",
        placeholder="Improving, stable, worsening, etc."
    )

    st.subheader("Urgency")

    u1, u2, u3 = st.columns(3)

    with u1:
        initial_urgency = st.selectbox(
            "Clinical urgency",
            ["Low", "Medium", "High"]
        )

    with u2:
        time_sensitive = st.selectbox(
            "Time sensitivity",
            [
                "Routine",
                "Within 72 hours",
                "Within 24 hours"
            ]
        )

    with u3:
        critical = st.checkbox(
            "Critical-care flag"
        )

    ethical_issue = st.text_area(
        "Ethical Issue",
        placeholder="Example: patient preference vs urgency..."
    )

    if st.button(
        "Create Case & Generate Options",
        type="primary",
        use_container_width=True
    ):

        new_number = len(st.session_state.cases) + 1

        case_id = f"CASE-{new_number:03d}"

        urgency = calculate_urgency(
            initial_urgency,
            time_sensitive,
            critical
        )

        option_data = generate_options(problem)

        new_case = {
            "case_id": case_id,
            "patient_id": patient_id,
            "age": age,
            "gender": gender,
            "problem": problem,

            "medical_history": [
                history if history else "No history entered."
            ],

            "allergies": "Not specified",
            "medications": "Not specified",
            "symptoms": symptoms,
            "vitals": {},
            "findings": [],

            "investigations": [
                investigations if investigations
                else "No investigations entered."
            ],

            "current_care": current_care,
            "response_to_care": response,

            "time_sensitive": time_sensitive,
            "initial_urgency": initial_urgency,
            "critical_flag": critical,
            "urgency": urgency,

            "ethical_issue": ethical_issue,

            "options": option_data,

            "stakeholders": {
                "Treating Doctor": {
                    "choice": "",
                    "reason": "",
                    "risk": "Not assessed"
                },
                "Independent Physician": {
                    "choice": "",
                    "reason": "",
                    "risk": "Not assessed"
                },
                "Ethics Committee": {
                    "choice": "",
                    "reason": "",
                    "risk": "Not assessed"
                },
                "Patient": {
                    "choice": "",
                    "reason": "",
                    "risk": "Not assessed"
                }
            },

            "status": "Active",
            "assigned_to": "Dr. Sharma",
            "final_decision": "",
            "decision_justification": "",
            "human_reviewed": False,
            "created": now()
        }

        st.session_state.cases.append(new_case)

        st.session_state.selected_case_id = case_id

        add_audit(
            case_id,
            "System",
            "Case Created",
            f"New case created for patient {patient_id}."
        )

        add_audit(
            case_id,
            "System",
            "Options Generated",
            "Three concise decision alternatives generated."
        )

        if urgency in ["High", "Critical"]:

            add_notification(
                f"Urgent case {case_id} requires clinical review.",
                "Urgent"
            )

        st.success(
            f"Case {case_id} created successfully."
        )

        st.info(
            "Three decision options have been automatically generated."
        )


# ============================================================
# 3. CASES
# ============================================================

elif page == "📁 Cases":

    st.title("Cases")

    search = st.text_input(
        "🔎 Search by Patient ID, Case ID or condition"
    )

    filtered = []

    for case in st.session_state.cases:

        searchable = (
            case["case_id"] +
            case["patient_id"] +
            case["problem"]
        ).lower()

        if search.lower() in searchable:
            filtered.append(case)

    st.write(f"Showing **{len(filtered)}** case(s)")

    for case in filtered:

        urgency_icon = urgency_color(case["urgency"])

        with st.container():

            st.markdown(
                f"""
                <div class="card">
                <h3>{case['case_id']} — {case['patient_id']}</h3>
                <b>Condition:</b> {case['problem']}<br>
                <b>Status:</b> {case['status']}<br>
                <b>Urgency:</b> {urgency_icon} {case['urgency']}<br>
                <b>Assigned to:</b> {case['assigned_to']}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"Open {case['case_id']}",
                key=f"open_{case['case_id']}"
            ):
                st.session_state.selected_case_id = case["case_id"]
                st.success(
                    f"{case['case_id']} selected."
                )


# ============================================================
# 4. PATIENT CARE URGENCY
# ============================================================

elif page == "🚨 Patient Care Urgency":

    st.title("Urgency Assessment")

    selected_id = st.selectbox(
        "Select Case",
        case_ids,
        index=case_ids.index(
            st.session_state.selected_case_id
        )
    )

    case = get_selected_case(selected_id)

    st.session_state.selected_case_id = selected_id

    st.markdown(
        f"""
        <div class="card">
        <b>Patient ID:</b> {case['patient_id']}<br>
        <b>Condition:</b> {case['problem']}<br>
        <b>Urgency:</b> {urgency_color(case['urgency'])} {case['urgency']}<br>
        <b>Time Sensitivity:</b> {case['time_sensitive']}
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Urgency Level",
            case["urgency"]
        )

    with c2:
        st.metric(
            "Time Window",
            case["time_sensitive"]
        )

    with c3:
        st.metric(
            "Critical Flag",
            "Yes" if case["critical_flag"] else "No"
        )

    st.subheader("Priority Alerts")

    alerts = []

    if case["urgency"] in ["High", "Critical"]:
        alerts.append(
            "High clinical urgency detected."
        )

    if case["time_sensitive"] != "Routine":
        alerts.append(
            "Urgency review may be required."
        )

    if not case["human_reviewed"]:
        alerts.append(
            "Human clinical review recommended."
        )

    for alert in alerts:
        st.warning("⚠️ " + alert)

    if case["urgency"] in ["High", "Critical"]:
        st.markdown(
            """
            <div class="danger-card">
            <b>⚠️ Urgent case flagged.</b><br>
            Please review the clinical information and decision alternatives.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 5. CLINICAL INFORMATION
# ============================================================

elif page == "🧬 Clinical Information":

    st.title("Clinical Information")

    selected_id = st.selectbox(
        "Select Case",
        case_ids
    )

    case = get_selected_case(selected_id)
    st.session_state.selected_case_id = selected_id

    st.markdown(
        f"""
        <div class="card">
        <h3>{case['patient_id']}</h3>
        <b>Age:</b> {case['age']} |
        <b>Gender:</b> {case['gender']}<br>
        <b>Condition:</b> {case['problem']}<br>
        <b>Urgency:</b> {urgency_color(case['urgency'])} {case['urgency']}
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Medical History",
        "Current Status",
        "Investigations",
        "Current Care",
        "Decision Options"
    ])

    with tab1:

        st.subheader("Medical History")

        for item in case["medical_history"]:
            st.markdown("• " + item)

        st.write(
            "**Allergies:**",
            case["allergies"]
        )

        st.write(
            "**Current Medications:**",
            case["medications"]
        )

    with tab2:

        st.subheader("Current Clinical Status")

        st.write(case["symptoms"])

        if case["vitals"]:

            for key, value in case["vitals"].items():

                st.metric(
                    key,
                    value
                )

        if case["findings"]:

            st.subheader("Relevant Findings")

            for finding in case["findings"]:
                st.markdown("• " + finding)

    with tab3:

        st.subheader("Clinical Investigations")

        for item in case["investigations"]:
            st.markdown("• " + item)

    with tab4:

        st.subheader("Current Care")

        st.write(
            case["current_care"]
        )

        st.subheader("Response to Care")

        st.write(
            case["response_to_care"]
        )

    with tab5:

        st.subheader("Available Decision Options")

        for option in case["options"]:

            st.markdown(
                f"""
                <div class="option-card">
                <h3>{option['name']}</h3>
                <b>Urgency:</b> {option['urgency']}<br>
                {option['description']}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# 6. AI DECISION SUPPORT
# ============================================================

elif page == "🤖 AI Decision Support":

    st.title("AI Decision Support")

    selected_id = st.selectbox(
        "Select Case",
        case_ids
    )

    case = get_selected_case(selected_id)
    st.session_state.selected_case_id = selected_id

    st.subheader("AI Analysis")

    st.markdown(
        """
        <div class="info-card">
        <b>Clinical Information Analysis</b><br>
        Key clinical information has been organized for decision support.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">
        <b>Ethical Issue Identification</b><br>
        Potential ethical considerations are highlighted for human review.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">
        <b>Scenario Analysis</b><br>
        The available decision alternatives are compared using transparent
        prototype scoring.
        </div>
        """,
        unsafe_allow_html=True
    )

    weights, scores, totals, ranking = calculate_mcdm(
        case["options"]
    )

    best_option = ranking[0][0]

    st.markdown(
        f"""
        <div class="success-card">
        <h3>🤖 Suggested Option</h3>
        <h2>{best_option}</h2>
        <b>Reasoning:</b><br>
        This option currently provides the highest weighted score under
        the prototype's predefined criteria.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### Key Factors")

    st.write(
        "• Expected benefit\n"
        "\n• Safety\n"
        "\n• Recovery probability\n"
        "\n• Resource availability\n"
        "\n• Ethical acceptability\n"
        "\n• Patient preference"
    )

    st.warning(
        "This is an AI-assisted decision-support prototype. "
        "It does not diagnose, prescribe, or replace professional clinical judgment."
    )


# ============================================================
# 7. MCDM ANALYSIS
# ============================================================

elif page == "📊 MCDM Analysis":

    st.title("MCDM Analysis")

    selected_id = st.selectbox(
        "Select Case",
        case_ids
    )

    case = get_selected_case(selected_id)
    st.session_state.selected_case_id = selected_id

    weights, scores, totals, ranking = calculate_mcdm(
        case["options"]
    )

    st.subheader("Selected Criteria & Weights")

    weight_cols = st.columns(3)

    for i, (criterion, weight) in enumerate(weights.items()):

        with weight_cols[i % 3]:
            st.metric(
                criterion,
                f"{weight * 100:.0f}%"
            )

    st.subheader("Option Scores")

    for option in case["options"]:

        st.markdown(
            f"### {option['name']}"
        )

        score_cols = st.columns(6)

        values = [
            option["benefit"],
            10 - option["risk"],
            option["benefit"],
            10 - option["resource"],
            option["ethics"],
            option["preference"]
        ]

        for i, value in enumerate(values):

            with score_cols[i]:

                labels = [
                    "Benefit",
                    "Safety",
                    "Recovery",
                    "Resources",
                    "Ethics",
                    "Preference"
                ]

                st.metric(
                    labels[i],
                    f"{value}/10"
                )

    st.subheader("Weighted Calculation")

    st.markdown(
        """
        **Weighted Score = Σ (Criterion Weight × Criterion Score)**

        Each criterion contributes according to its predefined weight.
        """
    )

    for option_name, total in totals.items():

        st.write(
            f"**{option_name} = {total:.2f} / 1.00**"
        )

        st.progress(
            min(float(total), 1.0)
        )

    st.subheader("Ranking")

    for rank, (option, score) in enumerate(ranking, start=1):

        medal = ["🥇", "🥈", "🥉"][rank - 1]

        st.markdown(
            f"""
            <div class="card">
            <h3>{medal} {rank}. {option}</h3>
            <div class="big-score">{score:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 8. TRADE-OFF ANALYSIS
# ============================================================

elif page == "⚖️ Trade-off Analysis":

    st.title("Trade-off Analysis")

    selected_id = st.selectbox(
        "Select Case",
        case_ids
    )

    case = get_selected_case(selected_id)
    st.session_state.selected_case_id = selected_id

    weights, scores, totals, ranking = calculate_mcdm(
        case["options"]
    )

    st.markdown(
        """
        <div class="info-card">
        Trade-off analysis compares expected benefit, safety,
        resources, ethical acceptability and patient preference.
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Benefits vs Risks",
        "Resources",
        "Ethical Factors",
        "Patient Preference"
    ])

    with tab1:

        st.subheader("Benefits vs Risks")

        for option in case["options"]:

            benefit = option["benefit"]
            risk = option["risk"]

            tradeoff = benefit - risk

            st.markdown(
                f"""
                <div class="option-card">
                <h3>{option['name']}</h3>
                <b>Expected Benefit:</b> {benefit}/10<br>
                <b>Risk Burden:</b> {risk}/10<br>
                <b>Benefit − Risk:</b> {tradeoff:+d}<br>
                <b>Urgency:</b> {option['urgency']}
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab2:

        st.subheader("Resource Trade-off")

        for option in case["options"]:

            resource = option["resource"]

            st.write(
                f"**{option['name']}** — Resource burden: "
                f"{resource}/10"
            )

            st.progress(
                resource / 10
            )

    with tab3:

        st.subheader("Ethical Acceptability")

        for option in case["options"]:

            st.write(
                f"**{option['name']}** — "
                f"{option['ethics']}/10"
            )

    with tab4:

        st.subheader("Patient Preference")

        for option in case["options"]:

            st.write(
                f"**{option['name']}** — "
                f"{option['preference']}/10"
            )

    st.subheader("Overall Mathematical Trade-off")

    for option_name, score in totals.items():

        st.write(
            f"**{option_name} → Weighted utility = {score:.2f}**"
        )

    st.success(
        f"Current mathematical ranking: "
        f"**{ranking[0][0]}** with a score of "
        f"**{ranking[0][1]:.2f}**."
    )


# ============================================================
# 9. STAKEHOLDER OPINIONS
# ============================================================

elif page == "👥 Stakeholder Opinions":

    st.title("Stakeholder Opinions")

    selected_id = st.selectbox(
        "Select Case",
        case_ids
    )

    case = get_selected_case(selected_id)
    st.session_state.selected_case_id = selected_id

    stakeholder_names = [
        "Treating Doctor",
        "Independent Physician",
        "Ethics Committee",
        "Patient"
    ]

    option_names = [
        option["name"]
        for option in case["options"]
    ]

    for stakeholder in stakeholder_names:

        data = case["stakeholders"][stakeholder]

        st.markdown(
            f"""
            <div class="stakeholder">
            <h3>👤 {stakeholder}</h3>
            <b>Current Preference:</b>
            {data.get('choice', 'Not provided')}<br>
            <b>Risk Assessment:</b>
            {data.get('risk', 'Not assessed')}<br>
            <b>Reason:</b>
            {data.get('reason', 'Not provided')}
            </div>
            """,
            unsafe_allow_html=True
        )

        choice = st.selectbox(
            f"{stakeholder} — preferred option",
            ["Not selected"] + option_names,
            index=(
                option_names.index(data["choice"]) + 1
                if data.get("choice") in option_names
                else 0
            ),
            key=f"choice_{selected_id}_{stakeholder}"
        )

        reason = st.text_area(
            f"{stakeholder} — reasoning",
            value=data.get("reason", ""),
            key=f"reason_{selected_id}_{stakeholder}"
        )

        if st.button(
            f"Save {stakeholder}",
            key=f"save_{selected_id}_{stakeholder}"
        ):

            if choice != "Not selected":

                case["stakeholders"][stakeholder]["choice"] = choice

            case["stakeholders"][stakeholder]["reason"] = reason

            add_audit(
                selected_id,
                stakeholder,
                "Opinion Added",
                f"Preferred option: {choice}"
            )

            st.success(
                f"{stakeholder} opinion saved."
            )

    agreement, common_choice, counts = stakeholder_summary(
        case
    )

    st.subheader("Opinion Comparison")

    if common_choice:

        st.metric(
            "Current Agreement",
            f"{agreement}%"
        )

        for option in option_names:

            count = counts.get(option, 0)

            st.write(
                f"**{option}** — {count} stakeholder(s)"
            )

            st.progress(
                count / 4
            )

        if agreement < 75:

            st.error(
                "⚠️ Stakeholder disagreement detected."
            )

        else:

            st.success(
                "Stakeholder agreement is currently strong."
            )


# ============================================================
# 10. CONSENSUS MANAGEMENT
# ============================================================

elif page == "🤝 Consensus Management":

    st.title("Consensus Management")

    selected_id = st.selectbox(
        "Select Case",
        case_ids
    )

    case = get_selected_case(selected_id)
    st.session_state.selected_case_id = selected_id

    agreement, common_choice, counts = stakeholder_summary(
        case
    )

    st.metric(
        "Consensus Percentage",
        f"{agreement}%"
    )

    if agreement >= 75:
        st.success(
            f"Consensus status: Strong agreement around {common_choice}"
        )
    else:
        st.warning(
            "Consensus status: Partial consensus / disagreement"
        )

    st.subheader("Opinion Comparison")

    stakeholders = case["stakeholders"]

    for person, data in stakeholders.items():

        choice = data.get(
            "choice",
            "Not selected"
        )

        st.markdown(
            f"""
            <div class="card">
            <b>{person}</b><br>
            Preference: {choice}<br>
            Reason: {data.get('reason', '')}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Consensus Actions")

    a1, a2 = st.columns(2)

    with a1:

        if st.button(
            "Request Discussion",
            use_container_width=True
        ):

            add_notification(
                f"Discussion requested for {selected_id}.",
                "Pending"
            )

            add_audit(
                selected_id,
                "System",
                "Consensus Discussion",
                "Stakeholder discussion requested."
            )

            st.success(
                "Discussion request recorded."
            )

    with a2:

        if st.button(
            "Request Further Review",
            use_container_width=True
        ):

            add_notification(
                f"Further review requested for {selected_id}.",
                "Pending"
            )

            add_audit(
                selected_id,
                "System",
                "Further Review",
                "Additional clinical review requested."
            )

            st.success(
                "Further review recorded."
            )


# ============================================================
# 11. DECISION TRANSPARENCY
# ============================================================

elif page == "🔍 Decision Transparency":

    st.title("Decision Transparency")

    selected_id = st.selectbox(
        "Select Case",
        case_ids
    )

    case = get_selected_case(selected_id)
    st.session_state.selected_case_id = selected_id

    weights, scores, totals, ranking = calculate_mcdm(
        case["options"]
    )

    agreement, common_choice, counts = stakeholder_summary(
        case
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Evidence",
        "Data Sources",
        "Calculations",
        "History"
    ])

    with tab1:

        st.subheader("Evidence Considered")

        evidence = [
            "Clinical history",
            "Current clinical status",
            "Relevant symptoms/findings",
            "Clinical investigations",
            "Current care",
            "Urgency and time sensitivity",
            "Ethical issue",
            "Patient preference"
        ]

        for item in evidence:
            st.markdown("✦ " + item)

    with tab2:

        st.subheader("Clinical Data Sources")

        st.write(
            "• Patient-entered clinical information"
        )

        st.write(
            "• Clinical investigation information"
        )

        st.write(
            "• Stakeholder opinions"
        )

        st.write(
            "• Prototype MCDM criteria"
        )

    with tab3:

        st.subheader("MCDM Calculation")

        for criterion, weight in weights.items():

            st.write(
                f"{criterion}: {weight * 100:.0f}%"
            )

        st.markdown("---")

        for option, score in totals.items():

            st.write(
                f"**{option} → {score:.2f}**"
            )

        st.subheader("Stakeholder Agreement")

        st.write(
            f"Consensus percentage: **{agreement}%**"
        )

        if common_choice:
            st.write(
                f"Most selected stakeholder option: "
                f"**{common_choice}**"
            )

    with tab4:

        st.subheader("Decision History")

        history = [
            item
            for item in st.session_state.audit
            if item["case_id"] == selected_id
        ]

        for item in history:

            st.markdown(
                f"""
                **{item['time']}** — {item['action']}  
                {item['user']}: {item['details']}
                """
            )


# ============================================================
# 12. FINAL HUMAN DECISION
# ============================================================

elif page == "✅ Final Human Decision":

    st.title("Final Human Decision")

    selected_id = st.selectbox(
        "Select Case",
        case_ids
    )

    case = get_selected_case(selected_id)
    st.session_state.selected_case_id = selected_id

    weights, scores, totals, ranking = calculate_mcdm(
        case["options"]
    )

    ai_recommendation = ranking[0][0]

    st.markdown(
        f"""
        <div class="success-card">
        <h3>🤖 AI Recommendation</h3>
        <h2>{ai_recommendation}</h2>
        <b>Mathematical Score:</b>
        {ranking[0][1]:.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Human Review")

    decision_options = [
        option["name"]
        for option in case["options"]
    ]

    final_choice = st.radio(
        "Final decision",
        decision_options,
        index=decision_options.index(
            ai_recommendation
        )
    )

    review_type = st.radio(
        "Human review",
        [
            "Accept AI recommendation",
            "Modify AI recommendation",
            "Reject AI recommendation"
        ]
    )

    justification = st.text_area(
        "Decision Justification",
        value=case.get(
            "decision_justification",
            ""
        ),
        placeholder="Explain the human decision..."
    )

    reviewed = st.checkbox(
        "I confirm that this decision has undergone human review."
    )

    if st.button(
        "Record Final Decision",
        type="primary",
        use_container_width=True
    ):

        if not reviewed:

            st.error(
                "Please confirm human review before recording the decision."
            )

        else:

            case["final_decision"] = final_choice

            case["decision_justification"] = justification

            case["human_reviewed"] = True

            case["status"] = "Decision Recorded"

            add_audit(
                selected_id,
                "Dr. Priya",
                "Final Decision Recorded",
                f"Final decision: {final_choice}. "
                f"Review type: {review_type}."
            )

            add_notification(
                f"Final human decision recorded for {selected_id}.",
                "Info"
            )

            st.success(
                "Final human decision recorded successfully."
            )


# ============================================================
# 13. AUDIT TRAIL
# ============================================================

elif page == "📜 Audit Trail":

    st.title("Audit Trail")

    case_filter = st.selectbox(
        "Filter by Case",
        ["All Cases"] + case_ids
    )

    action_filter = st.selectbox(
        "Filter by Action",
        ["All Actions"] +
        sorted(
            list(
                set(
                    item["action"]
                    for item in st.session_state.audit
                )
            )
        )
    )

    records = st.session_state.audit

    if case_filter != "All Cases":

        records = [
            x for x in records
            if x["case_id"] == case_filter
        ]

    if action_filter != "All Actions":

        records = [
            x for x in records
            if x["action"] == action_filter
        ]

    for item in records:

        st.markdown(
            f"""
            <div class="card">
            <b>{item['action']}</b><br>
            <span class="small-text">
            {item['time']} · {item['user']} · {item['case_id']}
            </span><br>
            {item['details']}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 14. NOTIFICATIONS
# ============================================================

elif page == "🔔 Notifications":

    st.title("Notifications")

    urgent_count = len([
        c for c in st.session_state.cases
        if c["urgency"] in ["High", "Critical"]
    ])

    pending_count = len([
        c for c in st.session_state.cases
        if not c["human_reviewed"]
    ])

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Urgent Cases",
            urgent_count
        )

    with c2:
        st.metric(
            "Pending Reviews",
            pending_count
        )

    with c3:
        st.metric(
            "Notifications",
            len(st.session_state.notifications)
        )

    st.subheader("Recent Notifications")

    if not st.session_state.notifications:

        st.info(
            "No additional notifications."
        )

    else:

        for notification in st.session_state.notifications:

            level = notification["level"]

            if level == "Urgent":
                st.error(
                    "🚨 " + notification["message"]
                )

            elif level == "Pending":
                st.warning(
                    "⚠️ " + notification["message"]
                )

            else:
                st.success(
                    "✓ " + notification["message"]
                )


# ============================================================
# 15. SETTINGS
# ============================================================

elif page == "⚙️ Settings":

    st.title("Settings")

    st.subheader("Prototype Configuration")

    st.checkbox(
        "AI Decision Support",
        value=True
    )

    st.checkbox(
        "Human Review Required",
        value=True
    )

    st.checkbox(
        "Audit Trail",
        value=True
    )

    st.checkbox(
        "Stakeholder Consensus Monitoring",
        value=True
    )

    st.subheader("MCDM Criteria")

    criteria = {
        "Expected Benefit": "30%",
        "Safety": "25%",
        "Recovery Probability": "20%",
        "Resource Availability": "10%",
        "Ethical Acceptability": "10%",
        "Patient Preference": "5%"
    }

    for criterion, value in criteria.items():

        st.write(
            f"**{criterion}** — {value}"
        )

    st.info(
        "The criteria and weights are predefined for this prototype. "
        "They can be made configurable in a future version."
    )


# ============================================================
# PRINTABLE CASE REPORT
# ============================================================

st.sidebar.markdown("---")

if st.sidebar.button(
    "🖨️ Generate Case Report",
    use_container_width=True
):

    case = selected_case

    weights, scores, totals, ranking = calculate_mcdm(
        case["options"]
    )

    agreement, common_choice, counts = stakeholder_summary(
        case
    )

    stakeholder_html = ""

    for person, data in case["stakeholders"].items():

        stakeholder_html += f"""
        <tr>
            <td>{html.escape(person)}</td>
            <td>{html.escape(data.get("choice", ""))}</td>
            <td>{html.escape(data.get("reason", ""))}</td>
        </tr>
        """

    option_html = ""

    for option in case["options"]:

        option_html += f"""
        <tr>
            <td>{html.escape(option["name"])}</td>
            <td>{option["urgency"]}</td>
            <td>{option["benefit"]}/10</td>
            <td>{option["risk"]}/10</td>
            <td>{totals[option["name"]]:.2f}</td>
        </tr>
        """

    report = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>EthicSync Case Report - {case['case_id']}</title>

    <style>

    body {{
        font-family: Arial, sans-serif;
        margin: 40px;
        color: #222;
    }}

    h1 {{
        color: #123b5d;
    }}

    h2 {{
        color: #195d85;
        border-bottom: 1px solid #ccc;
        padding-bottom: 5px;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 25px;
    }}

    th, td {{
        border: 1px solid #ccc;
        padding: 8px;
        text-align: left;
    }}

    th {{
        background: #edf5fa;
    }}

    .box {{
        border: 1px solid #ccc;
        padding: 15px;
        margin-bottom: 15px;
    }}

    .warning {{
        background: #fff4d6;
        padding: 15px;
        border: 1px solid #e4c66b;
    }}

    @media print {{
        .no-print {{
            display: none;
        }}
    }}

    </style>

    </head>

    <body>

    <h1>⚕️ EthicSync</h1>
    <h3>Clinical Decision Support Report</h3>

    <div class="box">
    <b>Case ID:</b> {case['case_id']}<br>
    <b>Patient ID:</b> {case['patient_id']}<br>
    <b>Age:</b> {case['age']}<br>
    <b>Gender:</b> {case['gender']}<br>
    <b>Condition:</b> {case['problem']}<br>
    <b>Urgency:</b> {case['urgency']}<br>
    <b>Time Sensitivity:</b> {case['time_sensitive']}<br>
    <b>Status:</b> {case['status']}
    </div>

    <h2>Clinical Summary</h2>

    <div class="box">
    <b>Symptoms / Clinical Status</b><br>
    {html.escape(case['symptoms'])}
    </div>

    <div class="box">
    <b>Medical History</b><br>
    {'<br>'.join([html.escape(x) for x in case['medical_history']])}
    </div>

    <div class="box">
    <b>Investigations</b><br>
    {'<br>'.join([html.escape(x) for x in case['investigations']])}
    </div>

    <div class="box">
    <b>Current Care</b><br>
    {html.escape(case['current_care'])}
    </div>

    <div class="box">
    <b>Response to Care</b><br>
    {html.escape(case['response_to_care'])}
    </div>

    <h2>Urgency Assessment</h2>

    <div class="box">
    <b>Urgency Level:</b> {case['urgency']}<br>
    <b>Time Sensitivity:</b> {case['time_sensitive']}<br>
    <b>Critical Flag:</b> {'Yes' if case['critical_flag'] else 'No'}
    </div>

    <h2>Ethical Issue</h2>

    <div class="box">
    {html.escape(case['ethical_issue'])}
    </div>

    <h2>Available Decision Options</h2>

    <table>
    <tr>
        <th>Option</th>
        <th>Urgency</th>
        <th>Benefit</th>
        <th>Risk</th>
        <th>Weighted Score</th>
    </tr>

    {option_html}

    </table>

    <h2>MCDM Calculation</h2>

    <div class="box">

    <b>Formula:</b><br>

    Weighted Score = Σ (Criterion Weight × Criterion Score)

    <br><br>

    <b>Criteria:</b><br>

    Expected Benefit: 30%<br>
    Safety: 25%<br>
    Recovery Probability: 20%<br>
    Resource Availability: 10%<br>
    Ethical Acceptability: 10%<br>
    Patient Preference: 5%

    </div>

    <h2>Ranking</h2>

    <ol>
    """

    for option, score in ranking:

        report += f"""
        <li>
        <b>{html.escape(option)}</b>
        — {score:.2f}
        </li>
        """

    report += f"""

    </ol>

    <h2>Stakeholder Opinions</h2>

    <table>

    <tr>
        <th>Stakeholder</th>
        <th>Preferred Option</th>
        <th>Reasoning</th>
    </tr>

    {stakeholder_html}

    </table>

    <h2>Consensus</h2>

    <div class="box">

    <b>Consensus Percentage:</b> {agreement}%<br>

    <b>Most Selected Option:</b>
    {html.escape(common_choice or 'Not available')}

    </div>

    <h2>Final Human Decision</h2>

    <div class="box">

    <b>Final Decision:</b>
    {html.escape(case.get('final_decision', '') or 'Not recorded')}
    <br><br>

    <b>Human Review:</b>
    {'Completed' if case.get('human_reviewed') else 'Pending'}

    <br><br>

    <b>Justification:</b><br>
    {html.escape(case.get('decision_justification', '') or 'Not recorded')}

    </div>

    <h2>Audit History</h2>

    <table>

    <tr>
        <th>Date / Time</th>
        <th>User</th>
        <th>Action</th>
        <th>Details</th>
    </tr>
    """

    for item in st.session_state.audit:

        if item["case_id"] == case["case_id"]:

            report += f"""
            <tr>
                <td>{html.escape(item['time'])}</td>
                <td>{html.escape(item['user'])}</td>
                <td>{html.escape(item['action'])}</td>
                <td>{html.escape(item['details'])}</td>
            </tr>
            """

    report += """

    </table>

    <div class="warning">

    <b>Human Review Disclaimer</b><br>

    EthicSync is a clinical decision-support prototype.
    Its outputs are intended to organize information,
    compare decision alternatives and improve transparency.
    It does not diagnose disease, prescribe treatment or replace
    qualified healthcare professionals.

    </div>

    <br>

    <button class="no-print" onclick="window.print()">
    Print / Save as PDF
    </button>

    </body>
    </html>
    """

    st.sidebar.download_button(
        "📄 Download Printable Report",
        data=report,
        file_name=f"{case['case_id']}_EthicSync_Report.html",
        mime="text/html",
        use_container_width=True
    )

    st.sidebar.success(
        "Report generated. Open the HTML file and choose Print → Save as PDF."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "EthicSync • AI-assisted clinical decision-support prototype • "
    "Human oversight required"
)
