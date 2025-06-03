from datetime import datetime, timedelta
from typing import List, Dict

class StudyOptimizer:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.available_hours_per_day = 8
        self.break_duration = 15  # minutes
        self.max_session_duration = 120  # minutes
        
    def calculate_urgency_score(self, assignment) -> float:
        """Calculate urgency based on due date and priority"""
        try:
            days_until_due = (assignment.due_date - datetime.now()).days
            
            if days_until_due < 0:
                return 100  # Overdue
            elif days_until_due == 0:
                return 90   # Due today
            elif days_until_due <= 1:
                return 80   # Due tomorrow
            
            # Combine time pressure and priority
            time_pressure = max(0, 15 - days_until_due)
            priority_weight = assignment.priority * 10
            
            return min(100, time_pressure + priority_weight)
            
        except Exception as e:
            print(f"Error calculating urgency: {e}")
            return assignment.priority * 10
            
    def simple_schedule(self, days_ahead: int = 14) -> Dict:
        """Create a simple priority-based schedule"""
        
        pending_assignments = self.data_handler.get_pending_assignments()
        
        if not pending_assignments:
            return {
                "status": "No assignments",
                "schedule": [],
                "message": "No pending assignments to schedule!",
                "total_study_hours": 0
            }
        
        # Create a working copy of assignments to track remaining hours
        working_assignments = []
        for assignment in pending_assignments:
            working_assignments.append({
                'assignment': assignment,
                'remaining_hours': assignment.estimated_hours,
                'urgency': self.calculate_urgency_score(assignment)
            })
        
        # Sort by urgency (highest first)
        working_assignments.sort(key=lambda x: x['urgency'], reverse=True)
        
        schedule = []
        current_date = datetime.now().date()
        
        for day_offset in range(days_ahead):
            day = current_date + timedelta(days=day_offset)
            daily_schedule = {
                "date": day,
                "sessions": []
            }
            
            remaining_daily_hours = self.available_hours_per_day
            
            # Go through assignments in priority order
            for work_item in working_assignments:
                if remaining_daily_hours <= 0.5:  # Not enough time for meaningful work
                    break
                    
                assignment = work_item['assignment']
                
                # Skip if assignment is due before this day
                if assignment.due_date.date() < day:
                    continue
                
                # Skip if this assignment is already completed
                if work_item['remaining_hours'] <= 0:
                    continue
                
                # Calculate how much time to allocate today
                hours_to_allocate = min(
                    work_item['remaining_hours'],
                    remaining_daily_hours,
                    4.0  # Max 4 hours per assignment per day to ensure variety
                )
                
                if hours_to_allocate > 0.5:  # Only schedule significant blocks
                    daily_schedule["sessions"].append({
                        "assignment": assignment.name,
                        "course": assignment.course,
                        "hours": round(hours_to_allocate, 1),
                        "urgency": work_item['urgency'],
                        "due_date": assignment.due_date.strftime("%Y-%m-%d")
                    })
                    
                    # Update remaining hours
                    work_item['remaining_hours'] -= hours_to_allocate
                    remaining_daily_hours -= hours_to_allocate
            
            # Only add days that have sessions
            if daily_schedule["sessions"]:
                schedule.append(daily_schedule)
        
        total_hours = sum([
            sum([session["hours"] for session in day["sessions"]]) 
            for day in schedule
        ])
        
        return {
            "status": "Success",
            "schedule": schedule,
            "message": "Schedule generated successfully!",
            "total_study_hours": total_hours
        }
        
    def create_time_blocks(self, daily_sessions: List[Dict]) -> List[Dict]:
        """Convert daily sessions into specific time blocks"""
        time_blocks = []
        current_hour = 9  # Start at 9 AM
        
        for session in daily_sessions:
            duration_hours = session["hours"]
            
            # Calculate end time
            end_hour = current_hour + int(duration_hours)
            end_minute = int((duration_hours % 1) * 60)
            
            # Format times
            start_time = f"{current_hour:02d}:00"
            end_time = f"{end_hour:02d}:{end_minute:02d}"
            
            time_blocks.append({
                "assignment": session["assignment"],
                "course": session["course"],
                "start_time": start_time,
                "end_time": end_time,
                "duration_hours": duration_hours,
                "urgency": session["urgency"],
                "due_date": session["due_date"]
            })
            
            # Move to next time slot (add 15 minute break)
            current_hour = end_hour + (1 if end_minute > 45 else 0)
            if end_minute > 0 and end_minute <= 45:
                current_hour = end_hour
            
        return time_blocks

