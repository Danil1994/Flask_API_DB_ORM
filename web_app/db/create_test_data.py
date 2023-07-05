import psycopg2
from config import conn_params

from sqlalchemy import create_engine

from web_app.db.func_to_create_data import (create_10_course,
                                            create_random_groups, create_students,
                                            random_assign_course_for_student,
                                            random_assign_students_to_groups)

# Создание соединения SQLAlchemy
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)

# Создание соединения с базой данных
conn = psycopg2.connect(**conn_params)


def create_test_data_in_db():
    groups = create_random_groups(10)
    course = create_10_course()

    first_names = ['John', 'Alice', 'Michael', 'Emily', 'David', 'Olivia', 'Daniel', 'Emma', 'Matthew', 'Sophia']
    last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Miller', 'Wilson', 'Anderson', 'Clark', 'Walker', 'Hill']
    students = create_students(first_names, last_names)

    random_assign_students_to_groups(students, groups)
    random_assign_course_for_student(students, course)


if __name__ == '__main__':
    create_test_data_in_db()
