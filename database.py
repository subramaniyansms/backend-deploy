from sqlalchemy import create_engine,Column,Integer,String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#database file
DATABASE_URL = "sqlite:///./employees.db"

#create database engine 
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
 
#create session 
SessionLocal = sessionmaker(autocommit=False, bind=engine)

#create base class
Base = declarative_base()

#define emloyee database model
class EmployeeDB(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    experience = Column(Integer, index=True)
    department = Column(String, index=True)
    salary = Column(Float, index=True)  

#helper function to create database tables
def init_db():
    Base.metadata.create_all(bind=engine)