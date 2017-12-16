# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

import logging
log = logging.getLogger(__name__)

from django.utils.translation import ugettext as _
from django.template import Context
from django.template.loader import get_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.conf import settings
import smtplib

mailfrom = 'info@bycco.be'
mailcc = ['luc.cornet@telenet.be']

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
    context = Context({'sub':sub})

    # make root object of message
    msg = MIMEMultipart('related')
    msg['Subject'] = _('Confirmation Subscription')
    tolist = []
    if s.emailplayer:
        tolist.append(s.emailplayer)
    if s.emailparent:
        tolist.append(s.emailparent)
    msg['From'] = 'info@bycco.be'
    msg['To'] = ', '.join(tolist)
    msg['CC'] = ', '.join(mailcc)

    # # make html and text alternatives
    # alternatives = MIMEMultipart('alternative')
    # msgtext = MIMEText(get_template('cd_subscription/mailtext.html').render(
    #     context=context))
    # alternatives.attach(msgtext)
    # msghtml = MIMEText(get_template('cd_subscription/mailhtml.html').render(
    #     context=context))
    # alternatives.attach(msghtml)
    # msg.attach(alternatives)

    msghtml = MIMEText(get_template('subscription/mailhtml.html').render(
        context=context), 'html', 'utf-8')
    msg.attach(msghtml)

    # add image
    image = MIMEImage(s.badgeimage, _subtype=s.badgemimetype, name='badge.png')
    image.add_header('Content-ID', '<1>')
    msg.attach(image)

    # send it
    if settings.EMAIL_HOST:
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        user = settings.EMAIL.USER if hasattr(settings, "EMAIL_USER") else None
        s = smtplib.SMTP(host, port)
        if user:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(user, settings.EMAIL_PASSWORD)
        s.sendmail('organisatie@bjk2017.be', tolist + mailcc, msg.as_string())
        s.close()
    else:
        log.debug('No mail sent')