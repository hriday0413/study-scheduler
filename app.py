import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import os
import json

# Data classes
class Course:
    def __init__(self, name: str, credits: int, difficulty: int, weekly_hours: int):
        self.name = name
        self.credits = credits
        self.difficulty = difficulty
        self.weekly_hours = weekly_hours
    
    def to_dict(self):
        return {
            'name': self.name,
            'credits': self.credits,
            'difficulty': self.difficulty,
            'weekly_hours': self.weekly_hours
        }

class Assignment:
    def __init__(self, course: str, name: str, due_date: datetime, 
                 estimated_hours: int, priority: int, completed: bool = False):
        self.course = course
        self.name = name
        self.due_date = due_date
        self.estimated_hours = estimated_hours
        self.priority = priority
        self.completed = completed
    
    def to_dict(self):
        return {
            'course': self.course,
            'name': self.name,
            'due_date': self.due_date.isoformat(),
            'estimated_hours': self.estimated_hours,
            'priority': self.priority,
            'completed': self.completed
        }

class StudyOptimizer:
    def __init__(self):
        self.available_hours_per_day = 8
        
    def calculate_urgency_score(self, assignment) -> float:
        try:
            days_until_due = (assignment.due_date - datetime.now()).days
            
            if days_until_due < 0:
                return 100  # Overdue
            elif days_until_due == 0:
                return 90   # Due today
            elif days_until_due <= 1:
                return 80   # Due tomorrow
            
            time_pressure = max(0, 15 - days_until_due)
            priority_weight = assignment.priority * 10
            
            return min(100, time_pressure + priority_weight)
            
        except Exception as e:
            return assignment.priority * 10

# Page configuration
st.set_page_config(
    page_title="Smart Study Scheduler",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
def init_session_state():
    if 'courses' not in st.session_state:
        st.session_state.courses = []
    if 'assignments' not in st.session_state:
        st.session_state.assignments = []
    if 'optimizer' not in st.session_state:
        st.session_state.optimizer = StudyOptimizer()

def get_pending_assignments():
    return [a for a in st.session_state.assignments if not a.completed]

def main():
    init_session_state()
    
    st.title("📚 Smart Study Schedule Optimizer")
    st.markdown("*Optimize your study time with intelligent scheduling*")
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📊 Dashboard", 
        "📝 Manage Courses", 
        "📋 Manage Assignments", 
        "🎯 Generate Schedule"
    ])
    
    # Sidebar stats
    pending_count = len(get_pending_assignments())
    course_count = len(st.session_state.courses)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📈 Quick Stats**")
    st.sidebar.metric("Active Courses", course_count)
    st.sidebar.metric("Pending Tasks", pending_count)
    
    # Route to pages
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "📝 Manage Courses":
        manage_courses()
    elif page == "📋 Manage Assignments":
        manage_assignments()
    elif page == "🎯 Generate Schedule":
        generate_schedule()

