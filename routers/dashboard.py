from fastapi import APIRouter, Depends
from services.dashboard import dashboard_summary
from utils.security import get_current_user

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    return await dashboard_summary()
