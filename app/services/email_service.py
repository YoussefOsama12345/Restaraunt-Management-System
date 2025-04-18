"""
Simple SSL Email Service.

Sends plain text or HTML emails using SMTP with SSL. 
Configured via environment variables.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))  # SSL only
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


def send_email(recipient: str, subject: str, body: str, html: bool = False) -> None:
    """
    Send an email over SSL.

    Args:
        recipient (str): Email to send to.
        subject (str): Email subject.
        body (str): Email body (HTML or plain).
        html (bool): Whether the body is HTML.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient

    mime_type = "html" if html else "plain"
    msg.attach(MIMEText(body, mime_type))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email failed: {str(e)}")
