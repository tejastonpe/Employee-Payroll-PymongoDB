from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    message:str
    status:int

class EmployeeAddSchema(BaseModel):
    name: str    
    age: int
    dept: str
    salary: int

class EmployeeResponceSchema(BaseResponseModel):
   data:EmployeeAddSchema