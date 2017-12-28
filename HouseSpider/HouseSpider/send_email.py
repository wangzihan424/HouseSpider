# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
HOST = "smtp.163.com"


def send_file_email(where, what, file_name, subject, to="694936968@qq.com"):
    SUBJECT = subject
    TO = to
    msg = MIMEMultipart('related')
    msgtext = MIMEText(what,
                       "html",
                       "utf-8")
    msg.attach(msgtext)
    attach = MIMEText(open(file_name, "rb").read(), "base64", "utf-8")
    attach["Content-Type"] = "application/octet-stream"
    attach["Content-Disposition"] = "attachment; filename=\""+file_name+"\"".decode("utf-8").encode("gb18030")
    msg.attach(attach)
    msg['Subject'] = subject
    msg['From'] = where
    msg['To'] = to
    try:
        server = smtplib.SMTP()
        server.connect(HOST, "25")
        server.starttls()
        server.login("zhang864071694@163.com", "zhangzenan520")
        server.sendmail(where, to, msg.as_string())
        server.quit()
        print "邮件发送成功！"
    except Exception, e:
        print "失败：" + str(e)