def show_dashboard():
    st.header("📊 Dashboard Overview")
    
    pending_assignments = get_pending_assignments()
    all_assignments = st.session_state.assignments
    courses = st.session_state.courses
    
    if not courses and not all_assignments:
        st.info("👋 **Welcome to Smart Study Scheduler!**")
        st.markdown("""
        ### Get Started:
        1. **📝 Add Courses** - Set up your classes with difficulty ratings
        2. **📋 Create Assignments** - Add your homework and projects with deadlines
        3. **🎯 Generate Schedule** - Let the algorithm optimize your study time
        """)
        return
    
    # Key metrics
    total_hours = sum([a.estimated_hours for a in pending_assignments])
    completed_assignments = [a for a in all_assignments if a.completed]
    urgent_assignments = [a for a in pending_assignments 
                         if (a.due_date - datetime.now()).days <= 3]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Pending Assignments", len(pending_assignments))
    with col2:
        st.metric("⏱️ Study Hours Needed", f"{total_hours}h")
    with col3:
        st.metric("🚨 Urgent (≤3 days)", len(urgent_assignments))
    with col4:
        completion_rate = len(completed_assignments) / len(all_assignments) * 100 if all_assignments else 0
        st.metric("✅ Completion Rate", f"{completion_rate:.1f}%")
    
    # Upcoming deadlines
    if pending_assignments:
        st.subheader("📅 Upcoming Deadlines")
        
        deadline_data = []
        for assignment in sorted(pending_assignments, key=lambda x: x.due_date):
            days_left = (assignment.due_date - datetime.now()).days
            
            if days_left < 0:
                status = "🔴 Overdue"
            elif days_left == 0:
                status = "🟡 Due Today"
            elif days_left <= 3:
                status = "🟠 Urgent"
            else:
                status = "🟢 Normal"
            
            deadline_data.append({
                "Assignment": assignment.name,
                "Course": assignment.course,
                "Due Date": assignment.due_date.strftime("%m/%d"),
                "Days Left": days_left,
                "Hours": assignment.estimated_hours,
                "Priority": "⭐" * assignment.priority,
                "Status": status
            })
        
        df = pd.DataFrame(deadline_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Charts
        if len(deadline_data) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(df, x="Course", y="Hours", 
                           title="📊 Study Hours by Course")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.pie(df, values="Hours", names="Course",
                           title="📚 Workload Distribution")
                st.plotly_chart(fig, use_container_width=True)

def manage_courses():
    st.header("📝 Course Management")
    
    # Add course form
    st.subheader("➕ Add New Course")
    with st.form("add_course_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            course_name = st.text_input("Course Name*")
            credits = st.number_input("Credits", min_value=1, max_value=6, value=3)
        
        with col2:
            difficulty = st.slider("Difficulty Level (1-10)", min_value=1, max_value=10, value=5)
            weekly_hours = st.number_input("Weekly Study Hours", min_value=1, max_value=20, value=6)
        
        if st.form_submit_button("➕ Add Course", type="primary"):
            if course_name.strip():
                # Check for duplicates
                existing_names = [c.name for c in st.session_state.courses]
                if course_name.strip() not in existing_names:
                    new_course = Course(course_name.strip(), credits, difficulty, weekly_hours)
                    st.session_state.courses.append(new_course)
                    st.success(f"✅ Added course: **{course_name}**")
                    st.rerun()
                else:
                    st.error("❌ Course already exists!")
            else:
                st.error("❌ Please enter a course name!")
    
    # Display courses
    if st.session_state.courses:
        st.subheader("📚 Your Courses")
        
        course_data = []
        for course in st.session_state.courses:
            course_assignments = [a for a in st.session_state.assignments if a.course == course.name]
            pending = [a for a in course_assignments if not a.completed]
            
            course_data.append({
                "Course": course.name,
                "Credits": course.credits,
                "Difficulty": "🌟" * course.difficulty,
                "Weekly Hours": f"{course.weekly_hours}h",
                "Assignments": len(pending)
            })
        
        df = pd.DataFrame(course_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

def manage_assignments():
    st.header("📋 Assignment Management")
    
    courses = st.session_state.courses
    if not courses:
        st.warning("⚠️ Please add courses first!")
        return
    
    # Add assignment form
    st.subheader("➕ Add New Assignment")
    with st.form("add_assignment_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            selected_course = st.selectbox("Course*", [c.name for c in courses])
            assignment_name = st.text_input("Assignment Name*")
            due_date = st.date_input("Due Date", value=datetime.now().date() + timedelta(days=7))
        
        with col2:
            estimated_hours = st.number_input("Estimated Hours*", min_value=1, max_value=100, value=5)
            priority = st.slider("Priority Level", min_value=1, max_value=5, value=3)
        
        if st.form_submit_button("➕ Add Assignment", type="primary"):
            if assignment_name.strip():
                due_datetime = datetime.combine(due_date, datetime.min.time())
                new_assignment = Assignment(selected_course, assignment_name.strip(), 
                                          due_datetime, estimated_hours, priority)
                st.session_state.assignments.append(new_assignment)
                st.success(f"✅ Added assignment: **{assignment_name}**")
                st.rerun()
            else:
                st.error("❌ Please enter an assignment name!")
    
    # Display assignments
    if st.session_state.assignments:
        st.subheader("📝 Your Assignments")
        
        for i, assignment in enumerate(st.session_state.assignments):
            with st.expander(f"{'✅' if assignment.completed else '📋'} {assignment.name} - {assignment.course}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**📅 Due:** {assignment.due_date.strftime('%Y-%m-%d')}")
                    st.write(f"**⏱️ Hours:** {assignment.estimated_hours}")
                    days_left = (assignment.due_date - datetime.now()).days
                    if days_left < 0:
                        st.write(f"**⚠️ Status:** {abs(days_left)} days overdue")
                    else:
                        st.write(f"**📆 Status:** {days_left} days left")
                
                with col2:
                    st.write(f"**⭐ Priority:** {'⭐' * assignment.priority}")
                    urgency = st.session_state.optimizer.calculate_urgency_score(assignment)
                    st.write(f"**🚨 Urgency:** {urgency:.1f}/100")
                
                with col3:
                    if not assignment.completed:
                        if st.button("✅ Complete", key=f"complete_{i}"):
                            st.session_state.assignments[i].completed = True
                            st.success("Assignment completed! 🎉")
                            st.rerun()
                    else:
                        st.success("✅ Completed")

def generate_schedule():
    st.header("🎯 Generate Optimized Schedule")
    
    pending_assignments = get_pending_assignments()
    
    if not pending_assignments:
        st.info("🎉 All assignments complete!")
        return
    
    # Settings
    col1, col2 = st.columns(2)
    with col1:
        days_ahead = st.slider("Days to plan ahead", min_value=3, max_value=21, value=10)
    with col2:
        daily_hours = st.slider("Available hours per day", min_value=2, max_value=12, value=8)
    
    if st.button("🚀 Generate Schedule", type="primary"):
        # Simple scheduling algorithm
        schedule_data = []
        current_date = datetime.now().date()
        
        # Sort by urgency
        sorted_assignments = sorted(pending_assignments, 
                                  key=lambda x: st.session_state.optimizer.calculate_urgency_score(x), 
                                  reverse=True)
        
        for day_offset in range(days_ahead):
            day = current_date + timedelta(days=day_offset)
            remaining_hours = daily_hours
            
            for assignment in sorted_assignments:
                if remaining_hours <= 0:
                    break
                if assignment.due_date.date() < day:
                    continue
                
                hours_to_allocate = min(assignment.estimated_hours, remaining_hours, 4)
                
                if hours_to_allocate > 0.5:
                    schedule_data.append({
                        "Date": day.strftime("%A, %B %d"),
                        "Assignment": assignment.name,
                        "Course": assignment.course,
                        "Hours": hours_to_allocate,
                        "Priority": assignment.priority
                    })
                    remaining_hours -= hours_to_allocate
        
        if schedule_data:
            st.success("✅ Schedule generated!")
            
            # Display schedule
            df = pd.DataFrame(schedule_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Chart
            fig = px.bar(df, x="Date", y="Hours", color="Course",
                        title="📊 Daily Study Schedule")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No assignments to schedule!")

if __name__ == "__main__":
    main()
