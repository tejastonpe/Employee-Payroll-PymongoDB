from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from schema import EmployeeAddSchema,EmployeeResponceSchema,BaseResponseModel

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.client = MongoClient("mongodb://localhost:27017")
    app.database = app.client["bridgelabz_training"]
    app.employee_collection = app.database["employees"]

@app.on_event("shutdown")
def shutdown_db_client():
    app.client.close()

@app.post('/employees',response_model=EmployeeResponceSchema)
def add_new_employee(emp: EmployeeAddSchema):
    emp_data = emp.dict()
    created_emp = app.employee_collection.insert_one(emp_data)
    emp_data["id"] = str(created_emp.inserted_id)
    return {"message":"Employeee added sucessfully","status":201,"data":emp_data}

@app.get('/employees/{name}',response_model=EmployeeResponceSchema)
def read_emp(name:str):
    emp = app.employee_collection.find_one({"name":name})
    if emp:
        return {"message":"Employeee retrived sucessfully","status":201,"data":emp}
    raise HTTPException(status_code=404, detail=f"Employee with name '{name}' not found")

@app.put('/employees/{name}',response_model=BaseResponseModel)
def update_emp(name:str, emp:EmployeeAddSchema):
    updated_emp = app.employee_collection.find_one_and_update({"name":name},{"$set":emp.dict()})
    if updated_emp:
        return {f"message":"Employeee updated sucessfully","status":201,"data":updated_emp}
    raise HTTPException(status_code=404, detail=f"Employee not found")

@app.delete('/employee/{name}',response_model=BaseResponseModel)
def delete_emp(name:str):
    delted_emp = app.employee_collection.find_one_and_delete({"name":name})
    if delted_emp:
        return {f"message":"Employeee data deleted sucessfully","status":201}
    raise HTTPException(status_code=404, detail=f"Employee not found")