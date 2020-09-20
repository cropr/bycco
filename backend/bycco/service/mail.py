# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from markdown2 import Markdown
from io import BytesIO
from typing import List, Any
import os.path
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from bycco import settings
from bycco.models.md_subscription import SubscriptionDetailedOut
from bycco.i18n import locale_msg
from .mailbackend import backends

log = logging.getLogger('bycco')
md = Markdown()

def test_mail():
    """
    send a test mail
    """
    try:
        sender = settings.EMAIL['sender']
        receiver = 'ruben.decrop@gmail.com'
        msg = MIMEMultipart('related')
        msg['Subject'] = 'Testmail 2'
        msg['From'] = sender
        msg['To'] = receiver
        if settings.EMAIL.get('bcc'):
            msg['Bcc'] = settings.EMAIL['bcc']
        msg.preamble = 'This is a multi-part message in MIME format.'
        msgAlternative = MIMEMultipart('alternative')
        msgText = MIMEText("Hi it is I Leclercq, I am in disguise")
        msgAlternative.attach(msgText)
        msgText = MIMEText("Hi, It is I <b>Leclercq</b> I am in disguise", 'html')
        msgAlternative.attach(msgText)
        msg.attach(msgAlternative)
        backend = backends[settings.EMAIL['backend']]()
        backend.send_message(msg)
        log.info(f'testmail sent for {receiver}')
    except Exception:
        log.exception('failed')    


def sendconfirmationmail(s: SubscriptionDetailedOut):
    """
    send confirmation email
    :param s: the Subscription
    :return: None
    """
    sub = {
        'fullname': f"{s.first_name} {s.last_name}",
        'birthdate': s.birthdate,
        'idclub': s.idclub,
        'nationality': s.nationality,
        'ratingbel': s.ratingbel,
        'ratingfide': s.ratingfide,
        'category': s.category,
        'paymessage': s.paymessage,
    }
    i18n = locale_msg[s.locale]
    tolist = []
    if s.emailattendant:
        tolist.append(s.emailattendant)
    if s.emailparent:
        tolist.append(s.emailparent)
    if s.emailplayer:
        tolist.append(s.emailplayer)
    sub['champ'] = i18n['To be confirmed']
    if s.nationality == 'BEL':
        sub['champ'] = i18n['Yes']
    elif s.nationality :
        sub['champ'] = i18n['No']
    tpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    with open(os.path.join(tpath,f'mailsubscription_{s.locale}.md')) as tmpl:
        plaintext = tmpl.read()
    plaintext = plaintext.format(**sub)
    log.info(f'plaintext {plaintext}')

    # fetch the subject from the first line
    subject = plaintext.split('\n')[0][3:]
    htmltext = md.convert(plaintext)

    # create message and send it
    try:
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL['sender']
        msg['To'] = ','.join(tolist)
        if settings.EMAIL.get('bcc'):
            msg['Bcc'] = settings.EMAIL['bcc']
        msg.preamble = 'This is a multi-part message in MIME format.'
        msgAlternative = MIMEMultipart('alternative')
        msgText = MIMEText(plaintext)
        msgAlternative.attach(msgText)
        msgHtml = MIMEText(htmltext, 'html')
        msgAlternative.attach(msgHtml)
        msg.attach(msgAlternative)
        backend = backends[settings.EMAIL['backend']]()
        backend.send_message(msg)
    except:
        log.exception('sending subscription email failed')
