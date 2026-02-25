import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from . import models
from .auth import get_password_hash
from .routers import users, services, environments, pipelines, builds, deployments

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(users.users_router)
app.include_router(services.router)
app.include_router(environments.router)
app.include_router(pipelines.router)
app.include_router(builds.router)
app.include_router(deployments.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_active_user
from . import schemas


@app.get("/api/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    total_pipelines = db.query(models.Pipeline).count()
    total_builds = db.query(models.Build).count()
    successful_deployments = db.query(models.Deployment).filter(models.Deployment.status == "success").count()
    failed_builds = db.query(models.Build).filter(models.Build.status == "failed").count()
    recent_builds = db.query(models.Build).order_by(models.Build.id.desc()).limit(5).all()
    recent_deployments = db.query(models.Deployment).order_by(models.Deployment.id.desc()).limit(5).all()
    return {
        "total_pipelines": total_pipelines,
        "total_builds": total_builds,
        "successful_deployments": successful_deployments,
        "failed_builds": failed_builds,
        "recent_builds": recent_builds,
        "recent_deployments": recent_deployments,
    }


def seed_data():
    db = SessionLocal()
    try:
        # Seed admin user
        if not db.query(models.User).first():
            admin = models.User(
                username="admin",
                email="admin@devops.local",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_active=True,
            )
            db.add(admin)
            developer = models.User(
                username="developer",
                email="developer@devops.local",
                hashed_password=get_password_hash("dev123"),
                role="developer",
                is_active=True,
            )
            db.add(developer)
            db.commit()

        # Seed environments
        if not db.query(models.Environment).first():
            for env_name, desc in [("dev", "Development environment"), ("staging", "Staging environment"), ("prod", "Production environment")]:
                db.add(models.Environment(name=env_name, description=desc))
            db.commit()

        # Seed services
        if not db.query(models.Service).first():
            services_data = [
                {"name": "api-gateway", "description": "API Gateway service", "repository_url": "https://github.com/org/api-gateway", "language": "Go", "owner": "platform-team"},
                {"name": "user-service", "description": "User management microservice", "repository_url": "https://github.com/org/user-service", "language": "Python", "owner": "backend-team"},
                {"name": "frontend-app", "description": "React frontend application", "repository_url": "https://github.com/org/frontend-app", "language": "TypeScript", "owner": "frontend-team"},
                {"name": "notification-service", "description": "Email and push notification service", "repository_url": "https://github.com/org/notification-service", "language": "Node.js", "owner": "backend-team"},
            ]
            for s in services_data:
                db.add(models.Service(**s))
            db.commit()

        # Seed pipelines
        if not db.query(models.Pipeline).first():
            service_ids = [s.id for s in db.query(models.Service).all()]
            pipelines_data = [
                {"name": "api-gateway-ci", "service_id": service_ids[0], "trigger": "push", "status": "active"},
                {"name": "user-service-ci", "service_id": service_ids[1], "trigger": "push", "status": "active"},
                {"name": "frontend-deploy", "service_id": service_ids[2], "trigger": "pr", "status": "active"},
                {"name": "notification-ci", "service_id": service_ids[3], "trigger": "schedule", "status": "inactive"},
            ]
            for p in pipelines_data:
                db.add(models.Pipeline(**p))
            db.commit()

        # Seed builds
        if not db.query(models.Build).first():
            pipeline_ids = [p.id for p in db.query(models.Pipeline).all()]
            builds_data = [
                {"pipeline_id": pipeline_ids[0], "commit_sha": "abc1234", "branch": "main", "status": "success", "started_at": datetime(2025, 1, 10, 9, 0), "finished_at": datetime(2025, 1, 10, 9, 5), "logs": "Build started\nRunning tests...\nAll tests passed\nBuild successful"},
                {"pipeline_id": pipeline_ids[1], "commit_sha": "def5678", "branch": "main", "status": "failed", "started_at": datetime(2025, 1, 10, 10, 0), "finished_at": datetime(2025, 1, 10, 10, 3), "logs": "Build started\nRunning tests...\nTest failed: UserAuthTest\nBuild failed"},
                {"pipeline_id": pipeline_ids[2], "commit_sha": "ghi9012", "branch": "feature/dashboard", "status": "success", "started_at": datetime(2025, 1, 11, 8, 0), "finished_at": datetime(2025, 1, 11, 8, 8), "logs": "Build started\nInstalling deps\nBuild successful"},
                {"pipeline_id": pipeline_ids[0], "commit_sha": "jkl3456", "branch": "main", "status": "running", "started_at": datetime(2025, 1, 12, 9, 0), "finished_at": None, "logs": "Build started\nRunning tests..."},
                {"pipeline_id": pipeline_ids[3], "commit_sha": "mno7890", "branch": "main", "status": "success", "started_at": datetime(2025, 1, 9, 7, 0), "finished_at": datetime(2025, 1, 9, 7, 4), "logs": "Build completed successfully"},
            ]
            for b in builds_data:
                db.add(models.Build(**b))
            db.commit()

        # Seed deployments
        if not db.query(models.Deployment).first():
            builds = db.query(models.Build).filter(models.Build.status == "success").all()
            envs = db.query(models.Environment).all()
            env_map = {e.name: e.id for e in envs}
            services = db.query(models.Service).all()

            if builds and envs:
                deployments_data = [
                    {"build_id": builds[0].id, "service_id": services[0].id, "environment_id": env_map["prod"], "status": "success", "deployed_by": "admin", "version": "v1.2.0", "deployed_at": datetime(2025, 1, 10, 10, 0)},
                    {"build_id": builds[1].id, "service_id": services[1].id, "environment_id": env_map["staging"], "status": "failed", "deployed_by": "developer", "version": "v2.1.0", "deployed_at": datetime(2025, 1, 10, 11, 0)},
                    {"build_id": builds[2].id, "service_id": services[2].id, "environment_id": env_map["dev"], "status": "success", "deployed_by": "admin", "version": "v0.9.1", "deployed_at": datetime(2025, 1, 11, 9, 0)},
                    {"build_id": builds[0].id, "service_id": services[0].id, "environment_id": env_map["staging"], "status": "success", "deployed_by": "admin", "version": "v1.1.9", "deployed_at": datetime(2025, 1, 9, 12, 0)},
                ]
                for d in deployments_data:
                    db.add(models.Deployment(**d))
                db.commit()
    finally:
        db.close()


# Run seed on startup
seed_data()
