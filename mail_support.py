import os
import traceback
import sys

import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class __EmailClient:

    def __init__(self):
        self.smtp_address = os.getenv("SMTP_ADDRESS")

        self.email = os.getenv("EMAIL")
        self.email_from = os.getenv("EMAIL_FROM")
        self.email_to = os.getenv("EMAIL_TO")
        self.email_pw = os.getenv("EMAIL_PW")


__client = __EmailClient()


def __get_traceback_msg(exc_type, exc_error, exc_tb):
    lines = traceback.format_exception(exc_type, exc_error, exc_tb)
    full_traceback_text = ''.join(lines)

    return full_traceback_text


def send_error(subject_error):
    exc_error = sys.exc_info()[1]
    if exc_error is None:
        html_content = f"""
                        <h4>Human Verification after login.</h4>
                        <p>Action required!</p>

                        <h6>This is an automated message.</h6>
                        """
    else:
        exc_type = type(exc_error)
        exc_tb = exc_error.__traceback__

        traceback_msg = __get_traceback_msg(exc_type, exc_error, exc_tb)
        print(traceback_msg)

        html_content = f"""
                <h4>An unexpected error has occurred!</h4>

                <code>
                    {traceback_msg}
                </code>    

                <h6>This is an automated message.</h6>
                """

    msg = EmailMessage()
    msg["Subject"] = f"[ERR] - {subject_error}"
    msg["From"] = __client.email_from
    msg["To"] = __client.email_to
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(__client.smtp_address) as server:
        server.starttls()
        server.login(__client.email, __client.email_pw)
        server.send_message(msg)


def send_passed(login_streak):
    msg = EmailMessage()
    msg["Subject"] = f"[INFO] - Logged into stackoverflow.com"
    msg["From"] = __client.email_from
    msg["To"] = __client.email_to
    print(__client.email, __client.email_from, __client.email_to, __client.smtp_address)
    print("Logged into stackoverflow.com and accessed profile page.")

    html_content = f"""
            <h4>Successfully logged into stackoverflow.com and accessed profile page!</h4>
            <p>You have now {login_streak} consecutive logins!   
            
            <h6>This is an automated message.</h6>
            """
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(__client.smtp_address) as server:
        server.starttls()
        server.login(__client.email, __client.email_pw)
        server.send_message(msg)
