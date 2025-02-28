import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Load student data
@st.cache_data
def load_students():
    files = ["Students_Names_k14CSCHA.csv", "Students_Names_k14CSCDA.csv"]
    
    for file in files:
        if not os.path.exists(file):
            st.error(f"❌ File Not Found: {file}")

    try:
        df_cscha = pd.read_csv("Students_Names_k14CSCHA.csv") if os.path.exists("Students_Names_k14CSCHA.csv") else pd.DataFrame(columns=["Roll Number", "Name"])
        df_cscda = pd.read_csv("Students_Names_k14CSCDA.csv") if os.path.exists("Students_Names_k14CSCDA.csv") else pd.DataFrame(columns=["Roll Number", "Name"])
        return {"k14CSCHA": df_cscha, "k14CSCDA": df_cscda}
    except Exception as e:
        st.error(f"⚠️ Error Loading Student Data: {e}")
        return {"k14CSCHA": pd.DataFrame(columns=["Roll Number", "Name"]),
                "k14CSCDA": pd.DataFrame(columns=["Roll Number", "Name"])}

# Load attendance
def load_attendance():
    file_path = "attendance.xlsx"
    
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Date", "Class", "Roll Number", "Student Name", "Attendance"])
        df.to_excel(file_path, index=False)
        return df
    else:
        return pd.read_excel(file_path)

# Save attendance
def save_attendance(df):
    df.to_excel("attendance.xlsx", index=False)

# Display Attendance Records
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

    # Reload Data Button
    if st.button("🔄 Reload Data"):
        st.cache_data.clear()
        st.experimental_rerun()

    # Debug: Show available files
    if st.button("📂 Show Files in Directory"):
        files = os.listdir(".")
        st.write("📁 Files in Directory:", files)

    # Load student lists
    students_data = load_students()
    st.write("✅ Loaded Student Data:", students_data)  # Debugging Line

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

    # Save Attendance
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
