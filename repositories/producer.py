from fastapi import HTTPException
from fastapi.responses import JSONResponse
from database.connection import get_connection
from schemas.producer import ProducerInput
from database.connection import get_connection

def save_producer(data: ProducerInput):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Inserir produtor
            cur.execute(
                """
                INSERT INTO producers (document, name)
                VALUES (%s, %s)
                RETURNING id
                """,
                (data.document, data.name)
            )
            producer_id = cur.fetchone()[0]

            for farm in data.farms:
                cur.execute(
                    """
                    INSERT INTO farms (producer_id, name, city, state, total_area, agricultural_area, vegetation_area)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        producer_id,
                        farm.name,
                        farm.city,
                        farm.state,
                        farm.total_area,
                        farm.agricultural_area,
                        farm.vegetation_area
                    )
                )
                farm_id = cur.fetchone()[0]

                for crop in farm.crops:
                    cur.execute(
                        """
                        INSERT INTO crops (farm_id, season, name)
                        VALUES (%s, %s, %s)
                        """,
                        (farm_id, crop.season, crop.name)
                    )
        conn.commit()


def get_all_producers(page: int, size: int):
    offset = (page - 1) * size

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Total de registros
            cur.execute("SELECT COUNT(*) FROM producers;")
            total = cur.fetchone()[0]

            # Dados paginados
            cur.execute("""
                SELECT id, name, document
                FROM producers
                ORDER BY id
                LIMIT %s OFFSET %s;
            """, (size, offset))

            producers = []
            for row in cur.fetchall():
                producer_id, name, document = row

                # Buscar fazendas associadas
                cur.execute("""
                    SELECT id, name, city, state, total_area, agricultural_area, vegetation_area
                    FROM farms
                    WHERE producer_id = %s;
                """, (producer_id,))
                farms = []
                for farm_row in cur.fetchall():
                    farm_id, farm_name, city, state, total_area, agri_area, veg_area = farm_row

                    # Buscar culturas da fazenda (com id agora)
                    cur.execute("""
                        SELECT id, season, name
                        FROM crops
                        WHERE farm_id = %s;
                    """, (farm_id,))
                    crops = [
                        {"id": crop_id, "season": season, "name": crop_name}
                        for crop_id, season, crop_name in cur.fetchall()
                    ]

                    farms.append({
                        "id": farm_id,
                        "name": farm_name,
                        "city": city,
                        "state": state,
                        "total_area": float(total_area),
                        "agricultural_area": float(agri_area),
                        "vegetation_area": float(veg_area),
                        "crops": crops
                    })

                producers.append({
                    "id": producer_id,
                    "name": name,
                    "document": document,
                    "farms": farms
                })

    return {
        "total": total,
        "page": page,
        "size": size,
        "producers": producers
    }


def get_producer_by_id(producer_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, document FROM producers WHERE id = %s
            """, (producer_id,))
            row = cur.fetchone()
            if not row:
                return None

            producer_id, name, document = row

            # Buscar fazendas
            cur.execute("""
                SELECT id, name, city, state, total_area, agricultural_area, vegetation_area
                FROM farms
                WHERE producer_id = %s
            """, (producer_id,))
            farms = []
            for farm_row in cur.fetchall():
                farm_id, fname, city, state, total_area, agri_area, veg_area = farm_row

                # Buscar culturas da fazenda
                cur.execute("""
                    SELECT id, season, name FROM crops WHERE farm_id = %s
                """, (farm_id,))
                crops = [
                    {"id": cid, "season": season, "name": crop_name}
                    for cid, season, crop_name in cur.fetchall()
                ]

                farms.append({
                    "id": farm_id,
                    "name": fname,
                    "city": city,
                    "state": state,
                    "total_area": float(total_area),
                    "agricultural_area": float(agri_area),
                    "vegetation_area": float(veg_area),
                    "crops": crops
                })

            return {
                "id": producer_id,
                "name": name,
                "document": document,
                "farms": farms
            }


