import imaplib
import email
from email.header import decode_header
import re

# 配置信息（使用你自己的邮箱）
IMAP_SERVER = 'imap.qq.com'
PORT = 993
USERNAME = '2179451926@qq.com'          # ← 改成你的邮箱


auth_file = r'C:/Users\ASUS\Desktop\Workflow-Orchestrator\data\sqm.txt'
with open(auth_file, 'r', encoding='utf-8') as f:
    PASSWORD = f.read().strip()
print(PASSWORD)

def fetch_verification_code():
    mail = None
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, PORT)
        mail.login(USERNAME, PASSWORD)
        print("✅ 登录成功")

        mail.select('INBOX')
        # 搜索未读邮件，可根据需要增加发件人过滤，例如只读来自 2243421676@qq.com 的邮件
        result, data = mail.search(None, 'UNSEEN')
        if result != 'OK' or not data[0]:
            print("📭 没有未读邮件")
            return

        email_ids = data[0].split()
        print(f"📬 找到 {len(email_ids)} 封未读邮件")

        # 获取最新的一封
        latest_id = email_ids[-1]
        result, msg_data = mail.fetch(latest_id, '(RFC822)')
        if result != 'OK':
            print("❌ 获取邮件失败")
            return

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # 解码主题
        subject_raw = decode_header(msg.get('Subject'))[0]
        subject = subject_raw[0] if isinstance(subject_raw[0], str) else subject_raw[0].decode(subject_raw[1] or 'utf-8')
        print(f"📧 主题: {subject}")

        # 提取正文
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

        print(f"📝 正文:\n{body}")

        # 提取6位数字验证码
        match = re.search(r'\b(\d{6})\b', body)
        if match:
            code = match.group(1)
            print(f"🔑 验证码: {code}")
            return code
        else:
            print("⚠️ 未找到6位数字验证码")
            return None

    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP 错误: {e}")
        print("可能原因：授权码错误、未开启IMAP服务、账号异常")
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        if mail:
            try:
                mail.logout()
            except:
                pass

if __name__ == '__main__':
    fetch_verification_code()