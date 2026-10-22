from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, Lugar

engine = create_engine("sqlite:///./santamarta.db", connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Recreate tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    lugares = db.query(Lugar).all()
    print("Lugares ORM:", lugares)
    for l in lugares:
        print(f"  {l.id}: {l.nombre}")
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
finally:
    db.close()