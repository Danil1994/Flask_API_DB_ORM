import psycopg2
from config import conn_params

from sqlalchemy import create_engine, text

from web_app.db.func_to_create_data import (create_10_course,
                                            create_random_groups, create_students,
                                            random_assign_course_for_student,
                                            random_assign_students_to_groups)
from web_app.db.models import ALL_MODELS, student_course_association
from sqlalchemy.orm import sessionmaker

# Connect to DB
conn = psycopg2.connect(**conn_params)

# Create session SQLAlchemy
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
Session = sessionmaker(bind=engine)
session = Session()


def reset_auto_increment(table_name, column_name):
    query = text(f"ALTER SEQUENCE {table_name}_{column_name}_seq RESTART WITH 1")
    session.execute(query)
    session.commit()


def clean_table():
    delete_stmt = student_course_association.delete()
    session.execute(delete_stmt)
    session.commit()

    for model in ALL_MODELS:
        session.query(model).delete()
    session.commit()


def create_test_data_in_db():
    clean_table()

    for model in ALL_MODELS:
        reset_auto_increment(model.__tablename__, 'id')

    groups = create_random_groups(10)
    course = create_10_course()

    first_names = ['John', 'Alice', 'Michael', 'Emily', 'David', 'Olivia', 'Daniel', 'Emma', 'Matthew', 'Sophia']
    last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Miller', 'Wilson', 'Anderson', 'Clark', 'Walker', 'Hill']
    students = create_students(first_names, last_names)

    random_assign_students_to_groups(students, groups)
    random_assign_course_for_student(students, course)


if __name__ == '__main__':
    create_test_data_in_db()
