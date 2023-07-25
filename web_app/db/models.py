from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class StudentCourseAssociation(Base):
    __tablename__ = 'student_course_association'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)

    student = relationship("StudentModel")
    course = relationship("CourseModel")

    def __repr__(self):
        return f"StudentCourseAssociation(student_id={self.student_id}, course_id={self.course_id})"


class GroupModel(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship("StudentModel", back_populates="group")

    def __repr__(self):
        return f"Group '{self.name}' id={self.id}"


class StudentModel(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    first_name = Column(String)
    last_name = Column(String)

    group = relationship("GroupModel", back_populates="students")
    courses = relationship("CourseModel", secondary=StudentCourseAssociation.__table__, back_populates="students",
                           overlaps="student")

    def __repr__(self):
        return f"Student id={self.id}, group_id={self.group_id}, " \
               f"first_name='{self.first_name}', last_name='{self.last_name}' "


class CourseModel(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    students = relationship("StudentModel", secondary=StudentCourseAssociation.__table__, back_populates="courses",
                            overlaps="student")


ALL_MODELS = [StudentModel, CourseModel, GroupModel]

if __name__ == '__main__':
    pass
