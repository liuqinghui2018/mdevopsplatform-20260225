from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("/", response_model=List[schemas.ServiceOut])
def list_services(db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    return db.query(models.Service).all()


@router.post("/", response_model=schemas.ServiceOut)
def create_service(service_in: schemas.ServiceCreate, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    if db.query(models.Service).filter(models.Service.name == service_in.name).first():
        raise HTTPException(status_code=400, detail="Service name already exists")
    service = models.Service(**service_in.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.get("/{service_id}", response_model=schemas.ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.put("/{service_id}", response_model=schemas.ServiceOut)
def update_service(service_id: int, service_in: schemas.ServiceUpdate, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    for field, value in service_in.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service


@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    return {"detail": "Deleted"}
