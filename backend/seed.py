from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Lugar, Emergencia
from auth import get_admin_password_hash

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Lugar).count() > 0:
            print("Base de datos ya tiene datos, omitiendo seed")
            return
        
        # Lugares iniciales
        lugares = [
            Lugar(
                nombre="Playa El Rodadero",
                categoria="playa",
                imagen="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
                precio=0,
                seguridad="verde",
                detalle="Playa principal, ideal en familia. Precaución de noche."
            ),
            Lugar(
                nombre="Taganga",
                categoria="playa",
                imagen="https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=800&q=80",
                precio=20000,
                seguridad="amarillo",
                detalle="Pesca y buceo. Evitar zonas oscuras de noche."
            ),
            Lugar(
                nombre="Minca",
                categoria="naturaleza",
                imagen="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=800&q=80",
                precio=30000,
                seguridad="verde",
                detalle="Cascadas y café. Llevar repelente y salir temprano."
            ),
            Lugar(
                nombre="Centro Histórico",
                categoria="cultura",
                imagen="https://images.unsplash.com/photo-1568632234157-ce7aecd03d0d?auto=format&fit=crop&w=800&q=80",
                precio=0,
                seguridad="verde",
                detalle="Museos y gastronomía. Caminar de día, taxi de noche."
            ),
            Lugar(
                nombre="Parque Tayrona",
                categoria="naturaleza",
                imagen="https://images.unsplash.com/photo-1502680390469-be75c86b636f?auto=format&fit=crop&w=800&q=80",
                precio=73000,
                seguridad="amarillo",
                detalle="Verificar acceso y clima antes de ir. Solo de día."
            ),
            Lugar(
                nombre="Mercado Gastronómico",
                categoria="gastronomia",
                imagen="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=80",
                precio=30000,
                seguridad="verde",
                detalle="Comida típica desde $15.000. Preguntar precio antes."
            ),
        ]
        
        for lugar in lugares:
            db.add(lugar)
        
        # Emergencias iniciales
        emergencias = [
            Emergencia(nombre="Policía Nacional", telefono="123"),
            Emergencia(nombre="Bomberos Santa Marta", telefono="119"),
            Emergencia(nombre="Hospital Central", telefono="6054211111"),
        ]
        
        for emergencia in emergencias:
            db.add(emergencia)
        
        db.commit()
        print("Base de datos inicializada con datos de prueba")
        
    except Exception as e:
        db.rollback()
        print(f"Error al inicializar base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()