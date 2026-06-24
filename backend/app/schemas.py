from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ---- User ----
class UserBase(BaseModel):
    username: str
    email: str
    role: Optional[str] = "developer"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Auth ----
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ---- Service ----
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    repository_url: Optional[str] = None
    language: Optional[str] = None
    owner: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    language: Optional[str] = None
    owner: Optional[str] = None


class ServiceOut(ServiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Environment ----
class EnvironmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class EnvironmentCreate(EnvironmentBase):
    pass


class EnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class EnvironmentOut(EnvironmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Pipeline ----
class PipelineBase(BaseModel):
    name: str
    service_id: int
    trigger: Optional[str] = "push"
    status: Optional[str] = "active"


class PipelineCreate(PipelineBase):
    pass


class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    trigger: Optional[str] = None
    status: Optional[str] = None


class PipelineOut(PipelineBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Build ----
class BuildBase(BaseModel):
    pipeline_id: int
    commit_sha: Optional[str] = None
    branch: Optional[str] = None
    status: Optional[str] = "pending"
    logs: Optional[str] = None


class BuildCreate(BuildBase):
    pass


class BuildOut(BuildBase):
    id: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---- Deployment ----
class DeploymentBase(BaseModel):
    build_id: int
    service_id: int
    environment_id: int
    status: Optional[str] = "pending"
    deployed_by: Optional[str] = None
    version: Optional[str] = None


class DeploymentCreate(DeploymentBase):
    pass


class DeploymentOut(DeploymentBase):
    id: int
    deployed_at: datetime

    class Config:
        from_attributes = True


# ---- Dashboard ----
class DashboardStats(BaseModel):
    total_pipelines: int
    total_builds: int
    successful_deployments: int
    failed_builds: int
    recent_builds: List[BuildOut]
    recent_deployments: List[DeploymentOut]
