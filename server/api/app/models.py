# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, DateTime, Unicode
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String)
    firstname = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(Unicode(11))
    geographic_sector = Column(String) 
    role = Column(Integer)
    password = Column(String)
    token = Column(String)
    
    
class Equipements(Base) :
    __tablename__ = "equipements"
    
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String)
    starting_date = Column(DateTime)
    ending_date = Column(DateTime)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    
class Infrastructures(Base) : 
    __tablename__ = "infrastructures"
    
    id = Column(Integer, primary_key= True, index= True)   
    name = Column(String)
    localisation = Column(String)
    
class Maintenances(Base) : 
    __tablename__ = "maintenances"
    
    id = Column(Integer, primary_key= True, index= True)
    price = Column(Numeric(precision=10, scale=2))
    date_estimate = Column(DateTime)
    wear_rate = Column(Numeric(10,1))
    equipement_id = Column(Integer, ForeignKey('equipements.id'))
    
class Rooms(Base) : 
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String)
    infrastructure_id = Column(Integer, ForeignKey('infrastructures.id'))
    
class Interventions(Base) : 
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String)
    description = Column(String)
    starting_date = Column(DateTime)
    ending_date = Column(DateTime)
    execution = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    equipement_id = Column(Integer, ForeignKey('equipements.id'))


    