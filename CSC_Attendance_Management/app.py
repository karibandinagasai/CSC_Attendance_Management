import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Admin Credentials (You can modify these values)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"


# Load student data
@st.cache_data
def load_students():
    try:
        df_cscha = pd.read_csv("Students_Names_k14CSCHA.csv")
        df_cscda = pd.read_csv("Students_Names_k14CSCDA.csv")
        return {"k14CSCHA": df_cscha, "k14CSCDA": df_cscda}
    except FileNotFoundError:
        return {"k14CSCHA": pd.DataFrame(columns=["Roll Number", "Name"]),
                "k14CSCDA": pd.DataFrame(columns=["Roll Number", "Name"])}


# Load or create attendance data
def load_attendance():
    try:
        return pd.read_excel("attendance.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Class", "Roll Number", "Student Name", "Attendance"])


# Save attendance data
def save_attendance(df):
    df.to_excel("attendance.xlsx", index=False)


# Display Past Attendance (Visible to Everyone)
st.subheader("📅 Past Attendance Records")
df_attendance = load_attendance()
st.dataframe(df_attendance)

# Download Button
if not df_attendance.empty:
    csv = df_attendance.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Attendance Records", csv, "attendance_records.csv", "text/csv")

# Authentication
st.title("📌 Class-Wise Attendance System")
username = st.text_input("Enter Username")
password = st.text_input("Enter Password", type="password")

if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
    st.success("✅ Access Granted!")

    # Load student lists
    students_data = load_students()

    # Select Class
    class_selected = st.selectbox("Select Class", ["k14CSCHA", "k14CSCDA"])
    df_students = students_data[class_selected]

    # Select Date
    date = st.date_input("Select Date", datetime.today())

    # Mark Attendance
    attendance_dict = {}
    for _, row in df_students.iterrows():
        student_name = f"{row['Roll Number']} - {row['Name']}"
        attendance_dict[student_name] = st.checkbox(student_name)

    # Save Attendance Button
    if st.button("Save Attendance"):
        attendance_records = [{"Date": date, "Class": class_selected,
                               "Roll Number": row.split(" - ")[0],
                               "Student Name": row.split(" - ")[1],
                               "Attendance": "Present" if present else "Absent"}
                              for row, present in attendance_dict.items()]

        df_attendance = load_attendance()
        new_df = pd.DataFrame(attendance_records)
        updated_df = pd.concat([df_attendance, new_df], ignore_index=True)
        save_attendance(updated_df)

        st.success(f"✅ Attendance saved successfully for {class_selected}!")
else:
    st.warning("🔒 Enter valid credentials to access attendance marking.")
