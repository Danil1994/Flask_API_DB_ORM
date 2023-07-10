import psycopg2
from config import conn_params

from sqlalchemy import create_engine

from web_app.db.func_to_create_data import (create_10_course,
                                            create_random_groups, create_students,
                                            random_assign_course_for_student,
                                            random_assign_students_to_groups)
from web_app.db.models import GroupModel, StudentModel, CourseModel, student_course_association
from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker

# Connect to DB
conn = psycopg2.connect(**conn_params)

# Create session SQLAlchemy
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
Session = sessionmaker(bind=engine)
session = Session()


def clean_table():
    delete_stmt = student_course_association.delete()
    session.execute(delete_stmt)
    session.commit()

    session.query(StudentModel).delete()
    session.query(GroupModel).delete()

    session.query(CourseModel).delete()
    session.commit()


def create_test_data_in_db():
    clean_table()
    groups = create_random_groups(10)
    course = create_10_course()

    first_names = ['John', 'Alice', 'Michael', 'Emily', 'David', 'Olivia', 'Daniel', 'Emma', 'Matthew', 'Sophia']
    last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Miller', 'Wilson', 'Anderson', 'Clark', 'Walker', 'Hill']
    students = create_students(first_names, last_names)

    random_assign_students_to_groups(students, groups)
    random_assign_course_for_student(students, course)


if __name__ == '__main__':
    pass
