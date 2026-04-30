import asyncio
import asyncpg
import os

async def test_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", 5432))
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "postgres")

    print(f"正在测试数据库连接: {host}:{port} 用户: {user} 数据库: {database}")
    try:
        # 建立连接
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("数据库连接成功")
        
        version = await conn.fetchval("select version();")
        print(f"数据库版本: {version}")

        now = await conn.fetchval("select now();")
        print(f"当前数据库时间: {now}")

        await conn.close()
        print("数据库连接已关闭")
    except Exception as e:
        print(f"数据库连接失败: {e}")
        
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    asyncio.run(test_connection())