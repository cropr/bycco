# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.db.models import *
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Subscription(Model):

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
    first_name = CharField(_("First name"), max_length=25)
    fullnameattendant = CharField(_("Full name responsible on site"), max_length=50, blank=True, default='')
    fullnameparent = CharField(_("Full name parent"), max_length=50, blank=True, default='')
    gender = CharField(_("Gender"), max_length=1, choices=(('M', _('Male')), ('F', _('Female'))))
    idclub = CharField(_("Club id"), max_length=4, blank=True)
    idfide = CharField(_("Fide id"), max_length=15, blank=True)
    idbel = CharField(_("Belgian id"), max_length=6, unique=True)
    locale = CharField(_("Locale"), max_length=5)
    mobileattendant = CharField(_("GSM number responsible on site"), max_length=15, blank=True, default='')
    mobileparent = CharField(_("GSM parent"), max_length=15, blank=True, default='')
    mobileplayer = CharField(_("GSM player"), max_length=15, blank=True, default='')
    last_name = CharField(_("Last name"), max_length=40)
    nationalitybel = CharField(_("Nationality Passport"), max_length=4, blank=True)
    nationalityfide = CharField(_("Nationality Fide"), max_length=4, blank=True)
    payamount = IntegerField(_("Amount to pay"), blank=True, default=0)
    paydate = DateField(_("Payment date"), null=True,)
    paymessage = CharField(_("Payment message"), max_length=20, default='', blank=True)
    rating = IntegerField(_("Used rating"), default=0)
    ratingbel = IntegerField(_("Fide rating"), default=0)
    ratingfide = IntegerField(_("Fide rating"), default=0)
    remarks = TextField(_("Remarks"), blank=True)
    custom1 = TextField(blank=True)                     # maaltijdregime
    custom2 = TextField(blank=True)                     # aangemeld
    custom3 = TextField(blank=True)

    def __str__(self):
        return '%s %s' % (self.firstname, self.name)
