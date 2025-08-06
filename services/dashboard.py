from repositories.dashboard import get_dashboard_data

async def dashboard_summary():
    return await get_dashboard_data()
