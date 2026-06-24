from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="developer")  # admin, developer, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    repository_url = Column(String, nullable=True)
    language = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pipelines = relationship("Pipeline", back_populates="service")
    deployments = relationship("Deployment", back_populates="service")


class Environment(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    deployments = relationship("Deployment", back_populates="environment")


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    trigger = Column(String, default="push")  # push, pr, manual, schedule
    status = Column(String, default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow)

    service = relationship("Service", back_populates="pipelines")
    builds = relationship("Build", back_populates="pipeline")


class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=False)
    commit_sha = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, running, success, failed
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    logs = Column(Text, nullable=True)

    pipeline = relationship("Pipeline", back_populates="builds")
    deployments = relationship("Deployment", back_populates="build")


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    environment_id = Column(Integer, ForeignKey("environments.id"), nullable=False)
    status = Column(String, default="pending")  # pending, running, success, failed, rolled_back
    deployed_by = Column(String, nullable=True)
    deployed_at = Column(DateTime, default=datetime.utcnow)
    version = Column(String, nullable=True)

    build = relationship("Build", back_populates="deployments")
    service = relationship("Service", back_populates="deployments")
    environment = relationship("Environment", back_populates="deployments")
