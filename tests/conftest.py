import warnings
import pytest
import sqlalchemy
from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
from painless_sqlalchemy.BaseModel import Base, engine, session
from painless_sqlalchemy.Model import Model
from painless_sqlalchemy.elements.MapColumn import MapColumn

table_hierarchy = [
    'student', 'teacher', 'classroom', 'school'
]


@pytest.fixture(scope='session')
def School():
    class School(Model):
        __tablename__ = 'school'
        id = Column(Integer, primary_key=True, info={"exposed": True})

        classrooms = relationship(
            'Classroom',
            primaryjoin='School.id == Classroom.school_id'
        )

    return School


@pytest.fixture(scope='session')
def Classroom(School):
    class Classroom(Model):
        __tablename__ = 'classroom'

        school_id = Column(Integer, ForeignKey(School.id))
        school = relationship(
            School, foreign_keys=school_id,
            primaryjoin="School.id == Classroom.school_id"
        )

        teacher = relationship(
            "Teacher",
            primaryjoin="Classroom.id == Teacher.classroom_id",
            uselist=False
        )

    return Classroom


@pytest.fixture(scope='session')
def Teacher(Classroom):
    class Teacher(Model):
        __tablename__ = 'teacher'

        name = Column(String(64), index=True, nullable=False)

        classroom_id = Column(Integer, ForeignKey(Classroom.id), unique=True)
        classroom = relationship(
            Classroom, foreign_keys=classroom_id,
            primaryjoin="Classroom.id == Teacher.classroom_id"
        )
        students = relationship(
            'Student',
            secondary='teacher_to_student',
            primaryjoin='Teacher.id == teacher_to_student.c.teacher_id',
            secondaryjoin='teacher_to_student.c.student_id == Student.id'
        )

    return Teacher


@pytest.fixture(scope='session')
def Student(Teacher):
    class Student(Model):
        __tablename__ = 'student'

        name = Column(String(64), index=True, nullable=False)
        address = Column(String(64), index=False, nullable=True)
        phone = Column(String(35), nullable=True)
        home_phone = Column(String(35), nullable=True)
        email = Column(String(64), nullable=True)

        phone_numbers = MapColumn(['phone', 'home_phone'])

        contact_info = MapColumn({
            'phone': 'phone',
            'home_phone': 'home_phone',
            'email': 'email'
        })

        teachers = relationship(
            "Teacher", secondary='teacher_to_student',
            primaryjoin="Student.id == teacher_to_student.c.student_id",
            secondaryjoin="teacher_to_student.c.teacher_id == Teacher.id"
        )

    # teacher_to_student linkage table
    Table(
        'teacher_to_student',
        Base.metadata,
        Column('teacher_id', ForeignKey(Teacher.id, ondelete='CASCADE'),
               primary_key=True),
        Column('student_id', ForeignKey(Student.id, ondelete='CASCADE'),
               primary_key=True)
    )

    return Student


@pytest.fixture(scope='session', autouse=True)
def init_db(School, Classroom, Teacher, Student):
    recreate_db()

    from tests.helper.AbstractDatabaseTest import batch_testing
    if not batch_testing:  # pragma: no cover
        warnings.warn(
            "Running in Check Mode. This is expensive and should "
            "not be used to execute the whole test suite!"
        )


def recreate_db():
    engine.dispose()
    session.close()

    uri, db = engine.url.__str__().rsplit("/", 1)

    _engine = sqlalchemy.engine.create_engine(uri + "/postgres")
    conn = _engine.connect()
    conn.execute(
        "SELECT pg_terminate_backend(pid) "
        "FROM pg_stat_activity WHERE datname = '%s';" % db
    )
    conn.execute("commit")
    conn.execute('DROP DATABASE IF EXISTS "%s";' % db)
    conn.execute("commit")
    conn.execute('CREATE DATABASE "%s";' % db)
    conn.close()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def pytest_itemcollected(item):
    """ Format output as TestClass: TestName """
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    item._nodeid = ': '.join((pref, suf))
