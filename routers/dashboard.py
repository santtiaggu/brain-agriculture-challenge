from fastapi import APIRouter
from services.dashboard import dashboard_summary

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard")
async def get_dashboard():
    return await dashboard_summary()
