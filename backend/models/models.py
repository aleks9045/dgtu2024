import datetime

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, func, TIMESTAMP, BOOLEAN, UUID
from sqlalchemy.orm import Mapped

from database import db_session

Base = db_session.base


class BaseUserModel(Base):
    __tablename__ = "base_user"
    id_bu: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    uu_id: Mapped[str] = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name: Mapped[str] = Column(VARCHAR(32), nullable=False)
    surname: Mapped[str] = Column(VARCHAR(32), nullable=False)

    email: Mapped[str] = Column(VARCHAR(64), nullable=False, unique=True)
    password: Mapped[str] = Column(VARCHAR(1024), nullable=False)
    photo: Mapped[str] = Column(VARCHAR(255), nullable=True, default=f'/media/user_photos/default.png')
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    public_columns = (name, surname, email, photo, created_at)


class UserModel(Base):
    __tablename__ = "user"
    id_u: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    points: Mapped[int] = Column(Integer, default=0)
    base_user: Mapped[int] = Column(Integer, ForeignKey('base_user.id_bu', ondelete="CASCADE"), unique=True,
                                    nullable=False)

    public_columns = (id_u, points)


class AdminModel(Base):
    __tablename__ = "admin"
    id_a: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    base_user: Mapped[int] = Column(Integer, ForeignKey('base_user.id_bu', ondelete="CASCADE"), unique=True,
                                    nullable=False)


class InterestsModel(Base):
    __tablename__ = 'interests'
    id_i: Mapped[bool] = Column(Integer, primary_key=True, autoincrement=True)
    sport: Mapped[bool] = Column(BOOLEAN, nullable=False)
    cooking: Mapped[bool] = Column(BOOLEAN, nullable=False)
    art: Mapped[bool] = Column(BOOLEAN, nullable=False)
    tech: Mapped[bool] = Column(BOOLEAN, nullable=False)
    communication: Mapped[bool] = Column(BOOLEAN, nullable=False)
    literature: Mapped[bool] = Column(BOOLEAN, nullable=False)
    animals: Mapped[bool] = Column(BOOLEAN, nullable=False)
    games: Mapped[bool] = Column(BOOLEAN, nullable=False)
    music: Mapped[bool] = Column(BOOLEAN, nullable=False)
    films: Mapped[bool] = Column(BOOLEAN, nullable=False)
    id_u: Mapped[int] = Column(Integer, ForeignKey('user.id_u', ondelete="CASCADE"), unique=True, nullable=False)



class GoalsModel(Base):
    __tablename__ = "goals"
    id_g: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(VARCHAR(32), nullable=False)
    desc: Mapped[str] = Column(VARCHAR(255), nullable=False)
    id_u: Mapped[int] = Column(Integer, ForeignKey('user.id_u', ondelete="CASCADE"), nullable=False)


class LocalAchievementsModel(Base):
    __tablename__ = "local_achievements"

    id_lach: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(VARCHAR(32), nullable=False)
    id_u: Mapped[int] = Column(Integer, ForeignKey('goals.id_g'), nullable=False)


class LevelModel(Base):
    __tablename__ = "level"
    id_l: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    required_points: Mapped[int] = Column(Integer, nullable=False)


class GlobalAchievementsModel(Base):
    __tablename__ = 'global_achievements'
    id_gach: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(VARCHAR, nullable=False)
    points: Mapped[int] = Column(Integer, nullable=False)


class GAchUserModel(Base):
    __tablename__ = 'gach_user'
    id_uach: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    id_u: Mapped[int] = Column(Integer, ForeignKey('user.id_u'), nullable=False)
    id_gach: Mapped[int] = Column(Integer, ForeignKey('global_achievements.id_gach'), nullable=False)


class ChallengesModel(Base):
    __tablename__ = 'challenges'
    id_ch: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(VARCHAR, nullable=False)
    desc: Mapped[str] = Column(VARCHAR, nullable=True)
    rules: Mapped[str] = Column(VARCHAR, nullable=False)
    status: Mapped[str] = Column(VARCHAR, nullable=False)
    points: Mapped[int] = Column(Integer, nullable=False)
    created_at: Mapped[datetime] = Column(TIMESTAMP, nullable=False)
    start: Mapped[datetime] = Column(TIMESTAMP, nullable=False)
    end: Mapped[datetime] = Column(TIMESTAMP, nullable=False)
    photo: Mapped[str] = Column(VARCHAR, nullable=True)
    file: Mapped[str] = Column(VARCHAR, nullable=True)
    accepted: Mapped[bool] = Column(BOOLEAN, nullable=False)


class UserChallModel(Base):
    __tablename__ = 'user_chall'
    id_chu: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    id_u: Mapped[int] = Column(Integer, ForeignKey('user.id_u'), nullable=False)
    id_ch: Mapped[int] = Column(Integer, ForeignKey('challenges.id_ch'), nullable=False)
