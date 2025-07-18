from fastapi import APIRouter
from services.dashboard import dashboard_summary

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard")
def get_dashboard():
    return dashboard_summary()
