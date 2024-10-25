import datetime

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped

from database import db_session


Base = db_session.base
class InterestsModel(Base):
    __tablename__ = "interests"
    id_i: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(VARCHAR(32), nullable=False)


class UserInterestsModel(Base):
    __tablename__ = "user_interests"
    id_ui: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    id_u: Mapped[int] = Column(Integer, ForeignKey('user.id_u', ondelete="CASCADE"), unique=True, nullable=False)
    id_i: Mapped[int] = Column(Integer, ForeignKey('interests.id_i', ondelete="CASCADE"), unique=True, nullable=False)


class GoalsModel(Base):
    __tablename__ = "goals"
    id_g: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(VARCHAR(32), nullable=False)
    desc: Mapped[str] = Column(VARCHAR(255), nullable=False)
    id_u: Mapped[int] = Column(Integer, ForeignKey('user.id_u', ondelete="CASCADE"), unique=True, nullable=False)


class LocalAchievements(Base):
    __tablename__ = "local_achievements"

    id_lach: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(VARCHAR(32), nullable=False)
    id_u: Mapped[int] = Column(Integer, ForeignKey('user.id_u'), nullable=False)


class LevelModel(Base):
    __tablename__ = "level"
    id_l: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    required_points: Mapped[int] = Column(Integer, nullable=False)

class GlobalAchievements(Base):
    __tablename__ = 'global_achievements'
    id_gach = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR, nullable=False)
    points = Column(Integer, nullable=False)
    id_u = Column(Integer, ForeignKey('user.id_u'), nullable=False)

class AchUser(Base):
    __tablename__ = 'ach_user'
    id_uach = Column(Integer, primary_key=True, autoincrement=True)
    id_u = Column(Integer, ForeignKey('user.id_u'), nullable=False)
    id_gach = Column(Integer, ForeignKey('global_achievements.id_gach'), nullable=False)
