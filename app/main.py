from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import database

# Initialize the application
app = FastAPI(title="Employee Management Core API")

# Fix CORS - Added the missing comma here so the browser allows connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Trigger database initialization
database.init_db()

# Database dependency pipeline
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Cleaned up Pydantic validation structure
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, example="subramani")
    experience: int = Field(..., ge=0, example=2)
    department: str = Field(..., min_length=1, example="Engineering")
    salary: float = Field(..., ge=0, example=50000.0)

class EmployeeCreate(EmployeeBase):
    pass

# --- API ROUTES (CRUD) ---

# READ ALL
@app.get("/employees")
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(database.EmployeeDB).all()

# CREATE
@app.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_emp = database.EmployeeDB(
        name=employee.name,
        experience=employee.experience,
        department=employee.department,
        salary=employee.salary
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

# UPDATE
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, updated_data: EmployeeCreate, db: Session = Depends(get_db)):
    emp_record = db.query(database.EmployeeDB).filter(database.EmployeeDB.id == emp_id).first()
    if not emp_record:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    emp_record.name = updated_data.name
    emp_record.experience = updated_data.experience
    emp_record.department = updated_data.department
    emp_record.salary = updated_data.salary         
    db.commit()
    db.refresh(emp_record)
    return emp_record

# DELETE
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp_record = db.query(database.EmployeeDB).filter(database.EmployeeDB.id == emp_id).first()
    if not emp_record:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Fixed the indentation spacing here so it runs correctly inside the function context
    db.delete(emp_record)
    db.commit() 
    return {"message": "employee deleted"}