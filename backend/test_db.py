from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./santamarta.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
try:
    result = db.execute(text("SELECT * FROM lugares"))
    rows = result.fetchall()
    print("Rows:", rows)
    for row in rows:
        print(row)
except Exception as e:
    print("Error:", e)
finally:
    db.close()