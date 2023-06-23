import random
import string

import psycopg2
from models import CourseModel, GroupModel, StudentModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conn_params = {
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'task_10_db',
    'user': 'postgres',
    'password': '1111'
}

# Connect to DB
conn = psycopg2.connect(**conn_params)

# Create the database engine and session
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
Session = sessionmaker(bind=engine)
session = Session()

# Create 10 groups with randomly generated names
groups = []
for _ in range(10):
    name = ''.join(random.choices(string.ascii_uppercase, k=2)) + '-' + ''.join(random.choices(string.digits, k=2))
    group = GroupModel(name=name)
    groups.append(group)
session.add_all(groups)
session.commit()

# Create 10 courses
courses = [
    CourseModel(name="Math", description="Math course"),
    CourseModel(name="Biology", description="Biology course"),
    CourseModel(name="Physics", description="Physics course"),
    CourseModel(name="Chemistry", description="Chemistry course"),
    CourseModel(name="History", description="History course"),
    CourseModel(name="Literature", description="Literature course"),
    CourseModel(name="Computer Science", description="Computer Science course"),
    CourseModel(name="Art", description="Art course"),
    CourseModel(name="Music", description="Music course"),
    CourseModel(name="Physical Education", description="Physical Education course")
]
session.add_all(courses)
session.commit()

# Generate student names
first_names = ['John', 'Alice', 'Michael', 'Emily', 'David', 'Olivia', 'Daniel', 'Emma', 'Matthew', 'Sophia']
last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Miller', 'Wilson', 'Anderson', 'Clark', 'Walker', 'Hill']

# Create 200 students with randomly assigned names and groups
students = []
for _ in range(200):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    student = StudentModel(first_name=first_name, last_name=last_name)
    students.append(student)
session.add_all(students)
session.commit()

# Randomly assign students to groups
for student in students:
    group = random.choice(groups)
    student.group = group
session.commit()

# Randomly assign 1 to 3 courses for each student
for student in students:
    num_courses = random.randint(1, min(3, len(courses)))  # Limit num_courses to the available number of courses
    student.courses = random.sample(courses, num_courses)
session.commit()

if __name__ == '__main__':
    pass
