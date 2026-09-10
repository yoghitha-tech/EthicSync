import streamlit as st

st.set_page_config(
    page_title="EthicSync",
    page_icon="⚖️",
    layout="wide"
)

# Sidebar
st.sidebar.title("⚖️ EthicSync")
st.sidebar.write("Clinical Decision Support System")

st.sidebar.button("🏠 Dashboard")
st.sidebar.button("➕ New Case")
st.sidebar.button("📁 Cases")
st.sidebar.button("🚨 Patient Care Urgency")
st.sidebar.button("🩺 Clinical Information")
st.sidebar.button("🤖 AI Decision Support")
st.sidebar.button("📊 MCDM Analysis")
st.sidebar.button("⚖️ Trade-off Analysis")
st.sidebar.button("👥 Stakeholder Opinions")
st.sidebar.button("🤝 Consensus Management")
st.sidebar.button("🔍 Decision Transparency")
st.sidebar.button("👤 Final Human Decision")
st.sidebar.button("📝 Audit Trail")
st.sidebar.button("🔔 Notifications")
st.sidebar.button("⚙️ Settings")

# Main page
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
