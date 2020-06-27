"""uses asyncio.create_subprocess_exec to call sendmail"""
import asyncio
from email.mime.text import MIMEText
import logging
import os
import re

logger = logging.getLogger(__name__)
SENDMAIL = "/usr/sbin/sendmail"


async def sendmail(message_body: str, recipients: list, subject: str, from_email: str, bcc=None):
    """use asyncio to call sendmail"""
    if not isinstance(recipients, list):
        recipients = [recipients]
    message = MIMEText(message_body)
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = "; ".join(recipients)
    if bcc:
        if not isinstance(bcc, list):
            bcc = [bcc]
        message['Bcc'] = "; ".join(bcc)


    message_string = message.as_string()
    logger.info("sending %s to %s", message_string, message["To"])
    proc = await asyncio.create_subprocess_exec(
        SENDMAIL,
        "-t",
        "-i",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate(message_string.encode())
    if stderr:
        logger.error('sendmail status: "%s"', stderr.decode())

    if stdout:
        logger.error('sendmail status: "%s"', stdout.decode())
