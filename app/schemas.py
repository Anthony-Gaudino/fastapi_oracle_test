from typing import List, Optional
from fastapi import Query

from pydantic import BaseModel

from datetime import date


class Badge(BaseModel):
    badge_number: int = Query(                                         
        ...,                                                                    
        title="Badge number",                                                    
        description="The employee badge number",                                 
        gt=0,
    )
    badge_status: Optional[str] = Query(
        None,
        title="Badge status",
        description="The employee badge status",
        max_length=10,
    )
    badge_expiry_date: Optional[date] = Query(
        None,
        title="Badge expiration date",
        description="The employee badge expiration date",
    )

    class Config:
        orm_mode = True

class Department(BaseModel):
    department_code: int = Query(                                         
        ...,                                                                    
        title="Department ID",                                                    
        description="The department ID",                                 
        gt=0,
    )
    department_name: Optional[str] = Query(
        None,
        title="Department name",
        description="The business department name",
        max_length=50,
    )

    class Config:
        orm_mode = True

class Employee(BaseModel):
    id: int = Query(                                         
        ...,                                                                    
        title="Employee ID",                                                    
        description="The employee ID",                                 
        gt=0,
    )
    firstname: Optional[str] = Query(
        None,
        title="Employee first name",
        description="The employee first name",
        max_length=100,
    )
    lastname: Optional[str] = Query(
        None,
        title="Employee last name",
        description="The employee last name",
        max_length=100,
    )
    country_code: Optional[str] = Query(
        None,
        title="Employee country code",
        description="The employee nationality country code",
        max_length=100,
    )
    job_title_code: Optional[int] = Query(
        ...,
        title="Job title FK",
        description="The job title FK",
        gt=0,
    )
    start_date: Optional[date] = Query(
        None,
        title="Employee start date",
        description="The date the employee was hired",
    )
    leave_date: Optional[date] = Query(
        None,
        title="Employee leave date",
        description="The date the employee left the job",
    )

    class Config:
        orm_mode = True

class EmployeeWithCountry(Employee):
    country_code: Optional[str] = Query(
        None,
        title="Employee country code",
        description="The employee nationality country code",
        max_length=256,
    )

class JobTitle(BaseModel):
    job_title_code: int = Query(                                         
        ...,                                                                    
        title="Job title ID",                                                    
        description="The job title ID",                                 
        gt=0,
    )
    job_title_name: Optional[str] = Query(
        None,
        title="Job title name",
        description="The job title name",
        max_length=50,
    )
    department_code: Optional[int] = Query(                                         
        None,                                                                    
        title="Department FK",                                                    
        description="The department FK",                                 
        gt=0,
    )

    class Config:
        orm_mode = True
