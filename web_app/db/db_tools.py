import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from config import conn_params
from web_app.db.create_data_func import (create_10_course,
                                         create_random_groups, create_students,
                                         random_assign_course_for_student,
                                         random_assign_students_to_groups)


def create_db_table():
    # Connect to DB
    conn = psycopg2.connect(**conn_params)

    # Create session SQLAlchemy
    engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)

    Base = declarative_base()
    Base.metadata.create_all(engine)


def create_test_data_in_db():
    groups = create_random_groups(10)
    course = create_10_course()

    first_names = ['John', 'Alice', 'Michael', 'Emily', 'David', 'Olivia', 'Daniel', 'Emma', 'Matthew', 'Sophia']
    last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Miller', 'Wilson', 'Anderson', 'Clark', 'Walker', 'Hill']
    students = create_students(first_names, last_names)

    random_assign_students_to_groups(students, groups)
    random_assign_course_for_student(students, course)


if __name__ == '__main__':
    pass
