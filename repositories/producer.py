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

