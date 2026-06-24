from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/deployments", tags=["deployments"])


@router.get("/", response_model=List[schemas.DeploymentOut])
def list_deployments(db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    return db.query(models.Deployment).order_by(models.Deployment.id.desc()).all()


@router.post("/", response_model=schemas.DeploymentOut)
def create_deployment(dep_in: schemas.DeploymentCreate, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    deployment = models.Deployment(**dep_in.model_dump())
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment


@router.get("/{deployment_id}", response_model=schemas.DeploymentOut)
def get_deployment(deployment_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    deployment = db.query(models.Deployment).filter(models.Deployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment


@router.post("/{deployment_id}/rollback", response_model=schemas.DeploymentOut)
def rollback_deployment(deployment_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    deployment = db.query(models.Deployment).filter(models.Deployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    deployment.status = "rolled_back"
    deployment.deployed_at = datetime.utcnow()
    db.commit()
    db.refresh(deployment)
    return deployment
