from fastapi import APIRouter, HTTPException, status
from schemas.producer import ProducerInput, ProducerListResponse
from schemas.pagination import PaginationInput
from services.producer import create_producer, list_producers
from typing import List

router = APIRouter(tags=["producers"])

@router.post("/producer", status_code=status.HTTP_201_CREATED)
def post_producer(payload: ProducerInput):
    return create_producer(payload)

@router.post("/producers/list", response_model=ProducerListResponse)
def post_list_producers(pagination: PaginationInput):
    return list_producers(page=pagination.page, size=pagination.size)
