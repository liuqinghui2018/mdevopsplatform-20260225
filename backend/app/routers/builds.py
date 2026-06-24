from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/builds", tags=["builds"])


@router.get("/", response_model=List[schemas.BuildOut])
def list_builds(db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    return db.query(models.Build).order_by(models.Build.id.desc()).all()


@router.post("/", response_model=schemas.BuildOut)
def create_build(build_in: schemas.BuildCreate, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    build = models.Build(**build_in.model_dump())
    db.add(build)
    db.commit()
    db.refresh(build)
    return build


@router.get("/{build_id}", response_model=schemas.BuildOut)
def get_build(build_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    build = db.query(models.Build).filter(models.Build.id == build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build
