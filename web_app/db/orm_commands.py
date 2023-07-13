from __future__ import annotations

from typing import Any, Dict, List, Tuple, Union

import sqlalchemy
from sqlalchemy import func

from config import create_db_engine_and_session
from logger import logger

from web_app.db.models import CourseModel, GroupModel, StudentModel

session = create_db_engine_and_session()


# Find all groups with less or equal student count:
def find_groups_with_student_count(student_count: int, session: sqlalchemy.orm.Session = session) -> list[GroupModel]:
    try:
        groups = session.query(GroupModel).join(GroupModel.students).group_by(GroupModel.id).having(
            func.count(StudentModel.id) <= student_count).all()
        return groups
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


# Find all students related to the course with a given name:
def find_students_related_to_the_course(course_name: str, session: sqlalchemy.orm.Session = session) -> \
        list[StudentModel] | str:
    try:
        students = session.query(StudentModel).join(StudentModel.courses).filter(
            CourseModel.name == course_name.capitalize()).all()
        return students
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


# Add a new student:
def create_new_student(first_name: str, last_name: str) -> dict[str, str]:
    try:
        new_student = StudentModel(first_name=first_name.capitalize(), last_name=last_name.capitalize())
        session.add(new_student)
        session.commit()
        logger.info('Student created successfully')
        return {'Response': f"New student {first_name, last_name} created successfully"}
    except Exception as e:
        logger.error("Error adding student: %s", str(e))
        return {'Response error': str(e)}


# Delete student by STUDENT_ID:
def delete_student(student_id: int) -> dict[str, str]:
    try:
        student = session.query(StudentModel).get(student_id)
        if student is None:
            logger.info(f"Student {student_id} doesn`t exist")
            return {'Response error': f"Student {student_id} doesn`t exist"}
        else:
            session.delete(student)
            session.commit()
            logger.info("Student deleted successfully")
            return {'Response': f"Student {student_id} deleted successfully"}
    except Exception as e:
        logger.error("Error by deleted student", str(e))
        return {'Response error': str(e)}


# Add a student to the course (from a list):
def add_student_to_the_course(student_id: int, course_id: int) -> dict[str, str]:
    try:
        student = session.query(StudentModel).get(student_id)
        course = session.query(CourseModel).get(course_id)
        if student is None:
            logger.info(f"Student {student_id} doesn`t exist")
            return {'Response error': f"Student {student_id} doesn`t exist"}
        elif course is None:
            logger.info(f"Courser {course_id} doesn`t exist")
            return {'Response error': f"Courser {course_id} doesn`t exist"}
        else:
            student.courses.append(course)
            session.commit()
            logger.info("Student was added successfully")
            return {'Response': f"Student {student_id} was added successfully to the course {course_id}"}
    except Exception as e:
        logger.error("Error by adding student: %s", str(e))
        return {'Response error': str(e)}


# Remove the student from one of his or her courses:
def remove_student_from_course(student_id: int, course_id: int) -> dict[str, str]:
    try:
        student = session.query(StudentModel).get(student_id)
        course = session.query(CourseModel).get(course_id)

        if course in student.courses:
            student.courses.remove(course)
            session.commit()
            logger.info(f"Student {student_id}  was removed from the course {course_id}")
            return {'Response': f"Student {student_id}  was removed from the course {course_id}"}
        else:
            logger.warning("Course is not associated with the student")
            return {'Response error': "Course is not associated with the student"}

    except Exception as e:
        logger.error("Error: %s", str(e))


if __name__ == '__main__':
    pass
