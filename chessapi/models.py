from django.db.models import *

# Create your models here.

class BelPlayer(Model):

    birthdate = DateField("Birthdate")
    chesstitle = CharField("Chess title", max_length=4, blank=True)
    federation = CharField("Federation", max_length=4)
    first_name = CharField("First name", max_length=25)
    gender = CharField("Gender", max_length=1)
    id_club = CharField("Club id", max_length=4)
    id_fide = CharField("Fide id", max_length=15)
    id_national = CharField("National id", max_length=6, primary_key=True)
    last_name = CharField("Last name", max_length=40)
    nationality = CharField("Nationality", max_length=4)
    natrating = IntegerField("Fide rating", default=0)

class FidePlayer(Model):

    first_name = CharField("First name", max_length=40)
    last_name = CharField("Last name", max_length=50)
    gender = CharField("Gender", max_length=1)
    id_fide = CharField("Fide id", max_length=15, primary_key=True)
    chesstitle = CharField("Chess title", max_length=4, blank=True)
    fiderating = IntegerField("Fide rating", default=0)
    fidenation = CharField("Fide nation", max_length=4)
