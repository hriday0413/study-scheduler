# Smart Study Schedule Optimizer

A web-based application designed to help students optimize their study schedules through intelligent task prioritization and time allocation algorithms. Built as a computer science project demonstrating full-stack development, data analytics, and algorithmic problem-solving.

## Live Application

**[View Application](https://study-scheduler-dzy7mf6kvzhvvrh7jwrmzj.streamlit.app/)**

## Project Overview

This application addresses the common student challenge of managing multiple courses and assignments with competing deadlines. The system uses a priority-based scheduling algorithm to automatically generate optimal study schedules based on assignment urgency, user-defined priorities, and available study time.

## Features

### Core Functionality
- **Course Management**: Add and track courses with difficulty ratings and credit hours
- **Assignment Tracking**: Monitor homework, projects, and exams with due dates and priority levels
- **Intelligent Scheduling**: Automated schedule generation using custom optimization algorithms
- **Progress Analytics**: Visual dashboard displaying workload distribution and completion metrics

### Technical Features
- **Data Visualization**: Interactive charts using Plotly for workload analysis
- **Calendar Integration**: Export schedules as ICS files compatible with Google Calendar, Outlook, and Apple Calendar
- **Data Export**: CSV export functionality for external analysis
- **Real-time Updates**: Dynamic interface with immediate feedback on user actions

## Technology Stack

- **Backend**: Python 3.8+
- **Frontend Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express
- **Deployment**: Streamlit Cloud
- **Version Control**: Git

## Algorithm Design

The scheduling system implements a priority-based optimization approach:

1. **Urgency Calculation**: Combines time remaining until deadline with user-assigned priority weights
2. **Time Allocation**: Distributes available study hours across days while respecting daily time constraints
3. **Constraint Satisfaction**: Ensures all assignments can be completed before their respective deadlines
4. **Load Balancing**: Prevents excessive workload concentration on individual days

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Git
- pip package manager

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/study-scheduler.git
   cd study-scheduler
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Access the application at `http://localhost:8501`

## Usage

### Getting Started
1. Navigate to the "Manage Courses" section to add your current courses
2. Add assignments in the "Manage Assignments" section with appropriate due dates and priorities
3. Use the "Generate Schedule" feature to create an optimized study plan
4. Export your schedule to your preferred calendar application

### Dashboard Analytics
The dashboard provides several analytical views:
- Assignment completion rates
- Workload distribution by course
- Upcoming deadline timeline
- Urgency-based task prioritization

## Project Structure

```
study-scheduler/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .streamlit/        # Configuration files
    └── config.toml
```

## Educational Value

This project demonstrates several computer science concepts:
- **Algorithm Design**: Custom scheduling optimization with multiple constraints
- **Web Development**: Full-stack application development using modern frameworks
- **Data Structures**: Object-oriented programming with Python classes
- **User Interface Design**: Interactive dashboard with real-time updates
- **Software Engineering**: Clean code practices, documentation, and version control


### Dependencies
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
numpy>=1.24.0
```

## Author

**Hriday Shankar**  
Northeastern University  
Computer Science and Business Administration  
Contact: shankar.hr@northeastern.edu
