# copyright Ruben Decrop 2012-2019

import logging
log = logging.getLogger(__name__)


import decimal
import pdfkit
import base64
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.utils import translation, timezone
from django.core.mail import EmailMessage
from django.conf import settings
from email.mime.application import MIMEApplication
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
from rest_framework.response import Response

from .models import (
    playercategories,
    Subscription,
    TrnInvoice,
)

from .serializers import (
    TrnInvoiceSerializer,
)

def create_invoice(sub, recreate=True):
    """
    creates and saves a TrnInvoice object for a subcription
    :param sub: the Subscription Object
    :param recreate: boolean: recreates the invoice if it already exists
    :return: the invoice (saved to the DB)
    """

    try:
        invoice = TrnInvoice.objects.get(id_participant=sub.id)
    except TrnInvoice.DoesNotExist:
        invoice = None
    if invoice:
        if not recreate:
            return invoice
    else:
        invoice = TrnInvoice()
        invoice.id_participant = sub.id
        invoice.creationdate = timezone.now()
        invoice.invoicenumber = 2019010000 + sub.id
    invoice.modifieddate = timezone.now()
    invoice.emailresponsible = sub.emailparent or sub.emailplayer
    invoice.fullnameresponsible = sub.fullnameparent or (
        "{0} {1}".format(sub.first_name, sub.last_name))
    invoice.first_name = sub.first_name
    invoice.last_name = sub.last_name
    invoice.pricewithvat = decimal.Decimal(sub.payamount).quantize(
        decimal.Decimal('.01'))
    invoice.pricewithoutvat = (invoice.pricewithvat / decimal.Decimal(
        1.06)).quantize(decimal.Decimal('.01'))
    invoice.vat = invoice.pricewithvat - invoice.pricewithoutvat
    create_pdf(invoice, sub.locale)
    invoice.save()
    return invoice

def create_pdf(invoice, locale):
    """
    creates a pdf invoice, and stores it in the invoice object, no save
    :param invoice: an Invoice object for which the pdf must be created
    :param locale: the language
    :return: True if success, False if failure
    """
    translation.activate(locale)
    logobycco = open('bycco/static/img/logo_bycco.png', 'rb')
    imgbycco = logobycco.read()
    logobycco.close()
    imgurl = 'data:image/png;base64,%s' % base64.b64encode(
        imgbycco).decode()
    context = {
        'sub': invoice,
        'imgurl': imgurl,
        'creationdate': invoice.creationdate.strftime("%d-%m-%Y")
    }
    invhtml = get_template('tournament/invoicepdf.html').render(
        context=context)
    try:
        pdfkit.from_string(invhtml, 'invoice.pdf')
        pdffile = open('invoice.pdf', 'rb')
        invoice.pdf = pdffile.read()
        pdffile.close()
    except:
        log.error('Failed to create pdf invoice')
        translation.deactivate()
        return False
    translation.deactivate()
    return True

def send_invoice(invoice, resend=False):
    """
    sends the invoice by email, updates ans saves the invoice.senddate
    :param invoice: the invoice
    :param request: the request
    :param resend: resend the email if it already has been sent
    :return: True if success, False if failure
    """
    try:
        msgtext = get_template('tournament/invoicemail.txt').render().strip()
        msg = EmailMessage(
            _('Invoice'),
            msgtext,
            to=[invoice.emailresponsible],
            from_email=settings.EMAIL_ADDRESSES['invoice_from'],
            cc=settings.EMAIL_ADDRESSES['invoice_cc'],
        )
        pdf = MIMEApplication(invoice.pdf, 'pdf')
        msg.attach(pdf)
        msg.send()
    except:
        return False
    invoice.sentdate = timezone.now()
    invoice.save()
    return True


@api_view(['POST'])
def invoices(request):
    """
    creates and or sends the new invoices
    :param command: one of ['create', 'send', 'create_send']
    :param options: a dict of options:
      - recreate: boolean,
    :return:
    """
    command = request.data('command', '')
    options = request.data('options', {})
    for sub in Subscription.objects.all():
        if sub.category not in playercategories:
            continue
        if command == 'create' or command == 'create_send':
            create_invoice(sub, recreate=options.get('recreate', False))
        if command == 'send' or command == 'create_send':
            send_invoice(sub, resend=options.get('recreate', False))
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def invoice(request, id_part):

    try:
        id_part = int(id_part)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='invalid participant id')

    if request.method == 'GET':
        try:
            invoice = TrnInvoice.objects.get(id_participant=id_part)
        except TrnInvoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='no invoice yet')
        inv_serializer = TrnInvoiceSerializer(invoice)
        return Response(data={'invoice':inv_serializer.data})

    if request.method == 'POST':
        try:
            sub = Subscription.objects.get(id=id_part)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='no related subscription')
        invoice = create_invoice(sub, recreate=True)
        inv_serializer = TrnInvoiceSerializer(invoice)
        return Response(data={'invoice': inv_serializer.data})

@api_view(['POST'])
def invoice_send(request, id_part):

    if request.method == 'POST':
        try:
            invoice = TrnInvoice.objects.get(id_participant=id_part)
        except TrnInvoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='invoice not found')
        send_invoice(invoice, resend=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
