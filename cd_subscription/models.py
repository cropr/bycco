# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.db.models import *
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class CdSubscription(Model):

    badgeimage = BinaryField(_("Badge image"), blank=True)
    badgelength = IntegerField(_("Length badge image"), blank=True, default=0)
    badgemimetype = CharField("Badge mimetype", blank=True, default='', max_length=20)
    birthdate = DateField(_("Birthdate"), null=True)
    category = CharField(_("Category"), max_length=4)  # ARB, ORG, Bxx, Gxx, BGxx, SPO, EAT
    confirmed = BooleanField(default=False)
    chesstitle = CharField(_("Chess title"), max_length=4, blank=True)
    emailparent = EmailField(_("Email parent"), max_length=40, blank=True, default='')
    emailplayer = EmailField(_("Email player"), max_length=40, blank=True, default='')
    federation = CharField(_("Federation"), max_length=4, blank=True)
    fidenation = CharField(_("Fide nation"), max_length=4, blank=True)
    fiderating = IntegerField(_("Fide rating"), default=0)
    firstname = CharField(_("First name"), max_length=25)
    fullnameattendant = CharField(_("Full name responsible on site"), max_length=50, blank=True, default='')
    fullnameparent = CharField(_("Full name parent"), max_length=50, blank=True, default='')
    gender = CharField(_("Gender"), max_length=1, choices=(('M', _('Male')), ('F', _('Female'))))
    id_club = CharField(_("Club id"), max_length=4, blank=True)
    id_fide = CharField(_("Fide id"), max_length=15, blank=True)
    id_national = CharField(_("National id"), max_length=6, unique=True)
    locale = CharField(_("Locale"), max_length=5)
    mobileattendant = CharField(_("GSM number responsible on site"), max_length=15, blank=True, default='')
    mobileparent = CharField(_("GSM parent"), max_length=15, blank=True, default='')
    mobileplayer = CharField(_("GSM player"), max_length=15, blank=True, default='')
    name = CharField(_("Name"), max_length=40)
    nationality = CharField(_("Nationality"), max_length=4, blank=True)
    natrating = IntegerField(_("Fide rating"), default=0)
    payamount = IntegerField(_("Amount to pay"), blank=True, default=0)
    paydate = DateField(_("Payment date"), null=True,)
    paymessage = CharField(_("Payment message"), max_length=20, default='', blank=True)
    rating = IntegerField(_("Used rating"), default=0)
    remarks = TextField(_("Remarks"), blank=True)
    custom1 = TextField(blank=True)                     # maaltijdregime
    custom2 = TextField(blank=True)                     # aangemeld
    custom3 = TextField(blank=True)

    def __str__(self):
        return '%s %s' % (self.firstname, self.name)


class BelPlayer(Model):

    birthdate = DateField(_("Birthdate"))
    chesstitle = CharField(_("Chess title"), max_length=4, blank=True)
    federation = CharField(_("Federation"), max_length=4)
    firstname = CharField(_("First name"), max_length=25)
    gender = CharField(_("Gender"), max_length=1, choices=(('M', _('Male')), ('F', _('Female'))))
    id_club = CharField(_("Club id"), max_length=4)
    id_fide = CharField(_("Fide id"), max_length=15)
    id_national = CharField(_("National id"), max_length=6, primary_key=True)
    name = CharField(_("First name"), max_length=40)
    nationality = CharField(_("Nationality"), max_length=4)
    natrating = IntegerField(_("Fide rating"), default=0)

class FidePlayer(Model):

    firstname = CharField(_("First name"), max_length=40)
    name = CharField(_("First name"), max_length=50)
    gender = CharField(_("Gender"), max_length=1, choices=(('M', _('Male')), ('F', _('Female'))))
    id_fide = CharField(_("Fide id"), max_length=15, primary_key=True)
    chesstitle = CharField(_("Chess title"), max_length=4, blank=True)
    fiderating = IntegerField(_("Fide rating"), default=0)
    fidenation = CharField(_("Fide nation"), max_length=4)

class SmsRegistration(Model):
    mobile = CharField(max_length=20)
    id_national = CharField(max_length=6)
    locale = CharField(max_length=5)

