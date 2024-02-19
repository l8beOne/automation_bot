from sqlalchemy import (
    Column,
    DATE,
    ForeignKey,
    Integer,
    MetaData,
    String,
    TIME,
    Table
)
from sqlalchemy.orm import relationship

from .database import Base


metadata = MetaData()


group_users = Table(
    'group_users',
    metadata,
    Column('group_id', ForeignKey('groups.id'), primary_key=True),
    Column('users_id', ForeignKey('users.id'), primary_key=True)
)


schedule_subjects = Table(
    'schedule_subjects',
    metadata,
    Column('schedule_id', ForeignKey('schedules.id'), primary_key=True),
    Column('subject_id', ForeignKey('subjects.id'), primary_key=True)
)


class Subject(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    zoom_link = Column(String)
    type = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    classroom = Column(String, nullable=False)
    time = Column(TIME, nullable=False)
    schedules = relationship(
        'Schedule',
        secondary='schedule_subjects',
        back_populates='subjects'
    )
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('groups', back_populates='subjects')


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    date = Column(DATE, nullable=False)
    program_id = Column(Integer, ForeignKey('programs.id'))
    program = relationship('programs', back_populates='schedules')
    subjects = relationship(
        'Subject',
        secondary='schedule_subjects',
        back_populates='schedules'
    )


class Program(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    schedules = relationship('shedules', back_populates='program')
    users = relationship('users', back_populates='program')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    groups = relationship(
        'Group',
        secondary='group_users',
        back_populates='users'
    )
    program_id = Column(Integer, ForeignKey('programs.id'))
    program = relationship('programs', back_populates='users')


class Group(Base):
    __tablename__ = 'groups',
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    users = relationship(
        'User',
        secondary='group_users',
        back_populates='groups'
    )
    subjects = relationship('subjects', back_populates='group')
