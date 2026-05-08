import redis
import os
import secrets

import logging
logger = logging.getLogger(__name__)

pool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
    max_connections=20
)
redis_client = redis.Redis(connection_pool=pool)


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
        key = f"code:{email}"
        redis_client.set(key, code, ex=ex)
        logger.info(f"正在保存验证码到 Redis: {email} -> {code}")
        return True
    except Exception as e:
        logger.error(f"保存验证码失败: {e}")
        return False

def get_code(email: str):
    "获取 Redis 中保存的验证码"
    try:
        key = f"code:{email}"
        code = redis_client.get(key)
        logger.info(f"正在从 Redis 获取验证码: {email} -> {code}")
        return code
    except Exception as e:
        logger.error(f"获取验证码失败: {e}")
        return None

# 设置注册冷却时间
def set_reg_cooldown(email: str, ex = 600):
    """设置注册冷却时间"""
    try:
        key = f"reg_cooldown:{email}"
        redis_client.set(key, "1", ex = ex)
        logger.info(f"正在设置注册冷却时间: {email}")
    except Exception as e:
        logger.error(f"设置注册冷却时间失败: {e}")

# 确认是否在注册冷却时间内
def is_in_reg_cooldown(email: str):
    """确认是否在注册冷却时间内"""
    try:
        key = f"reg_cooldown:{email}"
        return redis_client.exists(key) == 1
    except Exception as e:
        logger.error(f"检查注册冷却时间失败: {e}")
        return False

# 生成安全token
def generate_register_token():
    """生成安全的注册链接token"""
    return secrets.token_urlsafe(32)

def save_register_token(email: str, token: str, ex = 86400):
    """保存注册链接token到 Redis，默认过期时间为1小时"""
    try:
        key = f"reg_token:{email}"
        redis_client.set(key, token, ex=ex)
        logger.info(f"正在保存注册链接token到 Redis: {email} -> {token}")
        return True
    except Exception as e:
        logger.error(f"保存注册链接token失败: {e}")
        return False

if __name__ == "__main__":
    from dotenv import load_dotenv
    # 加载环境变量
    load_dotenv()
    test_redis_connection()
    set_reg_cooldown('test@example.com')
    print(is_in_reg_cooldown('test@example.com'))
    print(generate_register_token())
    save_register_token('test@example.com', generate_register_token())