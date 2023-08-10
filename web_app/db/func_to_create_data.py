"""funcs generating random data to the DB."""
import random
import string

from config import create_db_engine_and_session
from web_app.db.models import CourseModel, GroupModel, StudentModel

session = create_db_engine_and_session()


# Create 10 groups with randomly generated names
def create_random_groups(count_of_group: int) -> list[GroupModel]:
    groups = []
    for _ in range(count_of_group):
        name = ''.join(random.choices(string.ascii_uppercase, k=2)) + '-' + ''.join(random.choices(string.digits, k=2))
        group = GroupModel(name=name)
        groups.append(group)
    session.add_all(groups)
    session.commit()
    return groups


# Create 10 courses
def create_10_course() -> list[CourseModel]:
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
    return courses


# Create 200 students with randomly assigned names and groups
def create_students(list_of_first_name: list[str], list_of_last_name: list[str]) -> list[StudentModel]:
    students = []
    for _ in range(200):
        first_name = random.choice(list_of_first_name)
        last_name = random.choice(list_of_last_name)
        student = StudentModel(first_name=first_name, last_name=last_name)
        students.append(student)
    session.add_all(students)
    session.commit()
    return students


# Randomly assign students to groups
def random_assign_students_to_groups(students: list, groups: list) -> None:
    for student in students:
        group = random.choice(groups)
        student.group = group
    session.commit()


# Randomly assign 1 to 3 courses for each student
def random_assign_course_for_student(students: list, courses: list) -> None:
    for student in students:
        num_courses = random.randint(1, min(3, len(courses)))  # Limit num_courses to the available number of courses
        student.courses = random.sample(courses, num_courses)
    session.commit()


if __name__ == '__main__':
    pass
