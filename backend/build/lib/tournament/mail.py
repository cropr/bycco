# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

import logging
log = logging.getLogger(__name__)

from django.utils import translation
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.utils.html import strip_tags
from django.template.loader import get_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.conf import settings
from rd_django.templatetags.rd_i18n import translate

mailfrom = 'info@bycco.be'
mailcc = 'confirmation@bycco.be'

def sendconfirmationmail(request, s):
    """
    send confirmation email
    :param s: the Subscription object
    :return: None
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
    translation.activate(s.locale)
    msghtml = get_template('tournament/mailhtml.html').render(
        context=context, request=request)
    msgtext = strip_tags(msghtml)
    image = MIMEImage(s.badgeimage, _subtype=s.badgemimetype, name='badge.png')
    image.add_header('Content-ID', '<1>')
    msg = EmailMultiAlternatives(
        translate('Confirmation Subscription', s.locale),
        msgtext,
        to=tolist,
        from_email=mailfrom,
        cc=[mailcc],
    )
    translation.deactivate()
    msg.attach_alternative(msghtml, "text/html")
    msg.attach(image)
    msg.send()

