from schemas.producer import ProducerInput
from repositories.producer import save_producer, get_all_producers

def create_producer(data: ProducerInput):
    # Validação: soma das áreas
    for farm in data.farms:
        if farm.agricultural_area + farm.vegetation_area > farm.total_area:
            raise ValueError(f"A soma das áreas da fazenda '{farm.name}' excede a área total")

    # Salvar no banco
    save_producer(data)

    return {"message": "Producer created successfully"}


def list_producers(page: int, size: int):
    return get_all_producers(page=page, size=size)
