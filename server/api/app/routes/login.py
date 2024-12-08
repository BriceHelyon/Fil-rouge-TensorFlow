import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime, timedelta
import jwt
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
#Login
#-------------------------------------------------------------------------------------------------------------------------------------------

@router.post("/login", response_model = schemas.Token)
async def login(user: schemas.login, db: Session = Depends(get_db)):
    try:     
        response = schemas.Token
        # La fonction get_user_by_email permet de récupere dans la base de donnée le user avec la même adresse mail donnée la requete
        user_by_email = get_user_by_email(db, user.email)

    
        if user_by_email :
            if user.password == user_by_email.password :
                access_token = update_token_base(db, user_by_email)
                # access_token = create_access_token(int(user_by_email.role))
            
                response.status = 200
                response.access_token = access_token
                response.token_type = ALGORITHM
                response.access_token_type = ALGORITHMJWT
                response.error_message = None
            else : 
                response.status = 403 
                response.access_token = None
                response.token_type = None
                response.access_token_type = None
                response.error_message = None
        else:
            response.status = 403 
            response.access_token = None 
            response.token_type = None
            response.access_token_type = None
            response.error_message = None

                
        return response
    except RequestValidationError as e:
            #print(e)
            response.status = 422 
            response.access_token = None 
            response.token_type = None
            response.access_token_type = None
            response.error_message = str(e)
            return response
    except Exception as e:
            #print(e)
            response.status = 500 
            response.access_token = None 
            response.token_type = None
            response.access_token_type = None
            response.error_message = str(e)            
            return response

  
def get_user_by_email(db, email):
    response = db.query(models.User).filter(models.User.email == email).first()
    return response

def update_token_base(db, user):
    ### vérifier si l'utilisateur a déja un token si oui, vérififier si il est éxpiré ou renouvelé la date d'expiration
    encoded_jwt = user.token
    if encoded_jwt == None : 
        encoded_jwt = create_access_token(db, user)
    else :    
        decode_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=ALGORITHMJWT)
        token_stocked = decode_jwt['token']
        date_expiration = decode_jwt['date_expiration']
        date_now = datetime.utcnow()
    
        date_expiration = datetime.fromisoformat(date_expiration) if isinstance(date_expiration, str) else date_expiration
    
        if date_expiration > date_now : 
            encoded_jwt = create_access_token(db, user)
        else : 
            encoded_jwt = create_access_token(db, user, token_stocked)

    return encoded_jwt     

def create_access_token(db, user, token=None): 
    # 1 - un JWT avec token random, date expiration, date de création, rôle
    #-- crée un token random, 
    #-- le stocker en base de donnée et renvoie dans l'api
    if token == None : 
        token_random = random.getrandbits(128)
    else:
        token_random = token
        
    date_creation = datetime.utcnow()
    date_expiration = date_creation + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    header = {
        "algortihm": ALGORITHMJWT,
        "type": "JWT"
    }
    
    data = {
        "token": token_random,
        "date_expiration": date_expiration.isoformat(),
        "date_creation": date_creation.isoformat(),
        "role": user.role
    }
    
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHMJWT, headers=header)
    
    
    user.token = encoded_jwt
    db.commit()
    # TEST
    # decode_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHMJWT])
    # print(decode_jwt)
    
    return encoded_jwt


#-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------