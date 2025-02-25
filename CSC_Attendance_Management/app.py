import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 📌 Ensure correct file paths for CSV loading
def get_csv_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# 📌 Load student data dynamically
@st.cache_data(ttl=0)  # Ensures fresh reloads every time
def load_students():
    try:
        df_cscha = pd.read_csv(get_csv_path("Students_Names_k14CSCHA.csv"), encoding="utf-8")
        df_cscda = pd.read_csv(get_csv_path("Students_Names_k14CSCDA.csv"), encoding="utf-8")
        return {"k14CSCHA": df_cscha, "k14CSCDA": df_cscda}
    except FileNotFoundError:
        return {"k14CSCHA": pd.DataFrame(columns=["Roll Number", "Name"]),
                "k14CSCDA": pd.DataFrame(columns=["Roll Number", "Name"])}

# 📌 Load or create attendance data
def load_attendance():
    try:
        return pd.read_excel(get_csv_path("attendance.xlsx"))
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Class", "Roll Number", "Student Name", "Attendance"])

# 📌 Save attendance data
def save_attendance(df):
    df.to_excel(get_csv_path("attendance.xlsx"), index=False)

# 📌 Load student lists
students_data = load_students()

# 📌 Streamlit UI
st.title("📌 4th Year Cyber Security Class-Wise Attendance System")
st.write("Mark and save attendance for your students.")

# 📌 Select Class
class_selected = st.selectbox("Select Class", list(students_data.keys()))

# 📌 Get student list based on selected class
df_students = students_data[class_selected]

# 📌 Debugging: Display column names if error persists
st.write("🔍 CSV Columns:", df_students.columns.tolist())

# 📌 Ensure correct column names exist
expected_columns = ["Roll Number", "Name"]
for col in expected_columns:
    if col not in df_students.columns:
        st.error(f"❌ Column '{col}' not found in {class_selected} CSV file! Please check the file format.")
        st.stop()

# 📌 Select Date
date = st.date_input("Select Date", datetime.today())

# 📌 Mark Attendance
attendance_dict = {}
for _, row in df_students.iterrows():
    student_name = f"{row['Roll Number']} - {row['Name']}"
    attendance_dict[student_name] = st.checkbox(student_name)

# 📌 Save Attendance Button
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

# 📌 Display Past Attendance
st.subheader(f"📅 Past Attendance Records - {class_selected}")
df_attendance = load_attendance()
filtered_df = df_attendance[df_attendance["Class"] == class_selected]
st.dataframe(filtered_df)
