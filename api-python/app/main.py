from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@app.put("/users/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"ok": True}
