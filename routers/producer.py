from fastapi import APIRouter, HTTPException, status
from schemas.producer import ProducerInput
from services.producer import create_producer

router = APIRouter(prefix="/producers", tags=["producers"])

@router.post("", status_code=status.HTTP_201_CREATED)
def post_producer(payload: ProducerInput):
    return create_producer(payload)
