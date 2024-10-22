from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, UUID
from sqlalchemy.orm import Mapped

from database import db_session

Base = db_session.base


class BaseUserModel(Base):
    __tablename__ = "baseuser"
    id_bu: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    uu_id: Mapped[str] = Column(UUID(as_uuid=True), nullable=False, unique=True)
    first_name: Mapped[str] = Column(VARCHAR(32), nullable=False)
    last_name: Mapped[str] = Column(VARCHAR(32), nullable=False)
    father_name: Mapped[str] = Column(VARCHAR(32), nullable=True)
    email: Mapped[str] = Column(VARCHAR(64), nullable=False, unique=True)
    password: Mapped[str] = Column(VARCHAR(1024), nullable=False)
    photo: Mapped[str] = Column(VARCHAR(255), nullable=True)

    public_columns = (first_name, last_name, father_name, email, photo)


class UserModel(Base):
    __tablename__ = "user"
    id_u: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    about: Mapped[str] = Column(VARCHAR(255), nullable=True)
    baseuser: Mapped[int] = Column(Integer, ForeignKey('baseuser.id_bu', ondelete="CASCADE"), unique=True,
                                   nullable=False)

    public_columns = (id_u, about)


class AdminModel(Base):
    __tablename__ = "admin"
    id_a: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    baseuser: Mapped[int] = Column(Integer, ForeignKey('baseuser.id_bu', ondelete="CASCADE"), unique=True,
                                   nullable=False)

# class MarkModel(Base):
#     __tablename__ = "mark"
#     id_m = Column(Integer, primary_key=True, autoincrement=True)
#     design = Column(Integer, nullable=False)
#     usability = Column(Integer, nullable=False)
#     backend = Column(Integer, nullable=False)
#     frontend = Column(Integer, nullable=False)
#     realization = Column(Integer, nullable=False)
#     comment = Column(VARCHAR(255), nullable=True)
#     user = Column(Integer, ForeignKey('baseuser.id_bu', ondelete="CASCADE"), nullable=True)
#     job = Column(Integer, ForeignKey('job.id_j', ondelete="CASCADE"), nullable=True)


# class CaseModel(Base):
#     __tablename__ = "case"
#     id_ca = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(VARCHAR(64), nullable=False, unique=True)
#     about = Column(VARCHAR(255), nullable=True)
#     file = Column(VARCHAR(255), nullable=True)
#     company = Column(Integer, ForeignKey('company.id_co', ondelete="CASCADE"), nullable=True)


# class CompanyModel(Base):
#     __tablename__ = "company"
#     id_co = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(VARCHAR(32), nullable=False)
#
#
# class TeamModel(Base):
#     __tablename__ = "team"
#     id_t = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(VARCHAR(32), nullable=False, unique=True)
#     about = Column(VARCHAR(255), nullable=True)
#     banner = Column(VARCHAR(255), nullable=True)

# class JobModel(Base):
#     __tablename__ = "job"
#     id_j = Column(Integer, primary_key=True, autoincrement=True)
#     github = Column(VARCHAR(255), nullable=True)
#     case = Column(Integer, ForeignKey('case.id_ca', ondelete="CASCADE"), nullable=False)
#     team = Column(Integer, ForeignKey('team.id_t', ondelete="CASCADE"), nullable=False, unique=True)
#
#
# class InviteModel(Base):
#     __tablename__ = "invited"
#     id_i = Column(Integer, primary_key=True, autoincrement=True)
#     user = Column(Integer, ForeignKey('user.id_u', ondelete="CASCADE"), nullable=True)
#     team = Column(Integer, ForeignKey('team.id_t', ondelete="CASCADE"), nullable=True)
