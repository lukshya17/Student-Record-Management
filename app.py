
import streamlit as st
import pandas as pd

st.title("🎓 Student Record Management System")

# Store student data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course"]
    )

# Select operation
choice = st.sidebar.selectbox(
    "Choose Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if choice == "Add Student":
    st.header("Add Student")

    roll = st.number_input("Roll Number", min_value=1, step=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")

    if st.button("Add"):
        if name and course:
            if roll not in st.session_state.data["Roll No"].values:
                new_data = pd.DataFrame([{
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course
                }])

                st.session_state.data = pd.concat(
                    [st.session_state.data, new_data],
                    ignore_index=True
                )

                st.success("Student Added Successfully!")
            else:
                st.error("Roll Number Already Exists!")
        else:
            st.warning("Enter all details")

# READ
elif choice == "View Students":
    st.header("Student Records")
    st.dataframe(st.session_state.data, use_container_width=True)

# UPDATE
elif choice == "Update Student":
    st.header("Update Student")

    df = st.session_state.data

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["Roll No"])
        index = df.index[df["Roll No"] == roll][0]

        name = st.text_input("Name", df.loc[index, "Name"])
        age = st.number_input(
            "Age", min_value=1, max_value=100,
            value=int(df.loc[index, "Age"])
        )
        course = st.text_input("Course", df.loc[index, "Course"])

        if st.button("Update"):
            st.session_state.data.loc[index] = [
                roll, name, age, course
            ]
            st.success("Student Updated!")
    else:
        st.info("No records available")

# DELETE
elif choice == "Delete Student":
    st.header("Delete Student")

    df = st.session_state.data

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["Roll No"])

        if st.button("Delete"):
            st.session_state.data = df[
                df["Roll No"] != roll
            ].reset_index(drop=True)

            st.success("Student Deleted!")
    else:
        st.info("No records available")
