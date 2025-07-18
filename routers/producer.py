from fastapi import APIRouter, HTTPException, status
from schemas.producer import ProducerInput, ProducerListResponse
from schemas.pagination import PaginationInput
from services.producer import create_producer, list_producers, update_producer
from typing import List

router = APIRouter(tags=["producers"])

@router.post("/producers", status_code=status.HTTP_201_CREATED)
def post_producer(payload: ProducerInput):
    return create_producer(payload)


@router.post("/producers/list", response_model=ProducerListResponse)
def post_list_producers(pagination: PaginationInput):
    return list_producers(page=pagination.page, size=pagination.size)


@router.put("/producers/{producer_id}")
def put_producer(producer_id: int, payload: ProducerInput):
    return update_producer(producer_id, payload)

