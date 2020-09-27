from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class Badge(Base):
    __tablename__ = "badge"

    badge_number      = Column(Integer, primary_key=True, index=True)
    badge_status      = Column(String(length=10))
    badge_expiry_date = Column(Date)

    emp_ref = relationship("Employee", back_populates="bdg_ref")

class Department(Base):
    __tablename__ = "department"

    department_code = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(length=50))

    jt_ref = relationship("JobTitle", back_populates="dep_ref")

class Employee(Base):
    __tablename__ = "employee"

    id             = Column(Integer, primary_key=True, index=True)
    firstname      = Column(String(length=100))
    lastname       = Column(String(length=100))
    badge_number   = Column(Integer, ForeignKey("badge.badge_number"))
    country_code   = Column(String(length=10))
    job_title_code = Column(Integer, ForeignKey("job_title.job_title_code"))
    start_date     = Column(Date)
    leave_date     = Column(Date)

    jt_ref  = relationship("JobTitle", back_populates="emp_ref", uselist=False)
    bdg_ref = relationship("Badge",    back_populates="emp_ref", uselist=False)

class JobTitle(Base):
    __tablename__ = "job_title"

    job_title_code  = Column(Integer, primary_key=True, index=True)
    job_title_name  = Column(String(length=50))
    department_code = Column(Integer, ForeignKey("department.department_code"))

    dep_ref = relationship("Department", back_populates="jt_ref", uselist=False)
    emp_ref = relationship("Employee",   back_populates="jt_ref")
