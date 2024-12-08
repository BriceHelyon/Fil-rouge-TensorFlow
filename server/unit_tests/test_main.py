import os
import bcrypt  # type: ignore
import pytest  # type: ignore
from fastapi.testclient import TestClient  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from unittest.mock import patch, MagicMock

from main import app
from database import get_db
from models import User

testClient = TestClient(app)

# Simulation d'un utilisateur en base de donnée
def override_get_db():
    
    database = MagicMock(spec=Session)
    
    try:
    
        yield database
   
    finally:

        database.close()

app.dependency_overrides [get_db] = override_get_db

# Creer un utilisateur simule
mock_user_data = {
    "email": "testuser@example.com", # Ecrire une vraie adresse-mail
    "password": bcrypt.hashpw(b"password", bcrypt.gensalt()).decode('utf-8'),  # Hash le MDP
    "role": 1,
    "token": None
}

#Reprend les donnes de l'utilisateur simule
@pytest.fixture
def mock_user() :
    
    mock_user_test = User(**mock_user_data)
    
    return mock_user_test

# Test une connexion reussie en appelant les fonctions
@patch("server.api.app.routers.auth.get_user_by_email")
@patch("server.api.app.routers.auth.update_token_base")
def test_login_success (mock_get_user_by_email, 
                        mock_update_token_base, 
                        mock_user) :
    
    mock_get_user_by_email.return_value = mock_user
    
    mock_update_token_base.return_value = "test_access_token"

    # Simule une requete de connexion valide
    login_data = {
        "email": mock_user_data ["email"],
        "password": "password"  # Ecrire un vrai utilisateur
    }

    # Envoi une requete POST au endoint login 
    response = testClient.post ("/login", 
                                json = login_data)

    # Verifie la reponse de l'API (200 valide)
    assert response.status_code == 200
    
    # Affiche le contenu de la reponse JSON (200 valide)
    json_response = response.json ()
    
    assert json_response ["status"] == 200
    assert json_response ["access_token"] == "test_access_token"
    assert json_response ["token_type"] == os.getenv("ALGORITHM")
    assert json_response ["access_token_type"] == os.getenv("ALGORITHMJWT")
    assert json_response ["error_message"] is None

# Test une connexion incorrect en appelant les fonctions
@patch("server.api.app.routers.auth.get_user_by_email")
def test_login_incorrect_password (mock_get_user_by_email, 
                                   mock_user) :
    
    mock_get_user_by_email.return_value = mock_user

    # Simule une requete de connexion invalide
    login_data = {
        "email": mock_user_data ["email"],
        "password": "wrongpassword" # Ecrire un faux MDP
    }

    # Envoi une requete POST au endoint login 
    response = testClient.post("/login", 
                               json = login_data)

    # Verifie la reponse de l'API (200 valide)
    assert response.status_code == 200
    
    # Affiche le contenu de la reponse JSON (erreur 403)
    json_response = response.json ()
    
    assert json_response ["status"] == 403
    assert json_response ["access_token"] is None
    assert json_response ["token_type"] is None
    assert json_response ["access_token_type"] is None
    assert json_response ["error_message"] is None

# Test pour un utilisateur introuvable en appelant les fonctions
@patch("server.api.app.routers.auth.get_user_by_email")
def test_login_user_not_found (mock_get_user_by_email) :
    
    mock_get_user_by_email.return_value = None

    # Simule une requete de connexion invalide
    login_data = {
        "email": "nonexistentuser@example.com",
        "password": "somepassword" # Ecrire un faux utilisateur
    }

    # Envoi une requete POST au endoint login 
    response = testClient.post ("/login", 
                                json = login_data)

    # Verifie la reponse de l'API (200 valide)
    assert response.status_code == 200
    
    # Affiche le contenu de la reponse JSON (erreur 403)
    json_response = response.json ()
    
    assert json_response ["status"] == 403
    assert json_response ["access_token"] is None
    assert json_response ["token_type"] is None
    assert json_response ["access_token_type"] is None
    assert json_response ["error_message"] is None