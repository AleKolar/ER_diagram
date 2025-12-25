import asyncio
import asyncpg

async def test_connection():
    try:
        conn = await asyncpg.connect(
            user='postgres',
            password='password',
            database='er_db',
            host='localhost',
            port=5432
        )
        print("✅ Подключение к PostgreSQL успешно!")
        await conn.close()
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())