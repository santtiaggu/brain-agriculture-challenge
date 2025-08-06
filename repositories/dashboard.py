import re
from database.connection import get_connection


async def get_dashboard_data():
    conn = await get_connection()
    try:
        async with conn.transaction():
            # Total de fazendas
            row = await conn.fetchrow("SELECT COUNT(*) FROM farms;")
            total_farms = row["count"]

            # Total de hectares (área total)
            row = await conn.fetchrow("SELECT COALESCE(SUM(total_area), 0) FROM farms;")
            total_area = float(row["coalesce"])

            # Fazendas por estado
            rows = await conn.fetch("""
                SELECT state, COUNT(*) 
                FROM farms 
                GROUP BY state;
            """)
            by_state = {row["state"]: row["count"] for row in rows}

            # Culturas por nome
            rows = await conn.fetch("""
                SELECT name, COUNT(*) 
                FROM crops 
                GROUP BY name;
            """)
            by_crop = {row["name"]: row["count"] for row in rows}

            # Culturas por safra e nome
            rows = await conn.fetch("""
                SELECT season, name, COUNT(*) 
                FROM crops 
                GROUP BY season, name;
            """)
            by_crop_season = {}
            for row in rows:
                season = row["season"]
                name = row["name"]
                count = row["count"]
                if season not in by_crop_season:
                    by_crop_season[season] = {}
                by_crop_season[season][name] = count

            # Uso do solo
            row = await conn.fetchrow("""
                SELECT 
                    COALESCE(SUM(agricultural_area), 0) AS agri,
                    COALESCE(SUM(vegetation_area), 0) AS veg
                FROM farms;
            """)
            agri_area = row["agri"]
            veg_area = row["veg"]

            # Tipo de documento (CPF/CNPJ)
            rows = await conn.fetch("SELECT document FROM producers;")
            by_document_type = {"CPF": 0, "CNPJ": 0}
            for row in rows:
                numeric = re.sub(r"\D", "", row["document"])
                if len(numeric) == 11:
                    by_document_type["CPF"] += 1
                elif len(numeric) == 14:
                    by_document_type["CNPJ"] += 1

            return {
                "total_farms": total_farms,
                "total_area": total_area,
                "by_state": by_state,
                "by_crop": by_crop,
                "by_crop_season": by_crop_season,
                "land_use": {
                    "agricultural": float(agri_area),
                    "vegetation": float(veg_area)
                },
                "by_document_type": by_document_type
            }

    finally:
        await conn.close()
