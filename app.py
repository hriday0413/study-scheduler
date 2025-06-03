import streamlit as st
from datetime import datetime, timedelta

# Simple classes directly in the app
class Course:
    def __init__(self, name, credits, difficulty, hours):
        self.name = name
        self.credits = credits
        self.difficulty = difficulty
        self.hours = hours

class Assignment:
    def __init__(self, course, name, due_date, hours, priority):
        self.course = course
        self.name = name
        self.due_date = due_date
        self.hours = hours
        self.priority = priority
        self.completed = False

# Initialize data
if 'courses' not in st.session_state:
    st.session_state.courses = []
if 'assignments' not in st.session_state:
    st.session_state.assignments = []

st.title("📚 Study Scheduler")

# Add course
st.header("Add Course")
with st.form("course_form"):
    name = st.text_input("Course Name")
    credits = st.number_input("Credits", 1, 6, 3)
    difficulty = st.slider("Difficulty", 1, 10, 5)
    hours = st.number_input("Weekly Hours", 1, 20, 6)
    
    if st.form_submit_button("Add Course"):
        st.session_state.courses.append(Course(name, credits, difficulty, hours))
        st.success(f"Added {name}!")

# Add assignment
if st.session_state.courses:
    st.header("Add Assignment")
    with st.form("assignment_form"):
        course = st.selectbox("Course", [c.name for c in st.session_state.courses])
        assignment_name = st.text_input("Assignment Name")
        due_date = st.date_input("Due Date")
        hours = st.number_input("Estimated Hours", 1, 50, 5)
        priority = st.slider("Priority", 1, 5, 3)
        
        if st.form_submit_button("Add Assignment"):
            due_datetime = datetime.combine(due_date, datetime.min.time())
            st.session_state.assignments.append(Assignment(course, assignment_name, due_datetime, hours, priority))
            st.success(f"Added {assignment_name}!")

# Show data
if st.session_state.courses:
    st.header("Your Courses")
    for course in st.session_state.courses:
        st.write(f"📚 {course.name} - {course.credits} credits, Difficulty: {course.difficulty}/10")

if st.session_state.assignments:
    st.header("Your Assignments")
    for assignment in st.session_state.assignments:
        days_left = (assignment.due_date - datetime.now()).days
        st.write(f"📝 {assignment.name} ({assignment.course}) - Due in {days_left} days")
