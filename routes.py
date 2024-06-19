from fastapi import FastAPI, HTTPException, Depends, Request
from pymongo import MongoClient
from schema import EmployeeAddSchema, EmployeeResponceSchema, BaseResponseModel

from db import Database, MongoDBMiddleware
from contextlib import asynccontextmanager

app = FastAPI()

db_name = "bridgelabz_training"
collection_name = "employees"
app.add_middleware(MongoDBMiddleware, database_name=db_name, collection_name=collection_name)

@asynccontextmanager
async def lifespan(app):
    try:
        Database.connect()
        yield
    finally:
        Database.disconnect()

@app.on_event("startup")
async def startup_event():
    Database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    Database.disconnect()

@app.post('/employees', response_model=EmployeeResponceSchema)
async def add_new_employee(emp: EmployeeAddSchema, request: Request):
    collection = request.state.db[db_name][collection_name]
    emp_data = emp.dict()
    created_emp = collection.insert_one(emp_data)
    emp_data["id"] = str(created_emp.inserted_id)
    return {"message": "Employee added successfully", "status": 201, "data": emp_data}

@app.get('/employees/{name}', response_model=EmployeeResponceSchema)
async def read_emp(name: str, request: Request):
    collection = request.state.db[db_name][collection_name]
    emp = collection.find_one({"name": name})
    if emp:
        return {"message": "Employee retrieved successfully", "status": 200, "data": emp}
    raise HTTPException(status_code=404, detail=f"Employee with name '{name}' not found")

@app.put('/employees/{name}', response_model=BaseResponseModel)
async def update_emp(name: str, emp: EmployeeAddSchema, request: Request):
    collection = request.state.db[db_name][collection_name]
    updated_emp = collection.find_one_and_update(
        {"name": name}, {"$set": emp.dict()}, return_document=True
    )
    if updated_emp:
        return {"message": "Employee updated successfully", "status": 200, "data": updated_emp}
    raise HTTPException(status_code=404, detail=f"Employee with name '{name}' not found")

@app.delete('/employees/{name}', response_model=BaseResponseModel)
async def delete_emp(name: str, request: Request):
    collection = request.state.db[db_name][collection_name]
    deleted_emp = collection.find_one_and_delete({"name": name})
    if deleted_emp:
        return {"message": "Employee deleted successfully", "status": 200}
    raise HTTPException(status_code=404, detail=f"Employee with name '{name}' not found")
