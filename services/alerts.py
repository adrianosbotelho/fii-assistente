import smtplib
import yaml
import os
from email.message import EmailMessage

def enviar_email(assunto, corpo):
    with open("config/email.yaml") as f:
        cfg = yaml.safe_load(f)

    msg = EmailMessage()
    msg["From"] = cfg["sender_email"]
    msg["To"] = cfg["receiver_email"]
    msg["Subject"] = assunto
    msg.set_content(corpo)

    server = smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"])
    server.starttls()
    server.login(cfg["sender_email"], os.getenv("EMAIL_PASSWORD"))
    server.send_message(msg)
    server.quit()
