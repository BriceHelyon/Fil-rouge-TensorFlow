from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..auth.auth import get_current_user  # Utilisation de l'authentification JWT
from app.database import get_db
from app import models, schemas

# Créer un routeur FastAPI
router = APIRouter()

@router.get("/interventions")
def get_interventions(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Route protégée qui nécessite un JWT valide pour accéder. 
    Elle récupère toutes les interventions de la base de données.
    """
    interventions = db.query(models.Interventions).all()

    return interventions

@router.get("/interventions/{id}")
def get_intervention(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Route protégée qui nécessite un JWT valide pour accéder. 
    Elle récupère une intervention spécifique par son ID.
    """
    # Vérifier que le token est valide (cette vérification est déjà effectuée par get_current_user)

    # Récupérer une intervention spécifique par ID
    intervention = db.query(models.Interventions).filter(models.Interventions.id == id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention non trouvée")

    return intervention



@router.post("/interventions")
def register_route(interventions: schemas.InterventionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):


    if current_user.get("role") != 1:  # Supposons que 1 est le rôle d'administrateur
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès interdit : seuls les administrateurs peuvent créer des utilisateurs."
        )


    # Créer une nouvelle instance de l'utilisateur
    new_intervention = models.Interventions(
        name= interventions.name,
        description= interventions.description,
        starting_date= interventions.starting_date,
        ending_date= interventions.ending_date,
        execution= interventions.execution,
        user_id= interventions.user_id,
        equipement_id= interventions.eq
    )

    # Ajouter le nouvel utilisateur à la base de données
    db.add(new_intervention)
    db.commit()
    db.refresh(new_intervention)

    # Retourner l'utilisateur nouvellement créé (sans le mot de passe)
    return new_intervention
