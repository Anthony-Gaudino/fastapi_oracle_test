from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from . import models, schemas


# Department
################################################################################

def get_departments(db: Session):
    return db.query(models.Department).all()

def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(
                models.Department.department_code == department_id
            ).first()

# Badges
################################################################################

def get_badges(db: Session):
    return db.query(models.Badge).all()

def get_badge(db: Session, badge_number: int):
    return db.query(models.Badge).filter(
                models.Badge.badge_number == badge_number
            ).all()

def get_active_badges(db: Session):
    return db.query(models.Badge).filter(
                models.Badge.badge_status == "Active",
                models.Badge.badge_expiry_date > func.current_date()
            ).all()

# Job titles
################################################################################

def get_job_titles(db: Session):
    return db.query(models.JobTitle).all()

def get_job_titles_from_department(db: Session, department_name: str):
    return db.query(models.JobTitle)\
            .join(models.Department, isouter=True).filter(
                models.Department.department_name == department_name
            ).all()

# Employees
################################################################################

def get_employees(db: Session):
    return db.query(models.Employee).all()

def get_active_employees(db: Session):
    return db.query(models.Employee).filter(or_(
                models.Employee.leave_date == None,
                models.Employee.leave_date > func.current_date()
            )).all()

def get_job_employees_from_department(db: Session, department_name: str):
    return db.query(models.Employee)\
            .join(models.JobTitle, isouter=True)\
            .join(models.Department, isouter=True).filter(
                models.Department.department_name == department_name
            ).all()
