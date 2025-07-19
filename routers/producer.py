from fastapi import APIRouter, HTTPException, status
from schemas.producer import ProducerInput, ProducerListResponse, ProducerOutput
from schemas.pagination import PaginationInput
from services.producer import create_producer, list_producers, update_producer, delete_producer, get_producer
from typing import List

router = APIRouter(tags=["producers"])

@router.post("/producers", status_code=status.HTTP_201_CREATED)
def post_producer(payload: ProducerInput):
    return create_producer(payload)


@router.post("/producers/list", response_model=ProducerListResponse)
def post_list_producers(pagination: PaginationInput):
    return list_producers(page=pagination.page, size=pagination.size)


@router.get("/producers/{producer_id}", response_model=ProducerOutput)
def get_producer_by_id(producer_id: int):
    producer = get_producer(producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer


@router.put("/producers/{producer_id}")
def put_producer(producer_id: int, payload: ProducerInput):
    return update_producer(producer_id, payload)


@router.delete("/producers/{producer_id}", status_code=status.HTTP_200_OK)
def delete_producer_route(producer_id: int):
    return delete_producer(producer_id)

