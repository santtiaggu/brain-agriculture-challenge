from fastapi import HTTPException
from fastapi.responses import JSONResponse
from database.connection import get_connection
from schemas.producer import ProducerInput

async def save_producer(data: ProducerInput):
    conn = await get_connection()
    try:
        async with conn.transaction():
            row = await conn.fetchrow("""
                INSERT INTO producers (document, name)
                VALUES ($1, $2)
                RETURNING id;
            """, data.document, data.name)
            producer_id = row["id"]

            for farm in data.farms or []:
                row = await conn.fetchrow("""
                    INSERT INTO farms (producer_id, name, city, state, total_area, agricultural_area, vegetation_area)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    RETURNING id;
                """, producer_id, farm.name, farm.city, farm.state,
                     farm.total_area, farm.agricultural_area, farm.vegetation_area)
                farm_id = row["id"]

                for crop in farm.crops or []:
                    await conn.execute("""
                        INSERT INTO crops (farm_id, season, name)
                        VALUES ($1, $2, $3);
                    """, farm_id, crop.season, crop.name)
    finally:
        await conn.close()


async def get_all_producers(page: int, size: int):
    offset = (page - 1) * size
    conn = await get_connection()
    try:
        total_row = await conn.fetchrow("SELECT COUNT(*) FROM producers;")
        total = total_row["count"]

        rows = await conn.fetch("""
            SELECT id, name, document
            FROM producers
            ORDER BY id
            LIMIT $1 OFFSET $2;
        """, size, offset)

        producers = []
        for row in rows:
            producer_id = row["id"]
            name = row["name"]
            document = row["document"]

            farms_data = await conn.fetch("""
                SELECT id, name, city, state, total_area, agricultural_area, vegetation_area
                FROM farms
                WHERE producer_id = $1;
            """, producer_id)

            farms = []
            for farm in farms_data:
                farm_id = farm["id"]

                crops_data = await conn.fetch("""
                    SELECT id, season, name
                    FROM crops
                    WHERE farm_id = $1;
                """, farm_id)

                crops = [{"id": c["id"], "season": c["season"], "name": c["name"]} for c in crops_data]

                farms.append({
                    "id": farm_id,
                    "name": farm["name"],
                    "city": farm["city"],
                    "state": farm["state"],
                    "total_area": float(farm["total_area"]),
                    "agricultural_area": float(farm["agricultural_area"]),
                    "vegetation_area": float(farm["vegetation_area"]),
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
    finally:
        await conn.close()


async def get_producer_by_id(producer_id: int):
    conn = await get_connection()
    try:
        row = await conn.fetchrow("SELECT id, name, document FROM producers WHERE id = $1", producer_id)
        if not row:
            return None

        producer_id = row["id"]
        name = row["name"]
        document = row["document"]

        farms_data = await conn.fetch("""
            SELECT id, name, city, state, total_area, agricultural_area, vegetation_area
            FROM farms
            WHERE producer_id = $1;
        """, producer_id)

        farms = []
        for farm in farms_data:
            farm_id = farm["id"]
            crops_data = await conn.fetch("""
                SELECT id, season, name
                FROM crops
                WHERE farm_id = $1;
            """, farm_id)

            crops = [{"id": c["id"], "season": c["season"], "name": c["name"]} for c in crops_data]

            farms.append({
                "id": farm_id,
                "name": farm["name"],
                "city": farm["city"],
                "state": farm["state"],
                "total_area": float(farm["total_area"]),
                "agricultural_area": float(farm["agricultural_area"]),
                "vegetation_area": float(farm["vegetation_area"]),
                "crops": crops
            })

        return {
            "id": producer_id,
            "name": name,
            "document": document,
            "farms": farms
        }
    finally:
        await conn.close()


async def update_producer_in_db(producer_id: int, data: ProducerInput):
    conn = await get_connection()
    try:
        async with conn.transaction():
            exists = await conn.fetchval("SELECT 1 FROM producers WHERE id = $1", producer_id)
            if not exists:
                raise HTTPException(status_code=404, detail="Producer not found")

            await conn.execute("""
                UPDATE producers SET name = $1, document = $2 WHERE id = $3
            """, data.name, data.document, producer_id)

            # Fazendas existentes no banco
            existing_farms = await conn.fetch("SELECT id FROM farms WHERE producer_id = $1", producer_id)
            existing_farm_ids = {row["id"] for row in existing_farms}
            received_farm_ids = {farm.id for farm in data.farms or [] if farm.id is not None}

            farms_to_delete = list(existing_farm_ids - received_farm_ids)
            if farms_to_delete:
                await conn.execute("DELETE FROM crops WHERE farm_id = ANY($1)", farms_to_delete)
                await conn.execute("DELETE FROM farms WHERE id = ANY($1)", farms_to_delete)

            for farm in data.farms or []:
                if farm.id and farm.id in existing_farm_ids:
                    await conn.execute("""
                        UPDATE farms SET name = $1, city = $2, state = $3,
                            total_area = $4, agricultural_area = $5, vegetation_area = $6
                        WHERE id = $7
                    """, farm.name, farm.city, farm.state,
                         farm.total_area, farm.agricultural_area, farm.vegetation_area,
                         farm.id)

                    # Atualizar ou inserir culturas
                    farm_id = farm.id
                    existing_crops = await conn.fetch("SELECT id FROM crops WHERE farm_id = $1", farm_id)
                    existing_crop_ids = {row["id"] for row in existing_crops}
                    received_crop_ids = {crop.id for crop in farm.crops if crop.id is not None}

                    crops_to_delete = list(existing_crop_ids - received_crop_ids)
                    if crops_to_delete:
                        await conn.execute("DELETE FROM crops WHERE id = ANY($1)", crops_to_delete)

                    for crop in farm.crops:
                        if crop.id and crop.id in existing_crop_ids:
                            await conn.execute("""
                                UPDATE crops SET season = $1, name = $2 WHERE id = $3
                            """, crop.season, crop.name, crop.id)
                        else:
                            await conn.execute("""
                                INSERT INTO crops (farm_id, season, name)
                                VALUES ($1, $2, $3)
                            """, farm_id, crop.season, crop.name)

                else:
                    # Inserir nova fazenda
                    result = await conn.fetchrow("""
                        INSERT INTO farms (producer_id, name, city, state, total_area, agricultural_area, vegetation_area)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                        RETURNING id
                    """, producer_id, farm.name, farm.city, farm.state,
                         farm.total_area, farm.agricultural_area, farm.vegetation_area)
                    farm_id = result["id"]

                    for crop in farm.crops:
                        await conn.execute("""
                            INSERT INTO crops (farm_id, season, name)
                            VALUES ($1, $2, $3)
                        """, farm_id, crop.season, crop.name)

        return JSONResponse(status_code=200, content={"message": "Producer updated successfully"})
    finally:
        await conn.close()


async def delete_producer_from_db(producer_id: int):
    conn = await get_connection()
    try:
        async with conn.transaction():
            exists = await conn.fetchval("SELECT 1 FROM producers WHERE id = $1", producer_id)
            if not exists:
                raise HTTPException(status_code=404, detail="Producer not found")

            farm_ids = await conn.fetch("SELECT id FROM farms WHERE producer_id = $1", producer_id)
            farm_ids = [row["id"] for row in farm_ids]

            if farm_ids:
                await conn.execute("DELETE FROM crops WHERE farm_id = ANY($1)", farm_ids)
                await conn.execute("DELETE FROM farms WHERE id = ANY($1)", farm_ids)

            await conn.execute("DELETE FROM producers WHERE id = $1", producer_id)

        return JSONResponse(status_code=200, content={"message": "Producer deleted successfully"})
    finally:
        await conn.close()
