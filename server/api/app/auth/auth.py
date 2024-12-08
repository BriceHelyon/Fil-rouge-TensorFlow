import os
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

# Charger les variables d'environnement
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHMJWT = os.getenv("ALGORITHMJWT")

# Utiliser OAuth2PasswordBearer pour récupérer le token depuis l'en-tête de la requête
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str):
    """Vérifier et décoder un token JWT."""
    try:
        # Décoder le token avec le secret et l'algorithme définis
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMJWT])

        # Vérifier manuellement la date d'expiration à partir du champ "date_expiration"
        exp_date = payload.get("date_expiration")
        if exp_date:
            exp_datetime = datetime.fromisoformat(exp_date)
            if datetime.utcnow() > exp_datetime:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Vérifier si le token dans le JWT est dans la base

        return payload  # Si le token est valide, retourner le payload décodé

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtenir l'utilisateur courant à partir du token JWT."""
    return verify_token(token)