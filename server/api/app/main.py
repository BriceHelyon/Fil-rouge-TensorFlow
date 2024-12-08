from fastapi import APIRouter, FastAPI
from app.routes import login, register, interventions, token
from .database import engine
from .models import Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()


# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173"],  # Autorise cette origine spécifique
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les en-têtes
)

# if __name__ == "__main__":
#     uvicorn.run(
#         app, 
#         host="0.0.0.0",
#         port=8000,
#         ssl_certfile="cert.pem",
#         ssl_keyfile="key.pem"
#     )

# @app.exception_handler(Exception)
# async def cath_all_exceptions(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code = 500 ,
#         content={
#             "access_token": None,
#             "token_type": None,
#             "access_token_type": None,
#             "error_message": exc 
#         }
#     )

#Crée les tables de la base de données
# Base.metadata.create_all(bind=engine)

# en prod enlever le drop all
#Base.metadata.drop_all(bind = engine)
Base.metadata.create_all(bind=engine)

# Inclut les routes
app.include_router(login.router)

app.include_router(register.router)

app.include_router(token.router)

app.include_router(interventions.router)

# app.include_router(equipement.router)

