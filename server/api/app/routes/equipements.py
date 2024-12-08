import os 
from dotenv import load_dotenv
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime, timedelta
from app import models, schemas, database
import hashlib
import random

dotenv_path = Path('server/.env')
load_dotenv(dotenv_path=dotenv_path)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ALGORITHMJWT = os.getenv("ALGORITHMJWT")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()

#-------------------------------------------------------------------------------------------------------------------------------------------
#   get all
#-------------------------------------------------------------------------------------------------------------------------------------------

@router.get("/equipements/", response_model=list[schemas.EquipementCreate])
async def get_all_equipements(equipements: models.Equipements, db: Session = Depends(get_db)):
    equipements = db.query(equipements).all()
    return {"equipements": [equipements.__dict__ for equipement in equipements]}


#-------------------------------------------------------------------------------------------------------------------------------------------
#   get by id
#-------------------------------------------------------------------------------------------------------------------------------------------

@router.get("/equipement/{equipement_id}", response_model = schemas.EquipementCreate)
async def get_equipement_by_id(equipement_id: int, equipement: models.Equipements, db: Session = Depends(get_db)):
    equipement = db.query(equipement).filter(models.Equipements.id == equipement_id).first()
    # equipement = db.query(models.Equipements).filter(models.Equipements.id == equipement_id).first()
    return equipement


#-------------------------------------------------------------------------------------------------------------------------------------------
#   create
#-------------------------------------------------------------------------------------------------------------------------------------------

@router.post("/equipement/", response_model = schemas.EquipementCreate)
async def create_equipement(equipement: schemas.EquipementCreate, db: Session = Depends(get_db)):
    #db_equipement = models.Equipement(email=user.email, hashed_password=fake_hashed_password)
    db.add(equipement)
    if db.commit() : 
        return True
    return False
    

#-------------------------------------------------------------------------------------------------------------------------------------------
#   update
#-------------------------------------------------------------------------------------------------------------------------------------------

@router.put("/equipement/{equipement_id}", response_model = schemas.EquipementCreate)
async def update_equipement(equipement_id: int, equipement: schemas.EquipementCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        return {"message": "Item not found"}
    item.name = name
    item.price = price
    db.commit()
    return {"message": "Item updated successfully"}

#-------------------------------------------------------------------------------------------------------------------------------------------
#   delete
#-------------------------------------------------------------------------------------------------------------------------------------------

@router.delete("/equipement/{equipement_id}", response_model = schemas.EquipementCreate)
async def delete_equipement(equipement_id: int) : 
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        return {"message": "Item not found"}
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}