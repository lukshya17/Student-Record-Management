
import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

st.title("Student Record Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.header("Add Student")

    roll = st.number_input("Roll Number", min_value=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    course = st.text_input("Course")

    if st.button("Add Student"):
        try:
            cursor.execute(
                "INSERT INTO students VALUES (?, ?, ?, ?)",
                (roll, name, age, course)
            )
            conn.commit()
            st.success("Student Added Successfully!")
        except sqlite3.IntegrityError:
            st.error("Roll Number Already Exists!")

# READ
elif menu == "View Students":
    st.header("View Students")

    df = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(df, width="stretch")

# UPDATE
elif menu == "Update Student":
    st.header("Update Student")

    df = pd.read_sql_query("SELECT * FROM students", conn)

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["roll"])
        student = df[df["roll"] == roll].iloc[0]

        name = st.text_input("Name", student["name"])
        age = st.number_input("Age", value=int(student["age"]))
        course = st.text_input("Course", student["course"])

        if st.button("Update Student"):
            cursor.execute(
                "UPDATE students SET name=?, age=?, course=? WHERE roll=?",
                (name, age, course, roll)
            )
            conn.commit()
            st.success("Student Updated!")
    else:
        st.info("No records found")

# DELETE
elif menu == "Delete Student":
    st.header("Delete Student")

    df = pd.read_sql_query("SELECT * FROM students", conn)

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["roll"])

        if st.button("Delete Student"):
            cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
            conn.commit()
            st.success("Student Deleted!")
    else:
        st.info("No records found")

conn.close()
