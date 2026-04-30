import asyncpg
import os
import logging
logger = logging.getLogger(__name__)

from typing import Optional

# 数据库连接池
pool: Optional[asyncpg.Pool] = None

async def init_db_pool():
    """
    初始化数据库连接池
    """
    global pool

    # 加载配置文件
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", 5432))
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "postgres")

    try:
        pool = await asyncpg.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            min_size=1,
            max_size=10,
            command_timeout=60,
            max_queries=50000,  # 限制每个连接的最大查询次数
            max_inactive_connection_lifetime=300    # 限制连接存活时间
        )

        async with pool.acquire() as conn:
            await conn.execute("SELECT 1")
        logger.info(f"数据库连接池已初始化: {host}:{port} 用户: {user} 数据库: {database}")
        return pool
    except Exception as e:
        logger.error(f"数据库连接池初始化失败: {e}")
        raise e

async def close_db_pool():
    """
    关闭数据库连接池
    """
    global pool
    if pool:
        await pool.close()
        logger.info("数据库连接池已关闭")

async def get_user_by_email(email: str):
    """"
    根据邮箱查询用户
    """
    if pool is None:
        raise RuntimeError("数据库连接池未初始化")
    async with pool.acquire() as conn:
        row = await conn.fetchrow("select id,email,username,created_at,updated_at from users where email = $1",email)
    
    if row:
        logger.debug(f"查询到用户:{row['id']}")
    else:
        logger.debug(f"未找到用户")
    return dict(row) if row else None