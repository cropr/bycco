# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

import logging
log = logging.getLogger(__name__)

from django.utils.translation import ugettext as _
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import get_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.conf import settings
import smtplib

mailfrom = 'info@bycco.be'
mailcc = 'confirmation@bycco.be'


def sendconfirmationmail(s):
    """
    send confirmation email
    :param s:
    :return:
    """
    sub = {
        'fullname': "{0} {1}".format(s.first_name, s.last_name),
        'birthdate': s.birthdate.strftime("%d/%m/%Y"),
        'idclub': s.idclub,
        'nationalityfide': s.nationalityfide,
        'natstatus': 'maybe',
        'ratingbel': s.ratingbel,
        'ratingfide': s.ratingfide,
        'gender': s.gender,
        'category': s.category,
        'paymessage': s.paymessage,
    }
    if s.nationalityfide == 'BEL':
        sub['natstatus'] = 'fidebelg'
    elif s.nationalityfide and len(s.nationalityfide) > 1:
        sub['natstatus'] = 'nobelg'
    context = {'sub':sub}
    tolist = []
    if s.emailplayer:
        tolist.append(s.emailplayer)
    if s.emailparent:
        tolist.append(s.emailparent)

    msghtml = get_template('subscription/mailhtml.html').render(
        context=context)
    image = MIMEImage(s.badgeimage, _subtype=s.badgemimetype, name='badge.png')
    image.add_header('Content-ID', '<1>')
    msg = EmailMessage(
        subject=_('Confirmation Subscription'), to=tolist, from_email=mailfrom,
        cc=[mailcc], attachments=[image], body=msghtml
    )
    msg.content_subtype = 'html'
    msg.send()
