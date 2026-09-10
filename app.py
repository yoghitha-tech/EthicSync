import streamlit as st
import json
import csv
import re
import io
from datetime import datetime

# Optional file readers
try:
    from PyPDF2 import PdfReader
except:
    PdfReader = None

try:
    from docx import Document
except:
    Document = None

try:
    from openpyxl import load_workbook
except:
    load_workbook = None


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EthicSync",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DARK + LIGHT MODE SAFE CSS
# ============================================================

st.markdown("""
<style>

    /* Main application */
    .stApp {
        background-color: #f7f9fc;
        color: #172033;
    }

    /* Main content */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #f9fafb !important;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #f9fafb !important;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #172033 !important;
    }

    /* Paragraphs */
    p, label, span, div {
        color: #172033;
    }

    /* Input boxes */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"],
    .stMultiSelect div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #172033 !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* Selectbox text */
    .stSelectbox span,
    .stMultiSelect span {
        color: #172033 !important;
    }

    /* File uploader */
    section[data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 2px dashed #64748b;
        border-radius: 12px;
        padding: 10px;
    }

    section[data-testid="stFileUploader"] * {
        color: #172033 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dbe3ee;
        border-radius: 12px;
        padding: 15px;
    }

    div[data-testid="stMetric"] label {
        color: #64748b !important;
    }

    div[data-testid="stMetric"] div {
        color: #172033 !important;
    }

    /* Tables */
    .stDataFrame {
        background-color: #ffffff;
    }

    /* Custom cards */
    .card {
        background-color: #ffffff;
        border: 1px solid #dbe3ee;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        color: #172033 !important;
        margin-bottom: 8px;
    }

    .card-text {
        color: #475569 !important;
        font-size: 15px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: #172033 !important;
        margin-bottom: 15px;
    }

    /* Status badges */
    .badge-high {
        background-color: #fee2e2;
        color: #991b1b !important;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: 700;
    }

    .badge-medium {
        background-color: #fef3c7;
        color: #92400e !important;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: 700;
    }

    .badge-low {
        background-color: #dcfce7;
        color: #166534 !important;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: 700;
    }

    /* Alert boxes */
    .info-box {
        background-color: #eff6ff;
        border-left: 5px solid #2563eb;
        padding: 15px;
        border-radius: 8px;
        color: #172033 !important;
    }

    .warning-box {
        background-color: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        color: #172033 !important;
    }

    .danger-box {
        background-color: #fef2f2;
        border-left: 5px solid #dc2626;
        padding: 15px;
        border-radius: 8px;
        color: #172033 !important;
    }

    .success-box {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 15px;
        border-radius: 8px;
        color: #172033 !important;
    }

    /* Dark mode compatibility */
    @media (prefers-color-scheme: dark) {

        .stApp {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }

        h1, h2, h3, h4,
        p, label, span {
            color: #f8fafc !important;
        }

        .card,
        div[data-testid="stMetric"],
        section[data-testid="stFileUploader"] {
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }

        .card-title {
            color: #f8fafc !important;
        }

        .card-text {
            color: #cbd5e1 !important;
        }

        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"],
        .stMultiSelect div[data-baseweb="select"] {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border-color: #475569 !important;
        }

        .stSelectbox span,
        .stMultiSelect span {
            color: #f8fafc !important;
        }

        section[data-testid="stFileUploader"] * {
            color: #f8fafc !important;
        }

        div[data-testid="stMetric"] label {
            color: #cbd5e1 !important;
        }

        div[data-testid="stMetric"] div {
            color: #f8fafc !important;
        }

        .info-box {
            background-color: #172554;
            color: #dbeafe !important;
        }

        .warning-box {
            background-color: #451a03;
            color: #fef3c7 !important;
        }

        .danger-box {
            background-color: #450a0a;
            color: #fecaca !important;
        }

        .success-box {
            background-color: #052e16;
            color: #bbf7d0 !important;
        }
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEALTH PROBLEMS
# ============================================================

HEALTH_PROBLEMS = [
    "Cardiovascular Diseases & Hypertension",
    "Diabetes",
    "Cancer",
    "Neurological Disorders",
    "Respiratory Diseases",
    "Kidney Disease",
    "Liver Disease",
    "Infectious Diseases",
    "Stroke",
    "Trauma",
    "Pediatric Conditions",
    "Geriatric Conditions",
    "Mental Health",
    "Pregnancy & Maternal Health",
    "Rare Diseases",
    "Autoimmune Disorders",
    "Gastrointestinal Disorders",
    "Endocrine Disorders",
    "Blood Disorders",
    "Musculoskeletal Disorders",
    "Ophthalmic Disorders",
    "Dermatological Disorders",
    "Other"
]


# ============================================================
# SESSION STATE
# ============================================================

if "cases" not in st.session_state:
    st.session_state.cases = {}

if "audit" not in st.session_state:
    st.session_state.audit = []

if "notifications" not in st.session_state:
    st.session_state.notifications = []

if "case_counter" not in st.session_state:
    st.session_state.case_counter = 1

if "selected_case" not in st.session_state:
    st.session_state.selected_case = None


# ============================================================
# BASIC FUNCTIONS
# ============================================================

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_audit(case_id, action, actor="System"):
    st.session_state.audit.append({
        "timestamp": now(),
        "case_id": case_id,
        "actor": actor,
        "action": action
    })


def add_notification(message, level="Info"):
    st.session_state.notifications.append({
        "time": now(),
        "level": level,
        "message": message
    })


# ============================================================
# FILE EXTRACTION
# ============================================================

def extract_text_from_file(uploaded_file):

    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    # TXT
    if filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    # JSON
    if filename.endswith(".json"):
        try:
            data = json.loads(file_bytes.decode("utf-8"))
            return json.dumps(data, indent=2)
        except:
            return file_bytes.decode("utf-8", errors="ignore")

    # CSV
    if filename.endswith(".csv"):
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
            rows = list(csv.DictReader(io.StringIO(text)))

            if rows:
                return json.dumps(rows, indent=2)

            return text
        except:
            return file_bytes.decode("utf-8", errors="ignore")

    # PDF
    if filename.endswith(".pdf"):

        if PdfReader is None:
            return "PDF reader is not installed."

        try:
            pdf = PdfReader(io.BytesIO(file_bytes))
            pages = []

            for page in pdf.pages:
                pages.append(page.extract_text() or "")

            return "\n".join(pages)

        except Exception as e:
            return f"Unable to read PDF: {e}"

    # DOCX
    if filename.endswith(".docx"):

        if Document is None:
            return "DOCX reader is not installed."

        try:
            document = Document(io.BytesIO(file_bytes))

            paragraphs = [
                p.text
                for p in document.paragraphs
                if p.text.strip()
            ]

            return "\n".join(paragraphs)

        except Exception as e:
            return f"Unable to read DOCX: {e}"

    # XLSX
    if filename.endswith(".xlsx"):

        if load_workbook is None:
            return "Excel reader is not installed."

        try:
            workbook = load_workbook(
                io.BytesIO(file_bytes),
                data_only=True
            )

            output = []

            for sheet in workbook.sheetnames:

                ws = workbook[sheet]

                output.append(f"Sheet: {sheet}")

                for row in ws.iter_rows(values_only=True):

                    values = [
                        str(cell)
                        for cell in row
                        if cell is not None
                    ]

                    if values:
                        output.append(" | ".join(values))

            return "\n".join(output)

        except Exception as e:
            return f"Unable to read Excel file: {e}"

    return "Unsupported file type."


# ============================================================
# TEXT HELPERS
# ============================================================

def find_value(text, patterns):

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return ""


def extract_patient_data(text):

    data = {}

    # Patient ID
    data["patient_id"] = find_value(
        text,
        [
            r"patient\s*id\s*[:\-]\s*([A-Za-z0-9\-_]+)",
            r"patientid\s*[:\-]\s*([A-Za-z0-9\-_]+)",
            r"ID\s*[:\-]\s*([A-Za-z0-9\-_]+)"
        ]
    )

    # Name
    data["name"] = find_value(
        text,
        [
            r"patient\s*name\s*[:\-]\s*(.+)",
            r"name\s*[:\-]\s*(.+)"
        ]
    )

    # Age
    age = find_value(
        text,
        [
            r"age\s*[:\-]\s*(\d+)",
            r"(\d+)\s*years?\s*old"
        ]
    )

    try:
        data["age"] = int(age)
    except:
        data["age"] = 0

    # Gender
    data["gender"] = find_value(
        text,
        [
            r"gender\s*[:\-]\s*(\w+)",
            r"sex\s*[:\-]\s*(\w+)"
        ]
    )

    # Blood pressure
    data["blood_pressure"] = find_value(
        text,
        [
            r"blood\s*pressure\s*[:\-]\s*([0-9]{2,3}\s*/\s*[0-9]{2,3})",
            r"BP\s*[:\-]\s*([0-9]{2,3}\s*/\s*[0-9]{2,3})"
        ]
    )

    # Heart rate
    hr = find_value(
        text,
        [
            r"heart\s*rate\s*[:\-]\s*(\d+)",
            r"HR\s*[:\-]\s*(\d+)"
        ]
    )

    try:
        data["heart_rate"] = int(hr)
    except:
        data["heart_rate"] = 0

    # Temperature
    temp = find_value(
        text,
        [
            r"temperature\s*[:\-]\s*([0-9.]+)",
            r"temp\s*[:\-]\s*([0-9.]+)"
        ]
    )

    try:
        data["temperature"] = float(temp)
    except:
        data["temperature"] = 0.0

    # SpO2
    spo2 = find_value(
        text,
        [
            r"SpO2\s*[:\-]\s*([0-9.]+)",
            r"oxygen\s*saturation\s*[:\-]\s*([0-9.]+)"
        ]
    )

    try:
        data["spo2"] = float(spo2)
    except:
        data["spo2"] = 0.0

    # Health problem
    problem = ""

    for item in HEALTH_PROBLEMS:

        if item.lower() in text.lower():

            problem = item
            break

    if not problem:

        if "hypertension" in text.lower():
            problem = "Cardiovascular Diseases & Hypertension"

        elif "diabetes" in text.lower():
            problem = "Diabetes"

        elif "cancer" in text.lower():
            problem = "Cancer"

        elif "stroke" in text.lower():
            problem = "Stroke"

        elif "kidney" in text.lower():
            problem = "Kidney Disease"

        elif "respiratory" in text.lower():
            problem = "Respiratory Diseases"

        else:
            problem = "Other"

    data["health_problem"] = problem

    # History
    data["history"] = find_value(
        text,
        [
            r"medical\s*history\s*[:\-]\s*(.+)",
            r"history\s*[:\-]\s*(.+)"
        ]
    )

    # Symptoms
    data["symptoms"] = find_value(
        text,
        [
            r"symptoms?\s*[:\-]\s*(.+)",
            r"presenting\s*symptoms?\s*[:\-]\s*(.+)"
        ]
    )

    # Investigations
    data["investigations"] = find_value(
        text,
        [
            r"investigations?\s*[:\-]\s*(.+)",
            r"tests?\s*[:\-]\s*(.+)"
        ]
    )

    # Current care
    data["current_care"] = find_value(
        text,
        [
            r"current\s*care\s*[:\-]\s*(.+)",
            r"treatment\s*[:\-]\s*(.+)",
            r"management\s*[:\-]\s*(.+)"
        ]
    )

    # Ethical issue
    data["ethical_issue"] = find_value(
        text,
        [
            r"ethical\s*issue\s*[:\-]\s*(.+)",
            r"ethics\s*[:\-]\s*(.+)"
        ]
    )

    # Time sensitivity
    data["time_sensitivity"] = find_value(
        text,
        [
            r"time\s*sensitivity\s*[:\-]\s*(.+)",
            r"urgency\s*[:\-]\s*(.+)"
        ]
    )

    # Full source text
    data["source_text"] = text

    return data


# ============================================================
# URGENCY ANALYSIS
# ============================================================

def calculate_urgency(patient):

    score = 0

    symptoms = str(patient.get("symptoms", "")).lower()
    bp = str(patient.get("blood_pressure", "")).lower()

    try:
        spo2 = float(patient.get("spo2", 0))
    except:
        spo2 = 0

    try:
        hr = int(patient.get("heart_rate", 0))
    except:
        hr = 0

    if spo2 > 0 and spo2 < 92:
        score += 3

    elif spo2 > 0 and spo2 < 95:
        score += 2

    if hr >= 120 or (hr > 0 and hr < 50):
        score += 2

    if "chest pain" in symptoms:
        score += 2

    if "shortness of breath" in symptoms:
        score += 2

    if "severe" in symptoms:
        score += 2

    if "/" in bp:

        try:
            systolic = int(bp.split("/")[0])

            if systolic >= 180:
                score += 3

            elif systolic >= 160:
                score += 2

        except:
            pass

    if score >= 6:
        return "High"

    elif score >= 3:
        return "Medium"

    return "Low"


# ============================================================
# DECISION OPTIONS
# ============================================================

def generate_options(patient):

    urgency = patient.get("urgency", "Medium")

    if urgency == "High":

        return {
            "A": {
                "name": "Immediate Intervention",
                "benefit": 9,
                "risk": 6,
                "resources": 8,
                "ethics": 8,
                "patient": 6
            },
            "B": {
                "name": "Further Investigation",
                "benefit": 7,
                "risk": 3,
                "resources": 6,
                "ethics": 9,
                "patient": 7
            },
            "C": {
                "name": "Conservative Management",
                "benefit": 5,
                "risk": 7,
                "resources": 3,
                "ethics": 6,
                "patient": 5
            }
        }

    elif urgency == "Medium":

        return {
            "A": {
                "name": "Immediate Intervention",
                "benefit": 8,
                "risk": 6,
                "resources": 7,
                "ethics": 8,
                "patient": 6
            },
            "B": {
                "name": "Further Investigation",
                "benefit": 8,
                "risk": 3,
                "resources": 5,
                "ethics": 9,
                "patient": 7
            },
            "C": {
                "name": "Conservative Management",
                "benefit": 6,
                "risk": 5,
                "resources": 3,
                "ethics": 7,
                "patient": 6
            }
        }

    else:

        return {
            "A": {
                "name": "Immediate Intervention",
                "benefit": 6,
                "risk": 6,
                "resources": 7,
                "ethics": 7,
                "patient": 5
            },
            "B": {
                "name": "Further Investigation",
                "benefit": 7,
                "risk": 3,
                "resources": 5,
                "ethics": 9,
                "patient": 7
            },
            "C": {
                "name": "Conservative Management",
                "benefit": 8,
                "risk": 2,
                "resources": 2,
                "ethics": 8,
                "patient": 8
            }
        }


# ============================================================
# MCDM
# ============================================================

def calculate_mcdm(options):

    weights = {
        "Expected Benefit": 0.30,
        "Safety": 0.25,
        "Recovery Probability": 0.20,
        "Resource Availability": 0.10,
        "Ethical Acceptability": 0.10,
        "Patient Preference": 0.05
    }

    results = {}

    for key, option in options.items():

        safety = 10 - option["risk"]

        recovery = option["benefit"]

        utility = (
            weights["Expected Benefit"] * option["benefit"] +
            weights["Safety"] * safety +
            weights["Recovery Probability"] * recovery +
            weights["Resource Availability"] * option["resources"] +
            weights["Ethical Acceptability"] * option["ethics"] +
            weights["Patient Preference"] * option["patient"]
        )

        results[key] = round(utility, 2)

    ranking = sorted(
        results.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return weights, results, ranking


# ============================================================
# CREATE CASE FROM PATIENT DATA
# ============================================================

def create_case(patient):

    case_number = st.session_state.case_counter

    patient_id = patient.get("patient_id")

    if not patient_id:
        patient_id = f"P{case_number:03d}"

    case_id = f"CASE-{case_number:03d}"

    patient["patient_id"] = patient_id

    urgency = calculate_urgency(patient)

    patient["urgency"] = urgency

    options = generate_options(patient)

    weights, scores, ranking = calculate_mcdm(options)

    patient["options"] = options
    patient["mcdm_weights"] = weights
    patient["mcdm_scores"] = scores
    patient["ranking"] = ranking

    patient["status"] = "Active"
    patient["assigned_to"] = "Clinical Review Team"

    patient["final_decision"] = ""
    patient["decision_status"] = "Pending Human Review"

    patient["stakeholders"] = {
        "Treating Doctor": {
            "option": "A",
            "reason": "Prioritizes timely clinical management."
        },
        "Independent Physician": {
            "option": "B",
            "reason": "Requests additional clinical evidence before intervention."
        },
        "Ethics Committee": {
            "option": "B",
            "reason": "Balances safety, proportionality, and uncertainty."
        },
        "Patient": {
            "option": "C",
            "reason": "Prefers a less intensive approach where clinically acceptable."
        }
    }

    patient["created_at"] = now()

    st.session_state.cases[case_id] = patient

    st.session_state.selected_case = case_id

    st.session_state.case_counter += 1

    add_audit(
        case_id,
        "Patient file uploaded and case created."
    )

    if urgency == "High":

        add_notification(
            f"{case_id}: High urgency case requires review.",
            "Urgent"
        )

    return case_id


# ============================================================
# GET SELECTED CASE
# ============================================================

def get_selected_case():

    if not st.session_state.selected_case:
        return None

    return st.session_state.cases.get(
        st.session_state.selected_case
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:28px;
        font-weight:800;
        color:#ffffff !important;
        margin-bottom:5px;">
        ⚕️ EthicSync
    </div>

    <div style="
        font-size:13px;
        color:#cbd5e1 !important;
        margin-bottom:20px;">
        Clinical Decision-Support Prototype
    </div>
    """,
    unsafe_allow_html=True
)

