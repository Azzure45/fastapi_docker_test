from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

# Create tables on startup (idempotent; won't recreate if exists)
models.Base.metadata.create_all(bind=database.engine)

# Example route: Create a user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if user exists (basic example; add hashing in prod)
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # TODO: Hash this (e.g., with bcrypt)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Example route: Get a user by ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user