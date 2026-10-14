from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import urllib.request
import urllib.parse

app = FastAPI(title="Santa Marta Seguro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Lugar(BaseModel):
    id: Optional[int] = None
    nombre: str
    categoria: str = "playa"
    imagen: str = ""
    precio: int = 0
    seguridad: str = "verde"
    detalle: str = ""


lugares_db: List[dict] = [
    {
        "id": 1,
        "nombre": "Playa El Rodadero",
        "categoria": "playa",
        "imagen": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "precio": 0,
        "seguridad": "verde",
        "detalle": "Playa principal, ideal en familia. Precaucion de noche.",
    },
    {
        "id": 2,
        "nombre": "Taganga",
        "categoria": "playa",
        "imagen": "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=800&q=80",
        "precio": 20000,
        "seguridad": "amarillo",
        "detalle": "Pesca y buceo. Evitar zonas oscuras de noche.",
    },
    {
        "id": 3,
        "nombre": "Minca",
        "categoria": "naturaleza",
        "imagen": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=800&q=80",
        "precio": 30000,
        "seguridad": "verde",
        "detalle": "Cascadas y cafe. Llevar repelente y salir temprano.",
    },
    {
        "id": 4,
        "nombre": "Centro Historico",
        "categoria": "cultura",
        "imagen": "https://images.unsplash.com/photo-1568632234157-ce7aecd03d0d?auto=format&fit=crop&w=800&q=80",
        "precio": 0,
        "seguridad": "verde",
        "detalle": "Museos y gastronomia. Caminar de dia, taxi de noche.",
    },
    {
        "id": 5,
        "nombre": "Parque Tayrona",
        "categoria": "naturaleza",
        "imagen": "https://images.unsplash.com/photo-1502680390469-be75c86b636f?auto=format&fit=crop&w=800&q=80",
        "precio": 73000,
        "seguridad": "amarillo",
        "detalle": "Verificar acceso y clima antes de ir. Solo de dia.",
    },
    {
        "id": 6,
        "nombre": "Mercado Gastronomico",
        "categoria": "gastronomia",
        "imagen": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=80",
        "precio": 30000,
        "seguridad": "verde",
        "detalle": "Comida tipica desde $15.000. Preguntar precio antes.",
    },
]

alertas_db = [
    {"id": 1, "tipo": "clima", "titulo": "Lluvias en la tarde", "mensaje": "Se esperan lluvias. Considera actividades bajo techo."},
    {"id": 2, "tipo": "movilidad", "titulo": "Via a Minca", "mensaje": "Verifica condiciones de acceso antes de desplazarte."},
]

emergencias_db = [
    {"id": 1, "nombre": "Policia Nacional", "telefono": "123"},
    {"id": 2, "nombre": "Bomberos Santa Marta", "telefono": "119"},
    {"id": 3, "nombre": "Hospital Central", "telefono": "6054211111"},
]

# Coordenadas de cada lugar para el clima en vivo (Open-Meteo, gratis y sin clave)
lugares_clima = [
    {"nombre": "El Rodadero", "lat": 11.2033, "lon": -74.2365},
    {"nombre": "Taganga", "lat": 11.2676, "lon": -74.1898},
    {"nombre": "Minca", "lat": 11.1406, "lon": -74.1186},
    {"nombre": "Centro Historico", "lat": 11.2408, "lon": -74.2119},
    {"nombre": "Parque Tayrona", "lat": 11.2700, "lon": -74.0700},
]


def obtener_clima(lat: float, lon: float):
    params = urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "America/Bogota",
        "forecast_days": 1,
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "SantaMartaSeguro/1.0"})
    with urllib.request.urlopen(req, timeout=10) as res:
        return json.loads(res.read().decode("utf-8"))


def generar_alertas_clima():
    alertas = []
    for lugar in lugares_clima:
        try:
            clima = obtener_clima(lugar["lat"], lugar["lon"])
            actual = clima.get("current", {})
            diario = clima.get("daily", {})
            temp = actual.get("temperature_2m")
            viento = actual.get("wind_speed_10m", 0)
            prob_lluvia = (diario.get("precipitation_probability_max") or [0])[0]
            temp_max = (diario.get("temperature_2m_max") or [0])[0]

            if prob_lluvia is not None and prob_lluvia >= 60:
                alertas.append({
                    "id": 1000 + len(alertas),
                    "tipo": "clima",
                    "titulo": f"🌧️ Lluvia probable en {lugar['nombre']} ({prob_lluvia}%)",
                    "mensaje": f"Se esperan lluvias en {lugar['nombre']}. Considera actividades bajo techo.",
                })
            if temp_max is not None and temp_max >= 34:
                alertas.append({
                    "id": 1000 + len(alertas),
                    "tipo": "clima",
                    "titulo": f"☀️ Calor alto en {lugar['nombre']} ({round(temp_max)}°C)",
                    "mensaje": f"Buen momento para playa temprano, hidrátate y usa protector en {lugar['nombre']}.",
                })
            if viento is not None and viento >= 30:
                alertas.append({
                    "id": 1000 + len(alertas),
                    "tipo": "clima",
                    "titulo": f"💨 Viento fuerte en {lugar['nombre']} ({round(viento)} km/h)",
                    "mensaje": f"Precaución en mar y senderos en {lugar['nombre']}.",
                })
            if not any(a["titulo"].endswith(f"({lugar['nombre']})") or lugar["nombre"] in a["titulo"] for a in alertas):
                alertas.append({
                    "id": 1000 + len(alertas),
                    "tipo": "clima",
                    "titulo": f"☀️ Buen clima en {lugar['nombre']} ({round(temp) if temp is not None else '?'}°C)",
                    "mensaje": f"Buen momento para actividades al aire libre en {lugar['nombre']}.",
                })
        except Exception:
            continue
    return alertas


@app.get("/")
def root():
    return {"status": True, "servicio": "Santa Marta Seguro API"}


@app.get("/health")
def health():
    return {"status": True}


@app.get("/api/lugares")
def get_all_lugares():
    return {"status": True, "respuesta": lugares_db}


@app.post("/api/lugares")
def save_lugar(lugar: Lugar):
    nuevo_id = max([l["id"] for l in lugares_db], default=0) + 1
    data = lugar.dict()
    data["id"] = nuevo_id
    lugares_db.append(data)
    return {"status": True, "respuesta": data}


@app.get("/api/alertas")
def get_all_alertas():
    respuesta = list(alertas_db) + generar_alertas_clima()
    return {"status": True, "respuesta": respuesta}


@app.get("/api/clima")
def get_all_clima():
    respuesta = []
    for lugar in lugares_clima:
        try:
            clima = obtener_clima(lugar["lat"], lugar["lon"])
            respuesta.append({"lugar": lugar["nombre"], "clima": clima})
        except Exception as e:
            respuesta.append({"lugar": lugar["nombre"], "error": str(e)})
    return {"status": True, "respuesta": respuesta}


@app.get("/api/emergencias")
def get_all_emergencias():
    return {"status": True, "respuesta": emergencias_db}
