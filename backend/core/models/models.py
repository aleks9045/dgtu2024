import datetime

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, func, TIMESTAMP
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

class GlobalAchievementsModel(Base):
    __tablename__ = 'global_achievements'
    id_gach = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR, nullable=False)
    points = Column(Integer, nullable=False)
    id_u = Column(Integer, ForeignKey('user.id_u'), nullable=False)

class AchUserModel(Base):
    __tablename__ = 'ach_user'
    id_uach = Column(Integer, primary_key=True, autoincrement=True)
    id_u = Column(Integer, ForeignKey('user.id_u'), nullable=False)
    id_gach = Column(Integer, ForeignKey('global_achievements.id_gach'), nullable=False)

class ChallengesModel(Base):
    __tablename__ = 'challenges'
    id_ch = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)
    desc = Column(VARCHAR, nullable=False)
    rules = Column(VARCHAR, nullable=False)
    status = Column(VARCHAR, nullable=False)
    points = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    start = Column(TIMESTAMP, nullable=False)
    end = Column(TIMESTAMP, nullable=False)
    photo = Column(VARCHAR, nullable=True)
    file = Column(VARCHAR, nullable=True)

class ChallUserModel(Base):
    __tablename__ = 'chall_user'
    id_chu = Column(Integer, primary_key=True, autoincrement=True)
    id_u = Column(Integer, ForeignKey('user.id_u'), nullable=False)
    id_ch = Column(Integer, ForeignKey('challenges.id_ch'), nullable=False)

class ChallAdmModel(Base):
    __tablename__ = 'chall_adm'
    id_cha = Column(Integer, primary_key=True, autoincrement=True)
    id_a = Column(Integer, ForeignKey('admin.id_a'), nullable=False)
    id_ch = Column(Integer, ForeignKey('challenges.id_ch'), nullable=False)