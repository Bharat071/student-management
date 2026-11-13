
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Management", page_icon="🎓")

st.title("🎓 Student Record Management System")
st.write("Manage student records easily using CRUD operations.")

# Initialize student data
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course"]
    )

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("Add New Student")

    roll = st.number_input("Roll Number", min_value=1, step=1)
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.selectbox("Course", ["CSE", "AIML", "ECE", "IT", "MBA"])

    if st.button("Add Student"):
        if name.strip() == "":
            st.error("Please enter student name.")
        elif roll in st.session_state.students["Roll No"].values:
            st.error("Roll number already exists!")
        else:
            new_student = pd.DataFrame([{
                "Roll No": roll,
                "Name": name,
                "Age": age,
                "Course": course
            }])

            st.session_state.students = pd.concat(
                [st.session_state.students, new_student],
                ignore_index=True
            )

            st.success("Student added successfully!")

# READ
elif menu == "View Students":
    st.subheader("All Student Records")

    if not st.session_state.students.empty:
        st.dataframe(st.session_state.students, use_container_width=True)
    else:
        st.info("No student records available.")

# UPDATE
elif menu == "Update Student":
    st.subheader("Update Student Details")

    if not st.session_state.students.empty:
        roll = st.selectbox(
            "Select Roll Number",
            st.session_state.students["Roll No"].tolist()
        )

        student = st.session_state.students[
            st.session_state.students["Roll No"] == roll
        ].iloc[0]

        name = st.text_input("New Name", value=student["Name"])
        age = st.number_input("New Age", min_value=1, max_value=100,
                              value=int(student["Age"]))
        course = st.selectbox(
            "New Course",
            ["CSE", "AIML", "ECE", "IT", "MBA"],
            index=["CSE", "AIML", "ECE", "IT", "MBA"].index(student["Course"])
        )

        if st.button("Update Student"):
            if name.strip() == "":
                st.error("Name cannot be empty.")
            else:
                idx = st.session_state.students[
                    st.session_state.students["Roll No"] == roll
                ].index[0]

                st.session_state.students.loc[idx, "Name"] = name
                st.session_state.students.loc[idx, "Age"] = age
                st.session_state.students.loc[idx, "Course"] = course

                st.success("Student updated successfully!")

    else:
        st.info("No records available to update.")

# DELETE
elif menu == "Delete Student":
    st.subheader("Delete Student Record")

    if not st.session_state.students.empty:
        roll = st.selectbox(
            "Select Roll Number to Delete",
            st.session_state.students["Roll No"].tolist()
        )

        if st.button("Delete Student"):
            st.session_state.students = st.session_state.students[
                st.session_state.students["Roll No"] != roll
            ].reset_index(drop=True)

            st.success("Student deleted successfully!")

    else:
        st.info("No records available to delete.")
