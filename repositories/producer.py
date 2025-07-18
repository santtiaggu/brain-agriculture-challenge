from database.connection import get_connection
from schemas.producer import ProducerInput

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
