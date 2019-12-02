# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger('talistro_election')

import requests
import smtplib
import dataclasses
import qrcode
from io import BytesIO
from typing import List, Any

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from .. import config
from ..models import ElectionEventModel, MemberModel, PhoneModel
from ..util.handler import ApiBaseHandler

bcc = 'ruben.bycco@gmail.com'

class BaseEmailBackend:
    def send_message(self, message: EmailMessage):
        return (400, 'NotImplemented')

class SmtpSslBackend(BaseEmailBackend):

    def send_message(self, msg: EmailMessage):
        with smtplib.SMTP_SSL(config.EMAIL_HOST, config.EMAIL_PORT) as s:
            if hasattr(config, "EMAIL_USER"):
                s.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            s.send_message(msg)

class SmtpBackend(BaseEmailBackend):

    def send_message(self, msg: EmailMessage):
        with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as s:
            if hasattr(config, "EMAIL_USER"):
                s.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            s.send_message(msg)
    
class MailgunEmailBackend(BaseEmailBackend):

    def send_message(self, msg: EmailMessage):
        """
        sends a list of  email messages
        :param messages:
        :return: number of successfully sent messages
        """
        # TODO multiple TO, CC and BCC
        from email.generator import BytesGenerator
        url = config.EMAIL_URL
        apikey = config.EMAIL_APIKEY
        fp = BytesIO()
        g = BytesGenerator(fp)
        g.flatten(msg)
        rc = requests.post(url, auth=("api", apikey),
            data={'to': msg['To']},
            files={'message': fp}
        )
        return (rc.status_code, str(rc))

backends = {
    'SMTP': SmtpBackend,
    'SMTP_SSL': SmtpSslBackend,
    'MAILGUN': MailgunEmailBackend,
}

