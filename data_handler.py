import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Course: 
    def __init__(self, name: str, credits: int, difficulty: int, weekly_hours: int):
        self.name = name
        self.credits = credits
        self.difficutly = difficulty
        self.weekly_hours = weekly_hours

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "credits": self.credits,
            "difficulty": self.difficutly,
            "weekly_hours": self.weekly_hours
        }
    
class Assignment: 
    def __init__(self, course: str, name: str, due_date: datetime, estimated_hours: int, 
                 priority: int, completed: bool = False):
        self.course = course
        self.name = name
        self.due_date = due_date
        self.estimated_hours = estimated_hours
        self.priority = priority
        self.completed = completed

    def to_dict(self) -> Dict:
        return {
            "course": self.course,
            "name": self.name,
            "due_date": self.due_date.isoformat(),
            "estimated_hours": self.estimated_hours,
            "priority": self.priority,
            "completed": self.completed
        }

class DataHandler:
    def __init__(self):
        self.courses = []
        self.assignments = []
        os.makedirs('data', exist_ok=True)

    def add_course(self, course: Course):
        existing_names = [c.name for c in self.courses]
        if course.name not in existing_names:
            self.courses.append(course)
            return True
        return False
    
    def add_assignment(self, assignment: Assignment):
        self.assignments.append(assignment)
        return True
        
    def get_pending_assignments(self):
        return [a for a in self.assignments if not a.completed]
        
    def save_data(self, filename: str = 'data/study_data.json'):
        try:
            data = {
                'courses': [course.to_dict() for course in self.courses],
                'assignments': [assignment.to_dict() for assignment in self.assignments]
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self, filename: str = 'data/study_data.json'):
        """Load courses and assignments from JSON file"""
        try:
            # If file doesn't exist, start with empty data
            if not os.path.exists(filename):
                print(f"No existing data file found at {filename}. Starting with empty data.")
                self.courses = []
                self.assignments = []
                return True
            
            # Load existing data from file
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Load courses
            self.courses = []
            for course_data in data.get('courses', []):
                course = Course(
                    course_data['name'],
                    course_data['credits'],
                    course_data['difficulty'],
                    course_data['weekly_hours']
                )
                self.courses.append(course)
            
            # Load assignments
            self.assignments = []
            for assignment_data in data.get('assignments', []):
                assignment = Assignment(
                    assignment_data['course'],
                    assignment_data['name'],
                    datetime.fromisoformat(assignment_data['due_date']),
                    assignment_data['estimated_hours'],
                    assignment_data['priority'],
                    assignment_data.get('completed', False)
                )
                self.assignments.append(assignment)
            
            print(f"Successfully loaded {len(self.courses)} courses and {len(self.assignments)} assignments")
            return True
            
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in {filename}: {e}")
            print("Starting with empty data.")
            self.courses = []
            self.assignments = []
            return False
            
        except KeyError as e:
            print(f"Error: Missing required field in data file: {e}")
            print("Starting with empty data.")
            self.courses = []
            self.assignments = []
            return False
            
        except Exception as e:
            print(f"Unexpected error loading data: {e}")
            print("Starting with empty data.")
            self.courses = []
            self.assignments = []
            return False
        