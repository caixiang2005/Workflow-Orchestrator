import redis
import os
import logging
logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# 测试连接
def test_redis_connection():
    """测试 Redis 连接是否成功"""
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError as e:
        logger.error(f"Redis 连接失败: {e}")
        return False

# 保存验证码到 Redis
def save_code(email: str, code:str, ex = 300):
    """
    email: 用户邮箱
    code: 验证码
    ex: 验证码过期时间，单位为秒，默认为300秒（5分钟）
    """
    try:
        redis_client.set(email, code, ex=ex)
        logger.info(f"正在保存验证码到 Redis: {email} -> {code}")
        return True
    except Exception as e:
        logger.error(f"保存验证码失败: {e}")
        return False

def get_code(email: str):
    "获取 Redis 中保存的验证码"
    try:
        code = redis_client.get(email)
        logger.info(f"正在从 Redis 获取验证码: {email} -> {code}")
        return code
    except Exception as e:
        logger.error(f"获取验证码失败: {e}")
        return None
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    # 加载环境变量
    load_dotenv()
    test_redis_connection()
