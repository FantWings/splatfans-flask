import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from email.mime.image import MIMEImage
# from email.mime.base import MIMEBase
# from email.mime.application import MIMEApplication
from email.header import Header
from flask import current_app


def sendmail(body, sendto, subject, sender, replyto=""):
    username = current_app.config.get("SMTP_USER")
    password = current_app.config.get("SMTP_PASS")
    host = current_app.config.get("SMTP_HOST")
    port = current_app.config.get("SMTP_PORT")

    # 构建alternative结构
    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header(subject).encode()
    msg["From"] = "%s <%s>" % (Header(sender).encode(), username)
    msg["To"] = sendto
    msg["Reply-to"] = replyto
    msg["Message-id"] = email.utils.make_msgid()
    msg["Date"] = email.utils.formatdate()

    # 构建alternative的text/html部分
    texthtml = MIMEText(body, _subtype="html", _charset="UTF-8")
    msg.attach(texthtml)

    # 发送邮件
    try:
        client = smtplib.SMTP_SSL(host=host)
        # SMTP普通端口为25或80
        client.connect(host, port)
        # 开启DEBUG模式
        client.set_debuglevel(0)
        client.login(username, password)
        # 发件人和认证地址必须一致
        # 备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
        #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
        client.sendmail(username, sendto, msg.as_string())
        client.quit()
        return "邮件发送成功！"
    except smtplib.SMTPConnectError as e:
        return ("邮件发送失败，连接失败:", e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        return ("邮件发送失败，认证错误:", e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        return ("邮件发送失败，发件人被拒绝:", e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        return ("邮件发送失败，收件人被拒绝:", e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        return ("邮件发送失败，数据接收拒绝:", e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        return ("邮件发送失败, ", e.message)
    except Exception as e:
        return ("邮件发送异常, ", str(e))
