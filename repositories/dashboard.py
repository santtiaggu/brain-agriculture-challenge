from database.connection import get_connection

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

            # Uso do solo
            cur.execute("""
                SELECT 
                    COALESCE(SUM(agricultural_area), 0), 
                    COALESCE(SUM(vegetation_area), 0) 
                FROM farms;
            """)
            agri_area, veg_area = cur.fetchone()

            return {
                "total_farms": total_farms,
                "total_area": total_area,
                "by_state": by_state,
                "by_crop": by_crop,
                "land_use": {
                    "agricultural": float(agri_area),
                    "vegetation": float(veg_area)
                }
            }
