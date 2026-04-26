import smtplib
from email.mime.text import MIMEText
from email.header import make_header
import os
from dotenv import load_dotenv  


load_dotenv()

def load_email_template(filename: str, **kwargs) -> str:
    """
    读取HTML邮件模板
    :param filename: 模板文件名
    :param kwargs: 模板中需要替换的变量
    :return: HTML模板内容
    """
    template_path = os.path.join(os.path.dirname(__file__), 'templates', filename)
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换模板中的变量
    for key, value in kwargs.items():
        placeholder = '{' + key + '}'
        content = content.replace(placeholder, str(value))
    
    return content

def send_qq_email(to_email: str, subject: str, body: str) -> bool:
    """
    通过 QQ 邮箱 SMTP 发送邮件
    :param to_email: 收件人邮箱
    :param subject:  邮件主题
    :param body:     邮件正文
    :param code:     验证码
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    from_email = os.getenv("SMTP_SENDER")
    auth_code = os.getenv("SMTP_AUTH_CODE")

    # 构建邮件
    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = str(make_header([(subject, "utf-8")]))
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        # 建立 SSL 连接并登录
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_email, auth_code)
        # 发送邮件
        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()
        print(f"邮件发送成功至 {to_email}")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False