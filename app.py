elif page == "➕ New Case":
    patient_name = st.text_input(...)

# ❌ Now we're outside New Case
if st.button("Create Case"):
    if patient_name == "":
        st.write("Urgency:", urgency)
