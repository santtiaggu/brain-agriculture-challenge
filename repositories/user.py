from database.connection import get_connection


async def get_user_by_email(email: str):
    conn = await get_connection()
    try:
        return await conn.fetchrow(
            "SELECT id, email, password, first_name, last_name, phone, admin, is_deleted FROM users WHERE email = $1",
            email
        )
    finally:
        await conn.close()
