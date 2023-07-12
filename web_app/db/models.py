from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table

Base = declarative_base()

student_course_association = Table('student_course_association', Base.metadata,
                                   Column('student_id', Integer, ForeignKey('student.id')),
                                   Column('course_id', Integer, ForeignKey('course.id'))
                                   )


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
    courses = relationship("CourseModel", secondary="student_course_association", back_populates="students")

    def __repr__(self):
        return f"Student(id={self.id}, group_id={self.group_id}, " \
               f"first_name='{self.first_name}', last_name='{self.last_name}')"


class CourseModel(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    students = relationship("StudentModel", secondary="student_course_association", back_populates="courses")


ALL_MODELS = [StudentModel, CourseModel, GroupModel]

if __name__ == '__main__':
    pass
