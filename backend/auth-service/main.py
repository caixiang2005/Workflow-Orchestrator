from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import random
app = FastAPI()


# 临时邮箱存储：{email:code}
temp_email_storage = {}

class SendCodeRequest(BaseModel):
    email: EmailStr

# 发生验证码请求的接口
@app.post("/api/v1/auth/send-code")
def send_code(req: SendCodeRequest) -> dict:
    email = req.email
    # 生产随机的六位验证码
    code = str(random.randint(100000, 999999))

    # 存储验证码到临时邮箱存储中
    temp_email_storage[email] = code

    # 发送验证码

    return {"message": f"验证码{code}已发送到邮箱{email}"}