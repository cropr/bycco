## Reservierungsbestätigung für den Aufenthalt BJLM 2025

Diese E-Mail wurde automatisch gesendet.

Wir bestätigen Ihre Bewerbung für einen Aufenthalt während der BJLM 2025.

Bei Fehlern in den unten aufgeführten Angaben kontaktieren Sie uns bitte unter <floral@bycco.be> unter Angabe Ihrer Handynummer.

Den Preis senden wir Ihnen nach Zuteilung der Unterkunft per E-Mail zu. Erst nach Zahlung des angegebenen Betrages ist die Unterkunft endgültig bestätigt

_Das Bycco-Team_

### Details verantwortliche Person

- Name: {{ first_name }} {{ last_name }}
- Email: {{ email }}
- Mobil: {{ mobile }}
- Adresse: <br>{{ address | replace("\n", "<br>")}}

### Details Gäste

{% for g in guestlist %}

- Name: {{ g.first_name }} {{ g.last_name }} <br>
    Geburtstag: {{ g.birthdate }} <br>
    Spieler: {{ "Ja" if g.player else "Nein" }} <br>
    Alterskategorie: {{ g.age_category }} <br>
{% endfor %}

### Details Unterkunft und Catering

- Typ: {{ stay }}
- Ankunftsdatum: {{ checkindate[0:10] }}
- Abreisedatum: {{ checkoutdate[0:10] }}
- Mahlzeiten: {{ meals }}

### Bemerkungen

{{ (remarks if remarks else "Keine Bemerkungen") | replace("\n", "<br>")}}