pages = [
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

page = st.sidebar.radio(
    "Navigation",
    pages
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        '<div class="section-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    cases = list(st.session_state.cases.values())

    total_cases = len(cases)

    active = len([
        c for c in cases
        if c.get("status") == "Active"
    ])

    urgent = len([
        c for c in cases
        if c.get("urgency") == "High"
    ])

    pending = len([
        c for c in cases
        if c.get("decision_status") == "Pending Human Review"
    ])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Cases", total_cases)
    c2.metric("Active Cases", active)
    c3.metric("Urgent Cases", urgent)
    c4.metric("Pending Review", pending)

    st.markdown("### Quick Actions")

    q1, q2 = st.columns(2)

    with q1:
        st.info(
            "📁 Upload a patient file from the New Case page."
        )

    with q2:
        st.info(
            "🧠 Review AI, MCDM and stakeholder analysis."
        )

    st.markdown("### Recent Cases")

    if cases:

        for case_id, case in list(
            st.session_state.cases.items()
        )[-5:]:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">
                        {case_id} — {case.get("patient_id", "Unknown")}
                    </div>

                    <div class="card-text">
                        Health Problem:
                        {case.get("health_problem", "Not specified")}
                        <br>
                        Urgency:
                        {case.get("urgency", "Not assessed")}
                        <br>
                        Status:
                        {case.get("status", "Unknown")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("No cases available. Upload a patient file to create a case.")


# ============================================================
# NEW CASE
# ============================================================

elif page == "New Case":

    st.markdown(
        '<div class="section-title">New Case</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-box">
        Upload the patient's clinical file. EthicSync will extract
        available patient information and automatically prepare the
        clinical decision-support workflow.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Patient File",
        type=[
            "txt",
            "csv",
            "json",
            "pdf",
            "docx",
            "xlsx"
        ]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button("Extract Patient Information"):

            text = extract_text_from_file(
                uploaded_file
            )

            patient = extract_patient_data(text)

            st.session_state.uploaded_patient = patient

            st.success(
                "Patient information extracted successfully."
            )

    if "uploaded_patient" in st.session_state:

        patient = st.session_state.uploaded_patient

        st.markdown("### Extracted Patient Information")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.text_input(
                "Patient ID",
                value=patient.get("patient_id", ""),
                key="edit_patient_id"
            )

            st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=patient.get("age", 0),
                key="edit_age"
            )

        with c2:

            st.text_input(
                "Patient Name",
                value=patient.get("name", ""),
                key="edit_name"
            )

            st.text_input(
                "Gender",
                value=patient.get("gender", ""),
                key="edit_gender"
            )

        with c3:

            st.selectbox(
                "Health Problem",
                HEALTH_PROBLEMS,
                index=(
                    HEALTH_PROBLEMS.index(
                        patient.get(
                            "health_problem",
                            "Other"
                        )
                    )
                    if patient.get(
                        "health_problem",
                        "Other"
                    ) in HEALTH_PROBLEMS
                    else len(HEALTH_PROBLEMS) - 1
                ),
                key="edit_problem"
            )

        st.markdown("### Clinical Information")

        history = st.text_area(
            "Medical History",
            value=patient.get("history", "")
        )

        symptoms = st.text_area(
            "Symptoms / Presenting Condition",
            value=patient.get("symptoms", "")
        )

        investigations = st.text_area(
            "Investigations",
            value=patient.get("investigations", "")
        )

        current_care = st.text_area(
            "Current Care / Management",
            value=patient.get("current_care", "")
        )

        ethical_issue = st.text_area(
            "Ethical Issue",
            value=patient.get("ethical_issue", "")
        )

        st.markdown("### Vital Information")

        v1, v2, v3, v4 = st.columns(4)

        with v1:

            bp = st.text_input(
                "Blood Pressure",
                value=patient.get(
                    "blood_pressure",
                    ""
                )
            )

        with v2:

            hr = st.number_input(
                "Heart Rate",
                min_value=0,
                max_value=250,
                value=int(
                    patient.get(
                        "heart_rate",
                        0
                    )
                )
            )

        with v3:

            temp = st.number_input(
                "Temperature",
                min_value=0.0,
                max_value=50.0,
                value=float(
                    patient.get(
                        "temperature",
                        0.0
                    )
                ),
                step=0.1
            )

        with v4:

            spo2 = st.number_input(
                "SpO2",
                min_value=0.0,
                max_value=100.0,
                value=float(
                    patient.get(
                        "spo2",
                        0.0
                    )
                ),
                step=1.0
            )

        if st.button(
            "Create Case & Run Analysis",
            type="primary"
        ):

            patient["patient_id"] = st.session_state.edit_patient_id
            patient["name"] = st.session_state.edit_name
            patient["age"] = st.session_state.edit_age
            patient["gender"] = st.session_state.edit_gender
            patient["health_problem"] = st.session_state.edit_problem

            patient["history"] = history
            patient["symptoms"] = symptoms
            patient["investigations"] = investigations
            patient["current_care"] = current_care
            patient["ethical_issue"] = ethical_issue

            patient["blood_pressure"] = bp
            patient["heart_rate"] = hr
            patient["temperature"] = temp
            patient["spo2"] = spo2

            case_id = create_case(patient)

            st.success(
                f"{case_id} created successfully!"
            )

            st.info(
                "The urgency, decision options and MCDM analysis have been generated."
            )


# ============================================================
# CASES
# ============================================================

elif page == "Cases":

    st.markdown(
        '<div class="section-title">Cases</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "Search cases",
        placeholder="Search by patient ID, case ID or health problem..."
    )

    for case_id, case in st.session_state.cases.items():

        searchable = (
            case_id +
            " " +
            str(case.get("patient_id", "")) +
            " " +
            str(case.get("health_problem", ""))
        ).lower()

        if search.lower() not in searchable:
            continue

        st.markdown(
            f"""
            <div class="card">

                <div class="card-title">
                    {case_id}
                </div>

                <div class="card-text">

                    Patient:
                    {case.get("patient_id", "Unknown")}
                    <br>

                    Problem:
                    {case.get("health_problem", "Unknown")}
                    <br>

                    Urgency:
                    {case.get("urgency", "Unknown")}
                    <br>

                    Status:
                    {case.get("status", "Unknown")}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            f"Open {case_id}",
            key=f"open_{case_id}"
        ):

            st.session_state.selected_case = case_id

            st.success(
                f"{case_id} selected."
            )


# ============================================================
# PATIENT CARE URGENCY
# ============================================================

elif page == "Patient Care Urgency":

    st.markdown(
        '<div class="section-title">Patient Care Urgency</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case from the Cases page first."
        )

    else:

        urgency = case.get(
            "urgency",
            "Unknown"
        )

        st.metric(
            "Urgency Level",
            urgency
        )

        st.write(
            "**Time Sensitivity:**",
            case.get(
                "time_sensitivity",
                "Not specified"
            )
        )

        if urgency == "High":

            st.markdown(
                """
                <div class="danger-box">
                🚨 High-priority case. Human clinical review should be prioritized.
                </div>
                """,
                unsafe_allow_html=True
            )

        elif urgency == "Medium":

            st.markdown(
                """
                <div class="warning-box">
                ⚠️ Moderate-priority case requiring clinical review.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="success-box">
                ✓ Lower urgency based on the available extracted information.
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### Critical Clinical Information")

        st.write(
            f"**Symptoms:** {case.get('symptoms', 'Not available')}"
        )

        st.write(
            f"**Blood Pressure:** {case.get('blood_pressure', 'Not available')}"
        )

        st.write(
            f"**Heart Rate:** {case.get('heart_rate', 'Not available')}"
        )

        st.write(
            f"**SpO2:** {case.get('spo2', 'Not available')}"
        )


# ============================================================
# CLINICAL INFORMATION
# ============================================================

elif page == "Clinical Information":

    st.markdown(
        '<div class="section-title">Clinical Information</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case from the Cases page first."
        )

    else:

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
            {case.get("patient_id", "Patient")}
            </div>

            <div class="card-text">

            <b>Health Problem:</b>
            {case.get("health_problem", "Not specified")}

            <br><br>

            <b>Age:</b>
            {case.get("age", "Not available")}

            <br>

            <b>Gender:</b>
            {case.get("gender", "Not available")}

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Medical History",
                "Current Status",
                "Investigations",
                "Current Care",
                "Decision Options"
            ]
        )

        with tab1:

            st.write(
                case.get(
                    "history",
                    "No medical history extracted."
                )
            )

        with tab2:

            st.write(
                f"**Symptoms:** {case.get('symptoms', 'Not available')}"
            )

            st.write(
                f"**Blood Pressure:** {case.get('blood_pressure', 'Not available')}"
            )

            st.write(
                f"**Heart Rate:** {case.get('heart_rate', 'Not available')}"
            )

            st.write(
                f"**Temperature:** {case.get('temperature', 'Not available')}"
            )

            st.write(
                f"**SpO2:** {case.get('spo2', 'Not available')}"
            )

        with tab3:

            st.write(
                case.get(
                    "investigations",
                    "No investigations extracted."
                )
            )

        with tab4:

            st.write(
                case.get(
                    "current_care",
                    "No current care information extracted."
                )
            )

        with tab5:

            options = case.get(
                "options",
                {}
            )

            for key, option in options.items():

                st.markdown(
                    f"""
                    <div class="card">

                    <div class="card-title">
                    {key} — {option["name"]}
                    </div>

                    <div class="card-text">

                    Benefit: {option["benefit"]}/10<br>
                    Risk: {option["risk"]}/10<br>
                    Resource Requirement: {option["resources"]}/10<br>
                    Ethical Acceptability: {option["ethics"]}/10<br>
                    Patient Preference: {option["patient"]}/10

                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# AI DECISION SUPPORT
# ============================================================

elif page == "AI Decision Support":

    st.markdown(
        '<div class="section-title">AI Decision Support</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case first."
        )

    else:

        ranking = case.get(
            "ranking",
            []
        )

        if ranking:

            best_option = ranking[0][0]

            option_name = case["options"][
                best_option
            ]["name"]

            st.markdown(
                f"""
                <div class="info-box">

                <b>Prototype AI Recommendation:</b>

                {best_option} — {option_name}

                <br><br>

                This recommendation is generated from the prototype's
                transparent scoring framework and extracted case information.

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Clinical Factors")

            st.write(
                f"**Health Problem:** {case.get('health_problem')}"
            )

            st.write(
                f"**Urgency:** {case.get('urgency')}"
            )

            st.write(
                f"**Symptoms:** {case.get('symptoms')}"
            )

            st.markdown("### Ethical Issue")

            st.write(
                case.get(
                    "ethical_issue",
                    "No ethical issue extracted."
                )
            )

            st.markdown(
                """
                <div class="warning-box">
                ⚠️ This is a clinical decision-support prototype,
                not a diagnostic or prescribing system.
                Human clinical judgment remains necessary.
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# MCDM ANALYSIS
# ============================================================

elif page == "MCDM Analysis":

    st.markdown(
        '<div class="section-title">MCDM Analysis</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case first."
        )

    else:

        weights = case.get(
            "mcdm_weights",
            {}
        )

        scores = case.get(
            "mcdm_scores",
            {}
        )

        ranking = case.get(
            "ranking",
            []
        )

        st.markdown("### Criteria Weights")

        for criterion, weight in weights.items():

            st.write(
                f"**{criterion}:** {weight * 100:.0f}%"
            )

        st.markdown("### Option Scores")

        for key, score in scores.items():

            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                {key} — {case["options"][key]["name"]}
                </div>

                <div class="card-text">

                Weighted Utility Score:
                <b>{score:.2f}/10</b>

                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### Ranking")

        for i, (key, score) in enumerate(
            ranking,
            start=1
        ):

            st.write(
                f"**{i}. {key} — "
                f"{case['options'][key]['name']} "
                f"({score:.2f}/10)**"
            )


# ============================================================
# TRADE-OFF ANALYSIS
# ============================================================

elif page == "Trade-off Analysis":

    st.markdown(
        '<div class="section-title">Trade-off Analysis</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case first."
        )

    else:

        for key, option in case["options"].items():

            net = (
                option["benefit"] -
                option["risk"]
            )

            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                {key} — {option["name"]}
                </div>

                <div class="card-text">

                <b>Benefit:</b> {option["benefit"]}/10
                <br>

                <b>Risk:</b> {option["risk"]}/10
                <br>

                <b>Benefit − Risk:</b> {net}
                <br>

                <b>Resource Burden:</b> {option["resources"]}/10
                <br>

                <b>Ethical Acceptability:</b> {option["ethics"]}/10
                <br>

                <b>Patient Preference:</b> {option["patient"]}/10

                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            """
            <div class="info-box">
            The trade-off analysis compares expected benefit,
            risk, resource burden, ethical considerations and
            patient preference before the final human decision.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# STAKEHOLDER OPINIONS
# ============================================================

elif page == "Stakeholder Opinions":

    st.markdown(
        '<div class="section-title">Stakeholder Opinions</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case first."
        )

    else:

        stakeholders = case.get(
            "stakeholders",
            {}
        )

        choices = [
            "A",
            "B",
            "C"
        ]

        for stakeholder, opinion in stakeholders.items():

            st.markdown(
                f"### {stakeholder}"
            )

            option = st.selectbox(
                "Preferred Option",
                choices,
                index=choices.index(
                    opinion.get("option", "B")
                ),
                key=f"stakeholder_{stakeholder}"
            )

            reason = st.text_area(
                "Reasoning / Concern",
                value=opinion.get(
                    "reason",
                    ""
                ),
                key=f"reason_{stakeholder}"
            )

            opinion["option"] = option
            opinion["reason"] = reason

        if st.button("Save Stakeholder Opinions"):

            add_audit(
                st.session_state.selected_case,
                "Stakeholder opinions updated."
            )

            st.success(
                "Stakeholder opinions saved."
            )

        opinions = [
            opinion.get("option")
            for opinion in stakeholders.values()
        ]

        disagreement = (
            len(set(opinions)) > 1
        )

        if disagreement:

            st.markdown(
                """
                <div class="warning-box">
                ⚠️ Stakeholder disagreement detected.
                The preferred decisions are not identical.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="success-box">
                ✓ Stakeholders currently show agreement.
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# CONSENSUS MANAGEMENT
# ============================================================

elif page == "Consensus Management":

    st.markdown(
        '<div class="section-title">Consensus Management</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case first."
        )

    else:

        stakeholders = case.get(
            "stakeholders",
            {}
        )

        opinions = [
            x.get("option")
            for x in stakeholders.values()
        ]

        total = len(opinions)

        if total:

            counts = {}

            for opinion in opinions:
                counts[opinion] = counts.get(
                    opinion,
                    0
                ) + 1

            majority_option = max(
                counts,
                key=counts.get
            )

            agreement = (
                counts[majority_option] /
                total
            ) * 100

            st.metric(
                "Consensus Agreement",
                f"{agreement:.0f}%"
            )

            st.write(
                f"Majority preference: "
                f"**{majority_option} — "
                f"{case['options'][majority_option]['name']}**"
            )

            if agreement < 100:

                st.warning(
                    "Disagreement remains. Human discussion/review is required."
                )

            else:

                st.success(
                    "All listed stakeholders currently agree."
                )

        if st.button("Record Consensus Review"):

            add_audit(
                st.session_state.selected_case,
                "Consensus review recorded."
            )

            st.success(
                "Consensus review recorded."
            )


# ============================================================
# DECISION TRANSPARENCY
# ============================================================

elif page == "Decision Transparency":

    st.markdown(
        '<div class="section-title">Decision Transparency</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case first."
        )

    else:

        st.markdown("### Data Source")

        st.write(
            "Patient information source:",
            case.get(
                "source_text",
                "Uploaded patient file"
            )[:1000]
        )

        st.markdown("### Calculation Method")

        st.write(
            "The prototype uses a weighted Multi-Criteria Decision-Making framework."
        )

        st.write(
            "Weighted Score = Σ(weight × criterion score)"
        )

        st.markdown("### Decision Ranking")

        for i, (key, score) in enumerate(
            case.get("ranking", []),
            start=1
        ):

            st.write(
                f"{i}. {key} — "
                f"{case['options'][key]['name']} "
                f"= {score:.2f}/10"
            )

        st.markdown("### Human Review Status")

        st.write(
            case.get(
                "decision_status",
                "Pending Human Review"
            )
        )


# ============================================================
# FINAL HUMAN DECISION
# ============================================================

elif page == "Final Human Decision":

    st.markdown(
        '<div class="section-title">Final Human Decision</div>',
        unsafe_allow_html=True
    )

    case = get_selected_case()

    if not case:

        st.warning(
            "Select a case first."
        )

    else:

        ranking = case.get(
            "ranking",
            []
        )

        ai_option = (
            ranking[0][0]
            if ranking
            else "B"
        )

        st.markdown(
            f"""
            <div class="info-box">

            <b>Prototype AI Recommendation:</b>

            {ai_option} —
            {case["options"][ai_option]["name"]}

            </div>
            """,
            unsafe_allow_html=True
        )

        decision = st.selectbox(
            "Human Decision",
            [
                "Accept AI Recommendation",
                "Modify AI Recommendation",
                "Reject AI Recommendation"
            ]
        )

        final_option = st.selectbox(
            "Final Selected Option",
            ["A", "B", "C"]
        )

        justification = st.text_area(
            "Decision Justification",
            placeholder="Enter the clinical reasoning for the human decision..."
        )

        human_review = st.checkbox(
            "I confirm this decision requires human clinical review."
        )

        if st.button(
            "Save Final Decision",
            type="primary"
        ):

            if not human_review:

                st.error(
                    "Please confirm human clinical review."
                )

            elif not justification.strip():

                st.error(
                    "Please provide a decision justification."
                )

            else:

                case["final_decision"] = final_option

                case["decision_type"] = decision

                case["decision_justification"] = justification

                case["decision_status"] = "Human Reviewed"

                case["final_decision_time"] = now()

                add_audit(
                    st.session_state.selected_case,
                    f"Final human decision recorded: {final_option}.",
                    "Human Reviewer"
                )

                st.success(
                    "Final human decision saved."
                )


# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "Audit Trail":

    st.markdown(
        '<div class="section-title">Audit Trail</div>',
        unsafe_allow_html=True
    )

    selected = st.session_state.selected_case

    records = [
        record
        for record in st.session_state.audit
        if not selected
        or record["case_id"] == selected
    ]

    if records:

        for record in reversed(records):

            st.markdown(
                f"""
                <div class="card">

                <div class="card-text">

                <b>{record["timestamp"]}</b>
                <br>

                Case:
                {record["case_id"]}

                <br>

                Actor:
                {record["actor"]}

                <br>

                Action:
                {record["action"]}

                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No audit events available."
        )


# ============================================================
# NOTIFICATIONS
# ============================================================

elif page == "Notifications":

    st.markdown(
        '<div class="section-title">Notifications</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.notifications:

        st.info(
            "No notifications."
        )

    else:

        for notification in reversed(
            st.session_state.notifications
        ):

            level = notification["level"]

            if level == "Urgent":

                st.error(
                    f"🚨 {notification['message']}"
                )

            else:

                st.info(
                    notification["message"]
                )

            st.caption(
                notification["time"]
            )


# ============================================================
# SETTINGS
# ============================================================

elif page == "Settings":

    st.markdown(
        '<div class="section-title">Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        EthicSync Prototype
        </div>

        <div class="card-text">

        <b>Application:</b>
        Clinical Decision-Support Prototype

        <br><br>

        <b>Data Input:</b>
        Patient file upload

        <br><br>

        <b>Decision Framework:</b>
        Multi-Criteria Decision-Making

        <br><br>

        <b>Human Oversight:</b>
        Required

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Supported Patient Files")

    st.write(
        "TXT, CSV, JSON, PDF, DOCX and XLSX"
    )

    st.markdown("### Important")

    st.warning(
        "The current prototype uses transparent rule-based extraction "
        "and scoring. It should not be presented as a clinically validated "
        "AI diagnostic system."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br><br>
    <div style="
        text-align:center;
        color:#64748b !important;
        font-size:12px;">
        EthicSync • Clinical Decision-Support Prototype •
        Human clinical judgment required
    </div>
    """,
    unsafe_allow_html=True
)
