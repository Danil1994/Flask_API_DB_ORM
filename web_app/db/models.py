import psycopg2
from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship

conn_params = {
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'task_10_db',
    'user': 'postgres',
    'password': '1111'
}

# Connect to DB
conn = psycopg2.connect(**conn_params)

# Create session SQLAlchemy
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)

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


class StudentModel(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    first_name = Column(String)
    last_name = Column(String)

    group = relationship("GroupModel", back_populates="students")
    courses = relationship("CourseModel", secondary=student_course_association, back_populates="students")


class CourseModel(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    students = relationship("StudentModel", secondary=student_course_association, back_populates="courses")


Base.metadata.create_all(engine)

if __name__ == '__main__':
    pass
