from typing import List
import secrets
import requests
import json

from fastapi import Depends, FastAPI, HTTPException, Response, status, Path
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, \
        HTTP_503_SERVICE_UNAVAILABLE
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()

security = HTTPBasic()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_authenticated(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(credentials.password, "pass")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


# Department
################################################################################

@app.get("/department",
    tags=["Department"],
    response_model=List[schemas.Department],
    summary="Gets all departments",
    response_description="A list containing all departments"
)
def get_departments(
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
    ):
    """Gets all departments."""
    return crud.get_departments(db)

# Badges
################################################################################

@app.get(
    "/badges",
    tags=["Badges"],
    response_model=List[schemas.Badge],
    summary="Gets all badges",
    response_description="A list containing all badges"
)
def get_badges(
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
    ):
    """Gets all badges."""
    return crud.get_badges(db)

@app.get(
    "/badges/active",
    tags=["Badges"],
    response_model=List[schemas.Badge],
    summary="Gets all active badges",
    response_description="A list containing all active badges",
    responses={404: {"model": None, "description": "No active badges found"}}
)
def get_active_badges(
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
    ):
    """Gets all active badges."""
    res = crud.get_active_badges(db)

    if not res:
        return Response(
            "No active badges found",
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )

    return res

@app.get(
    "/badges{badge_number}",
    tags=["Badges"],
    response_model=List[schemas.Badge],
    summary="Gets a single badge",
    response_description="A list containing the badge with the provided ID",
    responses={404: {"model": None, "description": "Badge not found"}}
)
def get_badge(
        badge_number: int = Path(
            ...,
            title="Badge number",
            description="Badge number",
            gt=0
        ),
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
    ):
    """
    Gets a badge:

    - **Badge number**: The badge ID
    """
    res = crud.get_badge(db, badge_number)

    if not res:
        return Response(
            'Badge not found',
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )

    return res

# Job titles
################################################################################

@app.get(
    "/job_titles",
    tags=["Job titles"],
    response_model=List[schemas.JobTitle],
    summary="Gets all job titles",
    response_description="A list containing all job titles"
)
def get_job_titles(
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
    ):
    """Gets all job titles."""
    return crud.get_job_titles(db)

@app.get(
    "/job_titles/:{department_name}",
    tags=["Job titles"],
    response_model=List[schemas.JobTitle],
    summary="Gets all job titles in the given department",
    response_description="A list containing all job titles in the department",
    responses={
        404: {"model": None, "description": "Job title not found in department"}
    }
)
def get_job_titles_from_department(
        department_name: str = Path(
            ...,
            title="Department name",
            description="Department name",
            max_length=50
        ),
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
    ):
    """
    Gets job titles in department:

    - **Department name**: name of the department
    """
    res = crud.get_job_titles_from_department(db, department_name)

    if not res:
        return Response(
            f"No job titles in the department {department_name} or department" \
            " doesn't exist",
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )

    return res

# Employees
################################################################################

def add_country_names(employees):
    """Replaces country codes by country names in employees list"""
    try:
        resp = requests.get(
            f"https://restcountries.eu/rest/v2/all?fields=name;alpha3Code;alpha2Code",
            timeout=3
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Can't obtain country names from restcountries.eu",
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Can't obtain country names from restcountries.eu",
        )

    resp = resp.json()

    for i in employees:
        cc = i.country_code.upper()

        i.country_code = "".join([c["name"] for c in resp 
            if c["alpha3Code"] == cc or c["alpha2Code"] == cc])


@app.get(
    "/employees",
    tags=["Employees"],
    response_model=List[schemas.EmployeeWithCountry],
    summary="Gets all employees",
    response_description="A list containing all employees"
)
def get_employees(
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
        ):
    """Gets all employees."""
    res = crud.get_employees(db)

    add_country_names(res)

    return res

@app.get(
    "/employees/active",
    tags=["Employees"],
    response_model=List[schemas.EmployeeWithCountry],
    summary="Gets all active employees",
    response_description="A list containing all active employees",
    responses={404: {"model": None, "description": "No active employees found"}}
)
def get_active_employees(
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
    ):
    """Gets all active employees."""
    res = crud.get_employees(db)

    if not res:
        return Response(
            "No active employees found",
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )

    add_country_names(res)

    return res

@app.get(
    "/employees{department_name}",
    tags=["Employees"],
    response_model=List[schemas.EmployeeWithCountry],
    summary="Gets all employees in the given department",
    response_description="A list containing all employees in the department",
    responses={
        404: {"model": None, "description": "Employee not found in department"}
    }
)
def get_employees_by_department(
        department_name: str = Path(
            ...,
            title="Department name",
            description="Department name",
            max_length=50
        ),
        db:   Session = Depends(get_db),
        auth: bool    = Depends(is_authenticated)
    ):
    """
    Gets all employees by department:

    - **Department name**: name of the department
    """
    res = crud.get_job_employees_from_department(db, department_name)

    if not res:
        return Response(
            f"No employees in the department {department_name} or department" \
            " doesn't exist",
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )

    add_country_names(res)

    return res
