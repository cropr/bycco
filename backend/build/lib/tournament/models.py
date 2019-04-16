# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.db.models import *
from django.utils.translation import ugettext_lazy as _

# Create your models here.

playercategories = [
    'B8', 'G8',
    'B10', 'G10',
    'B12', 'G12',
    'B14', 'G14',
    'B16', 'G16',
    'B18', 'G18',
    'B20', 'G20',
    'IMT',
]


class Subscription(Model):

    badgeimage = BinaryField(_("Badge image"), blank=True)
    badgelength = IntegerField(_("Length badge image"), blank=True, default=0)
    badgemimetype = CharField("Badge mimetype", blank=True, default='', max_length=20)
    birthdate = DateField(_("Birthdate"), null=True)
    category = CharField(_("Category"), max_length=4)  # ARB, ORG, Bxx, Gxx, BGxx, SPO, EAT
    confirmed = BooleanField(default=False)
    chesstitle = CharField(_("Chess title"), max_length=4, blank=True, default='')
    emailparent = EmailField(_("Email parent"), max_length=40, blank=True, default='')
    emailplayer = EmailField(_("Email player"), max_length=40, blank=True, default='')
    federation = CharField(_("Federation"), max_length=4, blank=True)
    first_name = CharField(_("First name"), max_length=25)
    fullnameattendant = CharField(_("Full name responsible on site"), max_length=50, blank=True, default='')
    fullnameparent = CharField(_("Full name parent"), max_length=50, blank=True, default='')
    gender = CharField(_("Gender"), max_length=1, choices=(('M', _('Male')), ('F', _('Female'))))
    idclub = CharField(_("Club id"), max_length=4, blank=True)
    idfide = CharField(_("FIDE id"), max_length=15, blank=True)
    idbel = CharField(_("Belgian id"), max_length=6, unique=True)
    locale = CharField(_("Locale"), max_length=5)
    meals = CharField('Meals', max_length=15, blank=True, default='')   
        # FB (full baording), HP (half pension), BR (breakfast), or custom
    mobileattendant = CharField(_("GSM number responsible on site"), max_length=15, blank=True, default='')
    mobileparent = CharField(_("GSM parent"), max_length=15, blank=True, default='')
    mobileplayer = CharField(_("GSM player"), max_length=15, blank=True, default='')
    last_name = CharField(_("Last name"), max_length=40)
    nationalitybel = CharField(_("Nationality Passport"), max_length=4, blank=True)
    nationalityfide = CharField(_("Nationality FIDE"), max_length=4, blank=True)
    payamount = IntegerField(_("Amount to pay"), blank=True, default=0)
    paydate = DateField(_("Payment date"), null=True,)
    paymessage = CharField(_("Payment message"), max_length=20, default='', blank=True)
    present = DateTimeField('Check-in time', null=True)
    rating = IntegerField(_("Used rating"), default=0)
    ratingbel = IntegerField(_("Belgian rating"), default=0)
    ratingfide = IntegerField(_("FIDE rating"), default=0)
    remarks = TextField(_("Remarks"), blank=True)
    custom1 = TextField(blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class CdTournament(Model):
    name = CharField(max_length=50)
    shortname = CharField(max_length=10)
    rounds = IntegerField(default=9)
    creationdate = DateTimeField(auto_now_add=True)

class CdTournamentPrizes(Model):
    tournament = OneToOneField(CdTournament,
        on_delete=CASCADE,
        primary_key=True,)
    jsonprizes = TextField(max_length=50, default='')

class CdPlayer(Model):
    birthdate = DateField()
    chesstitle = CharField(max_length=4, blank=True)
    clubname = CharField(max_length=40)
    federation = CharField(max_length=4)
    fidenation = CharField(max_length=4, blank=True)
    fiderating = IntegerField(default=0)
    firstname = CharField(max_length=25)
    gender = CharField(max_length=1, choices=(
        ('M', _('Male')),
        ('F', _('Female'))
    ))
    id_club = CharField(_("Club id"), max_length=4)
    id_fide = CharField(_("Fide id"), max_length=15, blank=True)
    id_national = CharField(_("National id"), max_length=6, unique=True)
    id_trn = ForeignKey(CdTournament, on_delete=CASCADE)
    name = CharField(_("Name"), max_length=40)
    nationality = CharField(_("Nationality"), max_length=4)
    natrating = IntegerField(_("Fide rating"), default=0)
    rating = IntegerField(default=0)

class CdStanding(Model):
    ngames = IntegerField()
    player = ForeignKey(CdPlayer, on_delete=CASCADE)
    points = DecimalField(max_digits=4, decimal_places=2)
    ranknr = IntegerField()
    round = IntegerField()

class CdPairing(Model):
    black = CharField(max_length=50)
    boardnr = IntegerField()
    id_black = ForeignKey(CdPlayer, on_delete=CASCADE, related_name='black')
    id_white = ForeignKey(CdPlayer, on_delete=CASCADE, related_name='white')
    result = CharField(max_length=6)
    round = IntegerField()
    white = CharField(max_length=50)

class CdScoreCard(Model):
    color = CharField(max_length=1, choices=(
        ('W', _("white")),
        ('B', _("black")),
        ('N', _("notassigned")),
    ))
    float = CharField(max_length=2)
    id_oppponent = ForeignKey(CdPlayer, on_delete=CASCADE, related_name='player')
    id_player = ForeignKey(CdPlayer, on_delete=CASCADE, related_name='opponent')
    opponent = CharField(max_length=50)
    player = CharField(max_length=50)
    points = DecimalField(max_digits=4, decimal_places=2)
    round = IntegerField()
    result = CharField(max_length=6)

class CdSwarTournament(Model):
    tournament = OneToOneField(CdTournament,
        on_delete=CASCADE,
        primary_key=True,)
    swarname = CharField(max_length=50, default='')

class CdSwarJson(Model):
    STATUSES = (
        ('ACT', 'Active'),
        ('OUT', 'Outdated'),
        ('UNP', 'Unpublished'),
    )

    round = IntegerField()
    jsonfile = TextField()
    swartrn = ForeignKey(CdSwarTournament, on_delete=CASCADE)
    uploaddate = DateTimeField(auto_now_add=True)
    status = CharField(max_length=3, choices=STATUSES, default='UNP')

class CdSwarPairings(Model):
    round = IntegerField()
    jsonpairings = TextField()
    swartrn = ForeignKey(CdSwarTournament, on_delete=CASCADE)    

class CdSwarStandings(Model):
    round = IntegerField()
    jsonstandings = TextField()
    swartrn = ForeignKey(CdSwarTournament, on_delete=CASCADE)    



class TrnInvoice(Model):
    id_participant = IntegerField()
    creationdate = DateTimeField()
    emailresponsible = CharField(max_length=50)
    first_name = CharField(max_length=25)
    fullnameresponsible = CharField(max_length=50)
    invoicenumber = IntegerField()
    last_name = CharField(max_length=40)
    locale = CharField(max_length=6, default='en')
    modifieddate = DateTimeField()
    pdf = BinaryField(null=True)
    pricewithvat = DecimalField(max_digits=6, decimal_places=2)
    pricewithoutvat = DecimalField(max_digits=6, decimal_places=2)
    sentdate = DateTimeField(null=True)
    vat = DecimalField(max_digits=6, decimal_places=2)
