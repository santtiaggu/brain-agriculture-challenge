from schemas.producer import ProducerInput
from repositories.producer import save_producer

def create_producer(data: ProducerInput):
    # Validação: soma das áreas
    for farm in data.farms:
        if farm.agricultural_area + farm.vegetation_area > farm.total_area:
            raise ValueError(f"A soma das áreas da fazenda '{farm.name}' excede a área total")

    # Salvar no banco
    save_producer(data)

    return {"message": "Producer created successfully"}
