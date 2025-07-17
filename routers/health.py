
"""Health routes implementation."""
from fastapi import APIRouter
from schemas.health import HealthOutput

router = APIRouter(tags=['health'])


@router.get(
    '',
    response_model=HealthOutput
)
async def health():
    """Health check."""
    return {'status': 'ok'}
