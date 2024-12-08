import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime, timedelta, timezone
import jwt
from app import models, schemas, database


dotenv_path = Path('server/.env')
load_dotenv(dotenv_path=dotenv_path)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ALGORITHMJWT = os.getenv("ALGORITHMJWT")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()
#-------------------------------------------------------------------------------------------------------------------------------------------
# Vérifier le token
#-------------------------------------------------------------------------------------------------------------------------------------------

@router.post("/token", response_model = schemas.Token)
async def token(tokenData: schemas.tokenData, db: Session = Depends(get_db)):
    try :
        response = schemas.Token
        
        if verify_token(db, tokenData.token) : 
            response.status = 200
            response.access_token = tokenData.token
            response.token_type = ALGORITHM
            response.access_token_type = ALGORITHMJWT
            response.error_message = None
        else : 
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
         
def verify_token(db, token): 
        
    # on fait une reqete avec un filtre du token pour savoir si il existe en base
    encoded_jwt = db.query(models.User.token).filter(models.User.token == token).first()

    # si le token est stocker en base on passe dans la condition
    if encoded_jwt : 
        
        # c'est deux ligne permet de changer le type du token en bytes
        encoded_jwt = encoded_jwt.token
    
        encoded_jwt = encoded_jwt.encode('utf-8')

        #print(type(encoded_jwt),f"Token : {encoded_jwt}")
        
        #on décode le JWT avec la clé secret stocker dans le .env
        decode_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=ALGORITHMJWT)

        # on récuprer les différent donnée du JWt
        token_stocked = decode_jwt['token']
        date_expiration = decode_jwt['date_expiration']
        date_now = datetime.utcnow()
        # europe_paris = zoneinfo.ZoneInfo("Europe/Paris")
        # date_now_europe = date_now.astimezone(europe_paris)

        
        #print(decode_jwt['token'], decode_jwt['date_expiration'], decode_jwt['date_creation'], decode_jwt['role'])
        
        # on met la date d'expiration au bon format pour la comparé avec la date_now
        date_expiration = datetime.fromisoformat(date_now) if isinstance(date_now, str) else date_now

        if date_expiration > date_now : 
            
            #print(f"False : {date_expiration} , {date_now}")
            
            return False
        else : 
            
            #print(f"True : {date_expiration} , {date_now}")

            return True 
        
    return False

#-------------------------------------------------------------------------------------------------------------------------------------------
# Supprimer un token
#-------------------------------------------------------------------------------------------------------------------------------------------

@router.delete("/logout/{token}", response_model = schemas.Response)
async def delete_token(token: str, db: Session = Depends(get_db)):
    try:  
        response = schemas.Response
        
        db_token = db.query(models.User).filter(models.User.token == token).first()
            
        if db_token == None : 
            response.status = 403
            response.error_message = "Token doesn't exist"
        else : 
            response.status = 200
            response.error_message = None
            
            db_token.token = None
            db.commit()
        
        return response
    except RequestValidationError as e:
        #print(e)
        response.status = 422 
        response.error_message = str(e)
        return response
    except Exception as e:
        #print(e)
        response.status = 500 
        response.error_message = str(e)            
        return response