from database.connection import get_connection
import re

def get_dashboard_data():
    with get_connection() as conn:
        with conn.cursor() as cur:

            # Total de fazendas
            cur.execute("SELECT COUNT(*) FROM farms;")
            total_farms = cur.fetchone()[0]

            # Total de hectares (área total)
            cur.execute("SELECT COALESCE(SUM(total_area), 0) FROM farms;")
            total_area = float(cur.fetchone()[0])

            # Fazendas por estado
            cur.execute("""
                SELECT state, COUNT(*) 
                FROM farms 
                GROUP BY state;
            """)
            by_state = {state: count for state, count in cur.fetchall()}

            # Culturas por nome
            cur.execute("""
                SELECT name, COUNT(*) 
                FROM crops 
                GROUP BY name;
            """)
            by_crop = {name: count for name, count in cur.fetchall()}

            # Culturas por safra
            cur.execute("""
                SELECT season, name, COUNT(*) 
                FROM crops 
                GROUP BY season, name;
            """)
            by_crop_season_raw = cur.fetchall()
            by_crop_season = {}
            for season, name, count in by_crop_season_raw:
                if season not in by_crop_season:
                    by_crop_season[season] = {}
                by_crop_season[season][name] = count

            # Uso do solo
            cur.execute("""
                SELECT 
                    COALESCE(SUM(agricultural_area), 0), 
                    COALESCE(SUM(vegetation_area), 0) 
                FROM farms;
            """)
            agri_area, veg_area = cur.fetchone()

            # Tipo de documento (CPF ou CNPJ)
            cur.execute("SELECT document FROM producers;")
            docs = cur.fetchall()
            by_document_type = {"CPF": 0, "CNPJ": 0}
            for (doc,) in docs:
                # CPF tem 11 dígitos, CNPJ tem 14
                numeric = re.sub(r"\D", "", doc)
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
