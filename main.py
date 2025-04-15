from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Producto

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
