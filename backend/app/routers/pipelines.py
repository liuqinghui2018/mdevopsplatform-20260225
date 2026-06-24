from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/pipelines", tags=["pipelines"])


@router.get("/", response_model=List[schemas.PipelineOut])
def list_pipelines(db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    return db.query(models.Pipeline).all()


@router.post("/", response_model=schemas.PipelineOut)
def create_pipeline(pipeline_in: schemas.PipelineCreate, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    pipeline = models.Pipeline(**pipeline_in.model_dump())
    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)
    return pipeline


@router.get("/{pipeline_id}", response_model=schemas.PipelineOut)
def get_pipeline(pipeline_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    pipeline = db.query(models.Pipeline).filter(models.Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@router.put("/{pipeline_id}", response_model=schemas.PipelineOut)
def update_pipeline(pipeline_id: int, pipeline_in: schemas.PipelineUpdate, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    pipeline = db.query(models.Pipeline).filter(models.Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    for field, value in pipeline_in.model_dump(exclude_unset=True).items():
        setattr(pipeline, field, value)
    db.commit()
    db.refresh(pipeline)
    return pipeline


@router.delete("/{pipeline_id}")
def delete_pipeline(pipeline_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_active_user)):
    pipeline = db.query(models.Pipeline).filter(models.Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    db.delete(pipeline)
    db.commit()
    return {"detail": "Deleted"}


@router.post("/{pipeline_id}/trigger", response_model=schemas.BuildOut)
def trigger_pipeline(pipeline_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    pipeline = db.query(models.Pipeline).filter(models.Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    build = models.Build(
        pipeline_id=pipeline_id,
        branch="main",
        commit_sha="manual-trigger",
        status="running",
        started_at=datetime.utcnow(),
        logs=f"Pipeline triggered manually by {current_user.username}\nRunning...\nBuild completed successfully.",
    )
    db.add(build)
    db.commit()
    # mark finished
    build.status = "success"
    build.finished_at = datetime.utcnow()
    db.commit()
    db.refresh(build)
    return build
