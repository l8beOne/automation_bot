from sqlalchemy import (
    Column,
    DATE,
    ForeignKey,
    Integer,
    MetaData,
    String,
    TIME
)
from sqlalchemy.orm import relationship

from .database import Base


# metadata = MetaData()


class SheduleSubjects(Base):
    __tablename__ = 'schedule_subjects'
    schedule_id = Column(Integer, ForeignKey('schedules.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)


class GroupUsers(Base):
    __tablename__ = 'group_users'
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class Subject(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    zoom_link = Column(String, nullable=True)
    type = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    classroom = Column(String, nullable=True)
    time = Column(TIME, nullable=False)
    schedules = relationship(
        'Schedule',
        secondary='schedule_subjects',
        back_populates='subjects'
    )
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    group = relationship('groups', back_populates='subjects', nullable=True)


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    date = Column(DATE, nullable=False)
    program_id = Column(Integer, ForeignKey('programs.id'))
    program = relationship('programs', back_populates='schedules')
    subjects = relationship(
        'Subject',
        secondary='schedule_subjects',
        back_populates='schedules',
        lazy='dynamic'
    )


class Program(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    schedules = relationship('shedules', back_populates='program', lazy='dynamic')
    users = relationship('users', back_populates='program', lazy='dynamic')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    groups = relationship(
        'Group',
        secondary='group_users',
        back_populates='users',
        lazy='dynamic'
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
        back_populates='groups',
        lazy='dynamic'
    )
    subjects = relationship('subjects', back_populates='group', lazy='dynamic')
