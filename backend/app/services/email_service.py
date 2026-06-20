import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from app.core.config import settings


class EmailConfigError(Exception):
    pass


def send_register_code_email(email: str, code: str) -> None:
    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password:
        raise EmailConfigError("smtp is not configured")

    message = EmailMessage()
    message["Subject"] = "CampusTree 注册验证码"
    message["From"] = formataddr((settings.smtp_from_name, settings.smtp_username))
    message["To"] = email
    message.set_content(
        "\n".join(
            [
                "你好，欢迎注册 CampusTree。",
                "",
                f"你的注册验证码是：{code}",
                "",
                f"验证码 {settings.email_code_expire_minutes} 分钟内有效。",
                "如果不是你本人操作，请忽略这封邮件。",
                "",
                "CampusTree 匿名校园树洞",
            ]
        )
    )

    if settings.smtp_port == 465:
        with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
        return

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)
