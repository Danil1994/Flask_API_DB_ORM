from web_app.db.create_data_func import (create_10_course,
                                         create_random_groups, create_students,
                                         random_assign_course_for_student,
                                         random_assign_students_to_groups)

groups = create_random_groups(10)
course = create_10_course()

first_names = ['John', 'Alice', 'Michael', 'Emily', 'David', 'Olivia', 'Daniel', 'Emma', 'Matthew', 'Sophia']
last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Miller', 'Wilson', 'Anderson', 'Clark', 'Walker', 'Hill']


students = create_students(first_names, last_names)

random_assign_students_to_groups(students, groups)
random_assign_course_for_student(students, course)

if __name__ == '__main__':
    pass
