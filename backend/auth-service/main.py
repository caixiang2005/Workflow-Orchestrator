from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import random
import os
from send_mail import send_qq_email, load_email_template
from dotenv import load_dotenv  
from logging_config import setup_logging
import logging
from redis_client import save_code, get_code, test_redis_connection
from fastapi import HTTPException
from redis import ConnectionError
from contextlib import asynccontextmanager
from db import init_db_pool, close_db_pool, get_user_by_email

@asynccontextmanager
async def lifespan(app:FastAPI):
    # 启动时
    await init_db_pool()
    yield
    # 关闭时
    await close_db_pool()

# 配置日志
setup_logging()
logger = logging.getLogger(__name__)

# 加载配置文件
load_dotenv()
app = FastAPI(lifespan=lifespan)

# 临时存储邮箱和验证码的字典(redis)
temp_email_storage = {}

# 定义请求体模型
class SendCodeRequest(BaseModel):
    email: EmailStr

@app.post("/api/v1/auth/send-code")
async def send_code(req: SendCodeRequest) -> dict:
    """
    发送验证码到指定邮箱
    """
    to_email = req.email

    # 测试数据库连接状态
    try:
        if not test_redis_connection():
            raise ConnectionError("Redis 未连接")
    except Exception as e:
        raise HTTPException(status_code=500, detail="验证码服务不可用，请稍后再试")



    # 验证码还有效
    if get_code(to_email):
        return {"message": f"验证码已发送到邮箱{to_email}，请勿重复请求", "code": 400}
    
    
    subject = "【incx】邮箱登陆验证"
    body = ''


    # 这里根据数据库内查询结果判断是否需要发送验证码邮件 
    user = await get_user_by_email(to_email)

    # 从环境变量获取logo URL并加载模板
    logo_url = os.getenv('LOGO_URL')
 
    if user:
        try:
            # 生成6位随机验证码
            code = str(random.randint(100000, 999999))

            if test_redis_connection():
                save_code(to_email, code)

        except Exception as e:
            logger.error(f"保存验证码失败: {e}")
            raise HTTPException(status_code=500, detail="验证码服务不可用，请稍后再试")

        # 构建验证码邮件内容
        body = load_email_template('verify_code_email.html', logo_url=logo_url, code=code)
    else:
        register_url = os.getenv("REGISTER_URL")

        # 没有记录发送注册模版
        body = load_email_template('register_email.html', logo_url=logo_url, register_url=register_url)
        

    success = send_qq_email(to_email, subject, body)
    
    if success:
        return {"message": f"验证码已发送到邮箱{to_email}", "code": 200}
    else:
        return {"message": "验证码发送失败，请稍后重试", "code": 500}