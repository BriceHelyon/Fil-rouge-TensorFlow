from fastapi import APIRouter, Depends, HTTPException, status
from ..auth.auth import get_current_user  # Utilisation d'un import relatif
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, database
import hashlib




# Créer un routeur FastAPI
router = APIRouter()

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')  # Convertir en bytes
    hash_object = hashlib.sha512(password_bytes)  # Hacher avec SHA-256
    return hash_object.hexdigest()  # Retourner le hash en format hexadécimal

@router.post("/register")
def register_route(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):


    if current_user.get("role") != 1:  # Supposons que 1 est le rôle d'administrateur
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès interdit : seuls les administrateurs peuvent créer des utilisateurs."
        )

    # Vérifier si l'utilisateur existe déjà dans la base de données
    user_in_db = db.query(models.User).filter(models.User.email == user.email).first()
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'utilisateur avec cet email existe déjà"
        )

    # Hacher le mot de passe
    hashed_password = hash_password(user.password)

    # Créer une nouvelle instance de l'utilisateur
    new_user = models.User(
        firstname= user.firstname,
        lastname=user.lastname,
        email=user.email,
        phone=user.phone,
        role=user.role,
        password=hashed_password
    )

    # Ajouter le nouvel utilisateur à la base de données
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Retourner l'utilisateur nouvellement créé (sans le mot de passe)
    return new_user
