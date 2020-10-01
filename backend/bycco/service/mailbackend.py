#    Copyright 2019 Chessdevil Consulting

import logging
import requests
import smtplib
import base64 
from markdown2 import Markdown
from io import BytesIO
from typing import List, Any
import os.path
from fastapi import HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.message import EmailMessage
from email.generator import BytesGenerator
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from bycco import settings

log = logging.getLogger('bycco')

bcc = 'ruben.decrop@bycco.be,luc.cornet@bycco.be'

class BaseEmailBackend:
    def send_message(self, message: MIMEBase):
        raise HTTPException(503, detail='EmailBackendNotImplemented')

class SmtpSslBackend(BaseEmailBackend):

    def send_message(self, msg: MIMEBase):
        with smtplib.SMTP_SSL(settings.EMAIL['host'], settings.EMAIL['port']) as s:
            if settings.EMAIL.get('user'):
                s.login(settings.EMAIL['user'], settings.EMAIL['password'])
            s.send_message(msg)

class SmtpBackend(BaseEmailBackend):

    def send_message(self, msg: MIMEBase):
        with smtplib.SMTP(settings.EMAIL['host'], settings.EMAIL['port']) as s:
            if settings.EMAIL.get('user'):
                s.login(settings.EMAIL['user'], settings.EMAIL['password'])
            s.send_message(msg)

class MailgunEmailBackend(BaseEmailBackend):

    def send_message(self, msg: MIMEBase):
        """
        sends a list of  email messages
        :param messages:
        :return: number of successfully sent messages
        """
        # TODO multiple TO, CC and BCC
        from email.generator import BytesGenerator
        url = settings.EMAIL_URL
        apikey = settings.EMAIL_APIKEY
        fp = BytesIO()
        g = BytesGenerator(fp)
        g.flatten(msg)
        rc = requests.post(url, auth=("api", apikey),
            data={'to': msg['To']},
            files={'message': fp}
        )
        return (rc.status_code, str(rc))

class GmailBackend(BaseEmailBackend):
    def send_message(self, msg: MIMEBase):
        service = get_gmail_service()
        rmsg = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode('ascii')}
        try:
            service.users().messages().send(userId='me', body=rmsg).execute()
        except Exception as e:
            log.exception('sending Gmail message failed')


def get_gmail_service():
    if not hasattr(get_gmail_service, 'service'):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                'credentials-gmail.json', 
                scopes=['https://www.googleapis.com/auth/gmail.send'])
            delegated_credentials = credentials.with_subject(settings.EMAIL['account']) 
            service = build('gmail', 'v1', credentials=delegated_credentials)        
            get_gmail_service.service = service
        except Exception:
            log.exception('Cannot setup Gmail API')
            raise HTTPException(503, detail='GmailAPINotAvailable')
    return get_gmail_service.service

backends = {
    'SMTP': SmtpBackend,
    'SMTP_SSL': SmtpSslBackend,
    'MAILGUN': MailgunEmailBackend,
    'GMAIL': GmailBackend,
}

