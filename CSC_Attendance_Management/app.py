import streamlit as st
import pandas as pd
from datetime import datetime


# Load student data from CSV files
@st.cache_data
def load_students():
    try:
        df_cscha = pd.read_csv("Students_Names_k14CSCHA.csv")  # Ensure correct filename
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


# Load student lists
students_data = load_students()

# Streamlit UI
st.title("📌 Class-Wise Attendance System")
st.write("Mark and save attendance for your students.")

# Select Class
class_selected = st.selectbox("Select Class", ["k14CSCHA", "k14CSCDA"])

# Get student list based on selected class
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

# Display Past Attendance
st.subheader(f"📅 Past Attendance Records - {class_selected}")
df_attendance = load_attendance()
filtered_df = df_attendance[df_attendance["Class"] == class_selected]
st.dataframe(filtered_df)