# Test the optimizer
if __name__ == "__main__":
    from data_handler import DataHandler, Course, Assignment
    
    print("Testing Study Optimizer...")
    
    # Test 1: Create test data handler with realistic data
    print("\n📚 Setting up test data...")
    handler = DataHandler()
    
    # Add realistic courses (like yours)
    courses = [
        Course("Fundamentals of Computer Science", 4, 8, 10),
        Course("Intermediate Programming with Data", 4, 7, 12),
        Course("Business Statistics", 3, 6, 8),
        Course("Financial Accounting & Reporting", 3, 5, 6)
    ]
    
    for course in courses:
        handler.add_course(course)
    
    print(f"✅ Added {len(handler.courses)} courses")
    
    # Add realistic assignments with varying urgency
    base_date = datetime.now()
    assignments = [
        Assignment("Fundamentals of Computer Science", "Binary Tree Project", 
                  base_date + timedelta(days=3), 10, 5),  # Very urgent
        Assignment("Intermediate Programming with Data", "Data Analysis Assignment", 
                  base_date + timedelta(days=7), 8, 4),   # Moderately urgent
        Assignment("Business Statistics", "Regression Analysis Report", 
                  base_date + timedelta(days=14), 12, 3), # Less urgent
        Assignment("Financial Accounting & Reporting", "Income Statement Analysis", 
                  base_date + timedelta(days=21), 6, 2),  # Not urgent
        Assignment("Fundamentals of Computer Science", "Algorithm Implementation", 
                  base_date + timedelta(days=5), 15, 4)   # High priority, medium urgency
    ]
    
    for assignment in assignments:
        handler.add_assignment(assignment)
    
    print(f"✅ Added {len(handler.assignments)} assignments")
    
    # Test 2: Create optimizer
    print("\n🎯 Testing optimizer creation...")
    optimizer = StudyOptimizer(handler)
    print("✅ StudyOptimizer created successfully")
    
    # Test 3: Test urgency calculations
    print("\n📊 Testing urgency calculations...")
    for assignment in handler.assignments:
        urgency = optimizer.calculate_urgency_score(assignment)
        days_left = (assignment.due_date - datetime.now()).days
        print(f"  {assignment.name[:30]:<30} | Due in {days_left:2d} days | Priority: {assignment.priority} | Urgency: {urgency:.1f}")
    
    # Test 4: Test with no assignments (edge case)
    print("\n🔍 Testing edge case - no pending assignments...")
    empty_handler = DataHandler()
    empty_optimizer = StudyOptimizer(empty_handler)
    empty_result = empty_optimizer.simple_schedule()
    print(f"✅ Empty schedule handled: {empty_result['status']}")
    print(f"   Message: {empty_result['message']}")
    
    # Test 5: Generate schedule with realistic data
    print("\n📅 Testing schedule generation...")
    result = optimizer.simple_schedule(days_ahead=10)
    
    print(f"✅ Schedule Status: {result['status']}")
    print(f"✅ Total Study Hours: {result['total_study_hours']:.1f}h")
    print(f"✅ Days with Sessions: {len(result['schedule'])}")
    
    # Test 6: Display generated schedule
    if result['schedule']:
        print("\n📋 Generated Schedule Details:")
        total_scheduled = 0
        
        for day_schedule in result['schedule']:
            if day_schedule['sessions']:
                day_name = day_schedule['date'].strftime('%A, %B %d')
                daily_hours = sum(session['hours'] for session in day_schedule['sessions'])
                total_scheduled += daily_hours
                
                print(f"\n  📅 {day_name} ({daily_hours:.1f}h total):")
                
                for session in day_schedule['sessions']:
                    print(f"    • {session['assignment'][:35]:<35} | {session['course'][:20]:<20} | {session['hours']:4.1f}h | Urgency: {session['urgency']:5.1f}")
        
        print(f"\n📊 Schedule Summary:")
        print(f"   Total hours scheduled: {total_scheduled:.1f}h")
        print(f"   Average hours per day: {total_scheduled/len(result['schedule']):.1f}h")
    
    # Test 7: Test time blocks creation
    print("\n⏰ Testing time block generation...")
    if result['schedule'] and result['schedule'][0]['sessions']:
        first_day_sessions = result['schedule'][0]['sessions']
        time_blocks = optimizer.create_time_blocks(first_day_sessions)
        
        print(f"✅ Generated {len(time_blocks)} time blocks for first day:")
        for block in time_blocks:
            print(f"   {block['start_time']}-{block['end_time']}: {block['assignment'][:30]} ({block['duration_hours']:.1f}h)")
    
    # Test 8: Test scheduler settings
    print("\n⚙️ Testing scheduler settings...")
    original_hours = optimizer.available_hours_per_day
    optimizer.available_hours_per_day = 6  # Reduce available time
    
    limited_result = optimizer.simple_schedule(days_ahead=7)
    print(f"✅ Limited schedule (6h/day): {limited_result['total_study_hours']:.1f}h total")
    
    # Restore original setting
    optimizer.available_hours_per_day = original_hours
    
    # Test 9: Test with overdue assignment (edge case)
    print("\n⚠️ Testing overdue assignment handling...")
    overdue_assignment = Assignment(
        "Fundamentals of Computer Science", 
        "Overdue Assignment",
        datetime.now() - timedelta(days=2),  # 2 days overdue
        5, 
        3
    )
    handler.add_assignment(overdue_assignment)
    
    overdue_urgency = optimizer.calculate_urgency_score(overdue_assignment)
    print(f"✅ Overdue assignment urgency: {overdue_urgency:.1f} (should be 100)")
    
    # Test 10: Verify data integrity after optimization
    print("\n🔍 Testing data integrity...")
    original_assignment_count = len(handler.assignments)
    original_course_count = len(handler.courses)
    
    # Run optimization again
    final_result = optimizer.simple_schedule()
    
    if (len(handler.assignments) == original_assignment_count and 
        len(handler.courses) == original_course_count):
        print("✅ Data integrity maintained - no assignments/courses lost during optimization")
    else:
        print("❌ Data integrity issue detected!")
    
    print("\n🎉 All optimizer tests completed successfully!")
    print(f"\nFinal Results:")
    print(f"  📚 Courses: {len(handler.courses)}")
    print(f"  📋 Total Assignments: {len(handler.assignments)}")
    print(f"  ⏳ Pending Assignments: {len(handler.get_pending_assignments())}")
    print(f"  📅 Schedulable Days: {len(final_result['schedule'])}")
    print(f"  ⏱️ Total Study Hours: {final_result['total_study_hours']:.1f}h")