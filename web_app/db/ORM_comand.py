from sqlalchemy import func

from logger import logger
from web_app.db.create_data_func import session
from web_app.db.models import CourseModel, GroupModel, StudentModel


# Find all groups with less or equal student count:
def find_groups_with_student_count(student_count: int) -> list[GroupModel]:
    groups = session.query(GroupModel).join(GroupModel.students).group_by(GroupModel.id).having(
        func.count(StudentModel.id) <= student_count).all()
    return groups


# Find all students related to the course with a given name:
def find_students_related_to_the_course(course_name: str) -> list[StudentModel]:
    students = session.query(StudentModel).join(StudentModel.courses).filter(CourseModel.name == course_name).all()
    return students


# Add a new student:
def add_new_student(first_name: str, last_name: str) -> None:
    try:
        new_student = StudentModel(first_name=first_name, last_name=last_name)
        session.add(new_student)
        session.commit()
        logger.info("Student added successfully")
    except Exception as e:
        logger.error("Error adding student: %s", str(e))


# Delete student by STUDENT_ID:
def del_student(student_id: int) -> None:
    try:
        student = session.query(StudentModel).get(student_id)
        session.delete(student)
        session.commit()
        logger.info("Student deleted successfully")
    except Exception as e:
        logger.error("Error by deleted student", str(e))


# Add a student to the course (from a list):
def add_student_to_the_course(student_id: int, course_id: int) -> None:
    try:
        student = session.query(StudentModel).get(student_id)
        course = session.query(CourseModel).get(course_id)
        student.courses.append(course)
        session.commit()
        logger.info("Student was added successfully")
    except Exception as e:
        logger.error("Error by adding student: %s", str(e))


# Remove the student from one of his or her courses:
def remove_student_to_other_course(student_id: int, course_id: int):
    try:
        student = session.query(StudentModel).get(student_id)
        course = session.query(CourseModel).get(course_id)
        if course in student.courses:
            student.courses.remove(course)
            session.commit()
            logger.info("Student was removed from the course")
        else:
            logger.warning("Course is not associated with the student")
    except Exception as e:
        logger.error("Error: %s", str(e))


if __name__ == '__main__':
    pass
