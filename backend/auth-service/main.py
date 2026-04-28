from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import random
import os
from send_mail import send_qq_email, load_email_template
from dotenv import load_dotenv  

# 加载配置文件
load_dotenv()
app = FastAPI()

# 临时存储邮箱和验证码的字典(redis)
temp_email_storage = {}

# 定义请求体模型
class SendCodeRequest(BaseModel):
    email: EmailStr

@app.post("/api/v1/auth/send-code")
def send_code(req: SendCodeRequest) -> dict:
    """
    发送验证码到指定邮箱
    """
    to_email = req.email
    code = str(random.randint(100000, 999999))
    
    temp_email_storage[to_email] = code

    subject = "【incx】邮箱登陆验证"
    body = ''

    # 根据不同的邮件类型构建邮件内容
    body_type = 'verify_cod'  

    # 这里根据数据库内查询结果判断是否需要发送验证码邮件 

    # 从环境变量获取logo URL并加载模板
    logo_url = os.getenv('LOGO_URL')
    
    if body_type == 'verify_code':
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