def update_producer_in_db(producer_id: int, data: dict):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Verifica se o produtor existe antes de continuar
            cur.execute("SELECT 1 FROM producers WHERE id = %s", (producer_id,))
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Producer not found")

            # Atualizar nome e documento do produtor
            cur.execute("""
                UPDATE producers SET name = %s, document = %s WHERE id = %s;
            """, (data.name, data.document, producer_id))

            # Buscar todas as fazendas atuais
            cur.execute("SELECT id FROM farms WHERE producer_id = %s;", (producer_id,))
            existing_farm_ids = {row[0] for row in cur.fetchall()}
            received_farm_ids = {farm.id for farm in data.farms if farm.id is not None}

            # Deletar fazendas que não estão no payload
            farms_to_delete = existing_farm_ids - received_farm_ids
            if farms_to_delete:
                cur.execute("DELETE FROM crops WHERE farm_id = ANY(%s);", (list(farms_to_delete),))
                cur.execute("DELETE FROM farms WHERE id = ANY(%s);", (list(farms_to_delete),))

            for farm in data.farms:
                if farm.id and farm.id in existing_farm_ids:
                    # UPDATE farm existente
                    cur.execute("""
                        UPDATE farms SET name = %s, city = %s, state = %s,
                            total_area = %s, agricultural_area = %s, vegetation_area = %s
                        WHERE id = %s;
                    """, (
                        farm.name, farm.city, farm.state,
                        farm.total_area, farm.agricultural_area, farm.vegetation_area,
                        farm.id
                    ))

                    farm_id = farm.id

                    # Atualizar crops
                    cur.execute("SELECT id FROM crops WHERE farm_id = %s;", (farm_id,))
                    existing_crop_ids = {row[0] for row in cur.fetchall()}
                    received_crop_ids = {crop.id for crop in farm.crops if crop.id is not None}

                    crops_to_delete = existing_crop_ids - received_crop_ids
                    if crops_to_delete:
                        cur.execute("DELETE FROM crops WHERE id = ANY(%s);", (list(crops_to_delete),))

                    for crop in farm.crops:
                        if crop.id and crop.id in existing_crop_ids:
                            cur.execute("""
                                UPDATE crops SET season = %s, name = %s WHERE id = %s;
                            """, (crop.season, crop.name, crop.id))
                        else:
                            cur.execute("""
                                INSERT INTO crops (farm_id, season, name)
                                VALUES (%s, %s, %s);
                            """, (farm_id, crop.season, crop.name))

                else:
                    # Inserir nova farm
                    cur.execute("""
                        INSERT INTO farms (producer_id, name, city, state, total_area, agricultural_area, vegetation_area)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING id;
                    """, (
                        producer_id, farm.name, farm.city, farm.state,
                        farm.total_area, farm.agricultural_area, farm.vegetation_area
                    ))
                    farm_id = cur.fetchone()[0]

                    for crop in farm.crops:
                        cur.execute("""
                            INSERT INTO crops (farm_id, season, name)
                            VALUES (%s, %s, %s);
                        """, (farm_id, crop.season, crop.name))

            conn.commit()

    return JSONResponse(
        status_code=200,
        content={"message": "Producer updated successfully"}
    )


def delete_producer_from_db(producer_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Verifica se o produtor existe
            cur.execute("SELECT 1 FROM producers WHERE id = %s", (producer_id,))
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Producer not found")

            # Buscar farms do produtor
            cur.execute("SELECT id FROM farms WHERE producer_id = %s", (producer_id,))
            farm_ids = [row[0] for row in cur.fetchall()]

            # Deletar crops
            if farm_ids:
                cur.execute("DELETE FROM crops WHERE farm_id = ANY(%s);", (farm_ids,))
                cur.execute("DELETE FROM farms WHERE id = ANY(%s);", (farm_ids,))

            # Deletar producer
            cur.execute("DELETE FROM producers WHERE id = %s;", (producer_id,))
            conn.commit()

    return JSONResponse(
        status_code=200,
        content={"message": "Producer deleted successfully"}
    )
