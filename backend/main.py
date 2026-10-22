from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import init_db
from routes import lugares_router, alertas_router, emergencias_router, admin_router
from seed import seed_database

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(lugares_router)
app.include_router(alertas_router)
app.include_router(emergencias_router)
app.include_router(admin_router)

# Inicializar DB al arrancar
@app.on_event("startup")
def startup_event():
    init_db()
    seed_database()

@app.get("/")
def root():
    return {"status": True, "servicio": "Santa Marta Seguro API"}

@app.get("/health")
def health():
    return {"status": True}