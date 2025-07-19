from fastapi import HTTPException
from fastapi.responses import JSONResponse
from schemas.producer import ProducerInput
from repositories.producer import save_producer, get_all_producers, update_producer_in_db, \
delete_producer_from_db, get_producer_by_id as fetch_producer_by_id

def create_producer(data: ProducerInput):
    # Validação: soma das áreas
    for farm in data.farms:
        if farm.agricultural_area + farm.vegetation_area > farm.total_area:
            raise HTTPException(
                status_code=422,
                detail=f"A soma das áreas da fazenda '{farm.name}' excede a área total"
            )

    # Salvar no banco
    save_producer(data)
    return JSONResponse(
        status_code=201,
        content={"message": "Producer created successfully"}
    )


def list_producers(page: int, size: int):
    return get_all_producers(page=page, size=size)


def get_producer(producer_id: int):
    return fetch_producer_by_id(producer_id)


def update_producer(producer_id: int, data):
    for farm in data.farms or []:
        if farm.agricultural_area + farm.vegetation_area > farm.total_area:
            raise HTTPException(
                status_code=422,
                detail=f"A soma das áreas da fazenda '{farm.name}' excede a área total de {farm.total_area} ha"
            )
        
    return update_producer_in_db(producer_id, data)


def delete_producer(producer_id: int):
    return delete_producer_from_db(producer_id)
