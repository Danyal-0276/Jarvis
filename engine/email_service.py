import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from engine.config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, MAX_EMAILS_PER_SESSION

_emails_sent = 0
_pending_email: dict | None = None


def get_pending_email() -> dict | None:
    return _pending_email


def clear_pending_email():
    global _pending_email
    _pending_email = None


def prepare_email(to: str, subject: str, body: str) -> dict:
    global _pending_email
    _pending_email = {"to": to, "subject": subject, "body": body}
    return {
        "status": "pending_confirmation",
        "preview": _pending_email,
        "message": f"Ready to send email to {to} with subject '{subject}'. Ask the user to confirm.",
    }


def send_email(to: str, subject: str, body: str, confirmed: bool = False) -> dict:
    global _emails_sent, _pending_email

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        return {"status": "error", "message": "Gmail credentials not configured in .env"}

    if _emails_sent >= MAX_EMAILS_PER_SESSION:
        return {"status": "error", "message": f"Email limit reached ({MAX_EMAILS_PER_SESSION} per session)."}

    if not confirmed:
        return prepare_email(to, subject, body)

    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        _emails_sent += 1
        _pending_email = None
        return {"status": "sent", "message": f"Email sent successfully to {to}."}
    except smtplib.SMTPAuthenticationError:
        return {
            "status": "error",
            "message": (
                "Gmail authentication failed. Use a Gmail App Password "
                "(not your regular password) at https://myaccount.google.com/apppasswords"
            ),
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to send email: {e}"}


def confirm_pending_email() -> dict:
    if not _pending_email:
        return {"status": "error", "message": "No pending email to confirm."}
    return send_email(
        _pending_email["to"],
        _pending_email["subject"],
        _pending_email["body"],
        confirmed=True,
    )
