from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/environments", tags=["environments"])


@router.get("/", response_model=List[schemas.EnvironmentOut])
def list_environments(db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    return db.query(models.Environment).all()


@router.post("/", response_model=schemas.EnvironmentOut)
def create_environment(env_in: schemas.EnvironmentCreate, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    if db.query(models.Environment).filter(models.Environment.name == env_in.name).first():
        raise HTTPException(status_code=400, detail="Environment name already exists")
    env = models.Environment(**env_in.model_dump())
    db.add(env)
    db.commit()
    db.refresh(env)
    return env


@router.get("/{env_id}", response_model=schemas.EnvironmentOut)
def get_environment(env_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    env = db.query(models.Environment).filter(models.Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    return env


@router.put("/{env_id}", response_model=schemas.EnvironmentOut)
def update_environment(env_id: int, env_in: schemas.EnvironmentUpdate, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    env = db.query(models.Environment).filter(models.Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    for field, value in env_in.model_dump(exclude_unset=True).items():
        setattr(env, field, value)
    db.commit()
    db.refresh(env)
    return env


@router.delete("/{env_id}")
def delete_environment(env_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    env = db.query(models.Environment).filter(models.Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    db.delete(env)
    db.commit()
    return {"detail": "Deleted"}
