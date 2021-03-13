<template>
  <v-container>
    <h1>{{ title[$i18n.locale] }}</h1>
    <hr />
    <markdown-it-vue class="md-body mt-2" :content="content[$i18n.locale]" />
  </v-container>
</template>

<script>
export default {
  layout: 'default',

  data() {
    return {
      title: {
        en: 'Tournament rules',
        nl: 'Toernooireglement',
        fr: 'Règlement du tournoi',
        de: 'Turnierregeln',
      },
      content: {
        en: `This text is not available in English.  Please select another language`,
        nl: `**versie: 25 september 2020**


Waar in de tekst  gerefereerd wordt naar "hij", "hem" of "zijn", wordt eveneens "zij" of "haar" bedoeld.

Indien de teksten of zelfs de nuances in de talen van het reglement zouden verschillen, is het reglement in het Nederlands dat geldt.

## Algemeen

1. Voor het Belgisch Jeugdkampioenschap zijn de reglementen van KBSB, op datum van aanvang van de inschrijving, van toepassing. Ook de beslissing van het bestuursorgaan op 15/09/2020 over het format van dit kampioenschap is van toepassing. Dit reglement geldt op aanvullende wijze. Daarnaast zijn ook alle [Covid 19 maatregelen](/page/covid19) die een speler heeft aanvaard bij zijn inschrijving, van kracht.

2. Er zijn 7 leeftijdsreeksen (-8, -10, -12, -14, -16, -18 en -20). De leeftijdsreeksen zijn onderverdeeld in een reeks voor jongens en een reeks voor meisjes.

3. Voor aanvang van het toernooi zal de toernooileiding in samenspraak met de wedstrijdleiding beslissen over de indeling van de reeksen. Bijvoorbeeld door de -18 en -20, of door jongens en meisjes, samen in te delen.

4. Er zijn prijzen voor elke reeks waarvoor men zich inschrijft. De volgorde wordt bepaald volgens de reeks waarin men is ingedeeld. Dus, indien meerdere reeksen werden samengevoegd, wordt enkel rekening gehouden met de volgorde van het klassement van de samengestelde reeks.

5. Een speler kan zich inschrijven in de leeftijdsreeks op basis van zijn of haar geslacht en leeftijd op 31 december 2019. Een speler kan zich inschrijven in een hogere leeftijdsreeks.

## Notatie

6. Notatie is verplicht voor iedere speler in alle reeksen (minimum vereiste notatie = 5 tekens voor de stukken: K/D/T/P/L). Elke speler (ook bij de -8) dient de zetten te kunnen opschrijven. Foutloos hoeft niet, maar dient wel nagestreefd te worden.

## Spelersgebied

7. Het spelersgebied bestaat uit alle toernooizalen, de dichtstbijzijnde toiletten en de doorgang ernaar. De spelers mogen tijdens de partij het spelersgebied niet verlaten tenzij na uitdrukkelijke goedkeuring van een arbiter. In dat geval zullen de spelers altijd vergezeld worden door een arbiter of een lid van de organisatie.

8. Geschrapt.

9. Een speler mag zijn mobiele telefoon in de speelzaal binnenbrengen maar moet deze voor de aanvang van de partij uitschakelen. De mobiele telefoon moet opgeborgen worden, of naast het bord gelegd worden. Een speler die zich tijdens de partij van zijn mobiele telefoon bedient, of waarvan zijn telefoon enige geluid maakt verliest de partij. De arbiter bepaalt het resultaat van de tegenstander.

10. Spelers mogen geen schaaktechnische hulpmiddelen binnenbrengen in het spelersgebied (schaakboeken, schaakcomputer, enz...).

11. De spelers dienen de stilte in het spelersgebied te respecteren. Elke onnodige vorm van communicatie, verbaal of niet, is verboden.

12. Spelers zullen in geval van overtreding gesanctioneerd worden conform het FIDE reglement.
 
## Toernooizalen
 
13. Geschrapt.

14. Een speler, die zijn partij beëindigd heeft, wordt aanzien als toeschouwer. Hij dient zoals vermeld in de sectie [Covid 19 maatregelen](/page/covid19) onmiddellijk naar de wachtruimte te gaan of de gebouwen te verlaten.

## Voedsel en drank

15. In de toernooizalen is alcohol verboden.

16. Aangezien er geen drank zal aangeboden worden door de organisatie, kunnen spelers eigen drank meenemen in de toernooizaal.

17. Spelers mogen in het spelersgebied een kleine snack eten enkel achter het bord en enkel als ze aan zet zijn (om de tegenstander nooit te storen).

18. Bij het verlaten van de speelzaal na hun partij dienen de spelers hun tafel volledig afvalvrij achter te laten.

## Mededelingen

19. Alle officiële mededelingen van de organisatoren (bijv. samenstelling van de commissies, paringen en klassementen, speelschema, enz...) worden enkel via de toernooiwebsite verspreid. Op aanvullende, niet bindende wijze, kunnen de organisatoren gebruik maken van andere media e-mail, sms, de app Chessout (enkel Android), enz...

## Scheidingssysteem

20. De door de FIDE voorgestelde scheidingssystemen worden gehanteerd

Zie het [FIDE-handbook C02](https://handbook.fide.com/files/handbook/C02Standards.pdf) art. 13.16.2. voor Round-Robin-groepen en art. 13.16.4 voor Zwitserse groepen.
 
## Paringen
 
21. De paringen gebeuren met de laatste beschikbare versie van Swar.
 
## ELO verwerking
 
22. De resultaten van alle partijen van alle groepen worden doorgegeven voor zowel FIDE-ELO- als voor Belgische ELO-verwerking.
 
## Aantal rondes en tempo
 
23. Het aantal rondes is 7. De leeftijdsreeksen van -8 en -10 spelen enkel op zaterdag (4 rondes: om 9u30, 12u30, 15u, 17u30) en zondag (3 rondes om 9u30, 12u, 14u30). De andere leeftijdsreeksen spelen op donderdag, vrijdag en zaterdag 2 rondes (om 9u30 en 15u) en op zondag 1 ronde (om 9u30). Er is vóór de eerste ronde geen openingsceremonie en na de laatste ronde geen slotceremonie.

24. Het tempo is als volgt vastgelegd:
 
- voor de leeftijdsreeksen -12 tot -20:   90 minuten voor de gehele partij + 30 seconden toevoeging per zet vanaf zet 1. Dit tempo heeft als gevolg dat alle spelers verplicht zijn alle zetten te noteren, dus ook wanneer hun klok minder dan 5 minuten aanwijst!
- voor de leeftijdsreeksen -8 en -10:  45 minuten voor de gehele partij + 15 seconden toevoeging per zet vanaf zet 1.  Van zodra een speler voor de eerste keer minder dan 5 minuten op de klok heeft, is hij niet langer verplicht te noteren.
 
## Afwezigheid van spelers
 
25. Indien een speler uit de leeftijdsreeks -12 tot -20 60 minuten of meer te laat komt aan het bord of indien een speler uit de leeftijdsreeks -8 tot -10 45 minuten of meer te laat komt aan het bord telkens ten opzichte van het vooraf aangekondigd aanvangsuur, dan verliest deze de partij. Wanneer hij/zij afwezig is zonder een gegronde reden of indien hij de organisatie hierover niet informeert voordat de volgende ronde gepaard wordt, dan wordt hij vanaf die volgende ronde uit het toernooi genomen. Wanneer een speler weet dat hij een volgende ronde afwezig zal zijn met een gegronde reden en de wedstrijdleider hierover informeert, dan wordt hij niet gepaard voor de volgende ronde(s). Indien de paring reeds bekend is, dan wordt er een forfait toegekend, maar de speler in kwestie wordt wel opnieuw gepaard voor de volgende ronde(s) waarvoor hij zich aanwezig heeft gemeld.
 
26. Om een afwezigheid te melden moet men contact opnemen met de toernooileiding (Luc Cornet gsm +32/474/99.52.74). Laat altijd een bericht na en vermeld duidelijk naam, het probleem en telefoonnummer waarop men terug kan bellen.
 
## Klachten
 
27. Elke groep heeft één of meerdere arbiters. Bij een probleem aan het bord kan de speler de klok stoppen en een arbiter roepen. Deze neemt een beslissing.
 
28. Indien een speler hier niet akkoord mee gaat, kan hij onmiddellijk mondeling klacht indienen bij de hoofdarbiter die dan de versies van zowel de speler als de arbiter aanhoort. Daarna bevestigt de hoofdarbiter de beslissing van de arbiter of annuleert hij die. De partij wordt vervolgens hervat (indien nodig).
 
29. Indien een speler ook niet met de beslissing van de hoofdarbiter akkoord gaat, dan kan hij tot uiterlijk een kwartier na zijn partij beroep aantekenen. Hij dient zijn klacht schriftelijk te motiveren en aan de hoofdarbiter te overhandigen, samen met een waarborg van 50 EUR. Op zijn beurt roept de hoofdarbiter de beroepscommissie samen die dan een definitieve beslissing neemt.

Tegen de beslissing van de beroepscommissie is er geen beroep meer mogelijk. De commissie beslist ook – op basis van de juistheid van de motivering van de klacht - of de waarborg geheel of gedeeltelijk aan de klager dient te worden terugbetaald.
 
## Selectie
 
30. Zoals bepaald in zijn reglementen zal de KBSB voor zover er nog Europese- en wereldkampioenschappen voor de jeugd zullen plaats vinden voor aanvang van het volgend Belgisch jeugdkampioenschap het resultaat behaald door een speler in dit Belgisch jeugdkampioenschap gebruiken als selectiecriterium voor Europese – en wereldkampioenschappen.
 
31. Voor zover er voor aanvang van het volgend Belgisch Kampioenschap geen Belgisch jeugdkampioenschap zal plaats vinden, is de kampioen(e) met de hoogste elo uit alle leeftijdreeksen automatisch geselecteerd bij de expertenreeks van het volgend Belgisch Kampioenschap, mits deze voldoet aan de criteria.

## Sancties en disciplinaire maatregelen

32. Art 14 van het Wedstrijdreglement van de KBSB en Art 14 van de statuten van de KBSB zijn altijd van toepassing.
`,
        fr: `**version: 25 septembre 2020**

Partout dans le texte où on fait une référence à "il" ou "lui", ça fait 
également référer à "elle'.

Si les textes ou mêmes les nuances dans les langues du règlement diffèrent, 
c’est le règlement en néerlandais qui fait foi.

## Généralités

1. Les règlements de la FRBE en vigueur au moment du début des inscriptions 
sont applicables pour le championnat de Belgique de la jeunesse. La décision 
de l’organe d’administration du 15/09/2020 sur le format de ce championnat 
s'applique également. Le présent règlement s'applique en complément. De plus, 
toutes les [mesures Covid 19](/page/covid19), acceptées par le joueur lors de 
son inscription, sont également en vigueur.

2. Il y a 7 catégories d'âge (-8, -10, -12, -14, -16, -18 et -20). Chacune des 
catégories d’âge est à son tour répartie en une catégorie garçons et une 
catégorie filles.

3. Avant le début du tournoi, la direction du tournoi se concertera avec la 
direction d' arbitrage de la compétition afin de décider de la répartition 
des groupes de joueurs. Par exemple, de réunir les -18 et les -20, ou les 
garçons et les filles en une seule compétition.

4. Des prix sont prévus pour chacune des catégories dans laquelle le joueur 
peut s’inscrire. Le classement est déterminé par le classement de la catégorie 
dans laquelle le joueur a joué. Donc, si plusieurs catégories ont été réunies, 
on tiendra seulement compte de l'ordre du classement obtenu du classement de 
la catégorie réunie.

5. Un joueur peut s’inscrire dans une catégorie d'âge sur base de son sexe 
et de son âge au 31 décembre 2019. Un joueur peut choisir de jouer dans une 
catégorie d’âge supérieure.

## Notation

6. La notation est obligatoire pour tous les joueurs dans toutes les 
catégories (obligation minimale = les lettres des 5 pièces : R/D/T/C/F). 
Tous les joueurs (même les -8) doivent savoir noter les coups. Le sans-
faute n’est pas requis, mais il faudra malgré tout tenter d’y arriver.

## Zone de jeu

7. La zone de jeu comprend toutes les salles de tournoi, les toilettes les 
plus proches et leur accès. Le lobby de l'hôtel ne fait pas partie de la 
zone de jeu. Les joueurs ne peuvent pas quitter la zone de jeu pendant la 
partie, sauf accord explicite d’un arbitre. Dans ce cas le joueur sera 
toujours accompagné d’un arbitre ou d’un membre de l’organisation

8. Supprimé.

9. Un joueur peut apporter son téléphone mobile dans la salle de jeu, 
mais il devra l’éteindre avant le début de la partie. Le téléphone mobile 
doit être rangé ou il doit être déposé à côté de l’échiquier. Un joueur qui 
se sert de son téléphone mobile pendant la partie ou dont le téléphone émet 
le moindre bruit, perd la partie. L’arbitre détermine le résultat de 
l’adversaire.

10. Les joueurs ne peuvent pas emmener de moyens d'aide échiquéens (livres 
d'échecs, ordinateur d'échecs, ...) dans la zone de jeu.

11. Les joueurs doivent respecter le silence dans la zone de jeu. Toute 
forme de communication non nécessaire, verbale ou non, est interdite.

12. En cas d'infraction, les joueurs seront sanctionnés conformément au 
règlement de la FIDE. 
    
## Salles de tournoi

13. Supprimé.

14. Un joueur, qui a terminé sa partie est considéré comme un spectateur. 
Comme indiqué dans la section mesures Covid 19, il doit immédiatement aller 
vers la zone d'attente ou quitter les lieux.

## Nourriture et boissons

15. L'alcool est interdit dans les salles de tournoi.

16. Puisqu’aucune boisson ne sera offerte par l'organisation, les joueurs 
peuvent amener leur propre boisson dans la salle de jeu.

17. Les joueurs peuvent manger un petit snack dans la zone de jeu, seulement 
devant l'échiquier et seulement quand c'est leur trait (de ne jamais déranger 
l'adversaire).

18. En quittant la salle de jeu après leur partie, les joueurs veilleront à 
nettoyer complètement leur table et donc à les laisser débarrassées de tout 
déchet.

## Communications

19. Pendant le tournoi, toutes les communications officielles des 
organisateurs (par ex. la composition des commissions, les appariements et 
les classements, le calendrier, ...) ne sont distribués que sur le site 
web du tournoi. En complément, sans obligation, les organisateurs peuvent 
faire usage d'autres moyens tels que l'e-mail, les sms, l'application 
Chessout (Android uniquement), etc.

## Système de départage

20. Les systèmes de départage proposés par la FIDE sont utilisés:

Voir [le manuel FIDE C02](https://handbook.fide.com/files/handbook/C02Standards.pdf) 
art. 13.16.2. pour les groupes Round-Robin et l'art. 13.16.4 pour les groupes 
suisses.
    
## Appariements

21. Les appariements sont réalisés avec la dernière version disponible de Swar.

## Traitement Elo

22. Les résultats de toutes les parties de tous les groupes seront transmis 
tant pour le classement Elo FIDE que pour le classement Elo belge.

## Nombre de rondes et cadence

23. Le nombre de rondes est de 7. Les catégories d'âge -8 et -10 ne jouent 
que le samedi (4 parties: à 9h30, 12h30, 15h, 17h30) et le dimanche (3 
parties à 9h30, 12h, 14h30). Les autres catégories d'âge jouent 2 rondes 
le jeudi, le vendredi et le samedi (à 9h30 et 15h) et 1 ronde le dimanche 
(à 9h30). Il n'y a pas de cérémonie d'ouverture avant la première ronde et 
pas de cérémonie de clôture après la dernière ronde.

24. La cadence est fixée comme suit:

 - pour les catégories d'âge -12 à -20: 90 minutes pour toute la partie + 
 30 secondes incrément par coup à partir du premier coup. Cette cadence a 
 comme conséquence que tous les joueurs doivent noter tous les coups, et ce 
 même si leur pendule indique moins de 5 minutes!
 - pour les catégories d'âge -8 et -10: 45 minutes pour toute la partie + 
 15 secondes incrément par coup à partir du premier coup. Dès la pendule 
 indique moins de 5 minutes pour la première fois, le joueur ne doit plus noter.


## Absence des joueurs

25. Si un joueur d’une catégorie d’âge -12 à -20 arrive devant l’échiquier
 avec un retard de 60 minutes ou plus ou si un joueur d’une catégorie d’âge 
 -8 à -10 arrive devant l’échiquier avec un retard de 45 minutes ou plus, 
 dans les deux cas par rapport à l’heure annoncée, il perd la partie par forfait. Si un joueur est absent sans raison légitime ou s’il n’informe pas l’organisation avant que les appariements pour la ronde suivante ne soient faits, il est retiré du tournoi à partir de la ronde suivante. Si un joueur sait qu'il sera absent à la ronde suivante pour une raison légitime et qu'il en informe l'arbitre, il n’est pas apparié pour la (les) ronde(s) suivante(s). Si l’appariement est déjà publié, le joueur perd la partie par forfait mais le joueur en question restera inclus dans les appariements des rondes suivantes dans lesquelles il a signalé être présent.

26. Pour annoncer une absence, il faut contacter le directeur du tournoi (Luc 
Cornet gsm +32/474/99.52.74). Laissez toujours un message, en mentionnant 
clairement votre nom, le problème et le numéro de téléphone auquel on peut 
vous joindre.

## Plaintes

27. Chaque groupe dispose d’un ou plusieurs arbitres. En cas de problème à 
l’échiquier, le joueur peut arrêter la pendule et appeler un arbitre. 
Celui-ci prend une décision.

28. Si un joueur n’accepte pas cette décision, il peut immédiatement porter 
plainte auprès de l’arbitre principal, qui entendra alors les versions aussi 
bien du joueur que de l’arbitre. Ensuite, l’arbitre principal confirme ou 
révoque la décision de l’arbitre. Ensuite, la partie continue (si nécessaire).

29. Si un joueur rejette également la décision de l’arbitre principal, il peut 
alors interjeter appel au plus tard un quart d'heure après la fin de sa 
partie. Il devra motiver sa plainte par écrit et la remettre à l’arbitre 
principal, avec une caution de 50 EUR. A son tour, l’arbitre principal 
réunira la commission d’appel, qui statuera alors de façon définitive.

Aucun recours n’est possible contre une décision de la commission d’appel. 
La commission décide également – sur la base de la justesse de la motivation 
de la plainte – s’il y a lieu de rembourser la caution intégralement ou 
partiellement.

## Sélection

30. Comme déterminé dans ses règlements, la FRBE, dans la mesure où il aura 
encore lieu des championnats d'Europe et du monde pour la jeunesse avant le 
début du prochain championnat de Belgique des jeunes, utilisera le résultat 
obtenu à ce championnat de Belgique des jeunes comme critère de sélection 
pour les championnats d'Europe et du monde.

31. Dans la mesure où aucun championnat de Belgique des jeunes n'aura lieu 
avant le début du prochain championnat de Belgique, le(la) champion(ne) avec 
le plus d' Elo de toutes les catégories est automatiquement sélectionné(e) 
pour le groupe expert du prochain championnat de Belgique.

## Sanctions et mesures disciplinaires

32. Art. 14 du Règlement des Tournois de la FRBE et art. 15 des statuts de l
a FRBE sont applicables en tout temps.`,
        de: `**Version: 25 September 2020**

Wo sich der Text auf "er", "ihn" oder "sein" verwiesen wird, ist auch "sie" der "ihr" gemeint.

Wenn sich die Texte oder sogar die Nuancen in den Sprachen der Vorschriften unterscheiden würden, gelten die Vorschriften in niederländischer Sprache.

## Allgemein

1. Es gelten die Spielregeln des Belgischen Schachbundes, die zu Beginn der Einschreibungen zur Schach-Jugend-Landesmeisterschaft veröffentlicht sind. Die Entscheidung des Verwaltungsrats vom 15.09.2020 über das Format dieser Meisterschaft gilt ebenfalls. Das folgende Regelwerk gilt als Zusatz. Darüber hinaus sind alle [Covid 19-Maßnahmen](/page/covid19) in Kraft, die ein Spieler bei der Registrierung akzeptiert hat.

2. Gespielt wird in 7 Altersgruppen (U8, U10, U12, U14, U16, U18 und U20). Jede Altersgruppe ist unterteilt in einer Jungen- und Mädchengruppe.

3. Vor Beginn des Turniers entscheidet die Turnierleitung gemeinsam mit der Wettstreitleitung über die Aufteilung der Spielgruppen. Zum Beispiel, ob die U18 und U20 oder Mädchen und Jungen gemeinsam oder getrennt spielen.

4. Preise sind vorgesehen in jeder Gruppe in welche sich ein(e) Teilnehmer einschreiben kann. Der Platz wird bestimmt in der Gruppe in welcher der/die Teilnehmer eingeteilt ist.

5. Ein(e) Teilnehmer kann sich in einer Gruppe Anmelden auf Grund seines/ihres Alters am 31. Dezember 2019. Jede(r) Teilnehmer darf sich in eine höhere Altersgruppe einschreiben.

## Notation

6. Die Notation ist obligatorisch für alle Spieler und in jeder Altersgruppe (minimale Anforderung = die Buchstaben der 5 Figuren: K/D/T/S/L). Alle Spieler (auch die -8) müssen die Züge schreiben können. Ein fehlerfreies Schreiben ist nicht gefordert, aber erstrebenswert.

## Turnierräume

7. Die Turnierräume umfassen die Spielsäle, die nächstgelegenen Toiletten und deren Zugang. Die Hotel-Lobby ist nicht mehr Teil der Turnierräume. Die Spieler dürfen während ihrer Partie die Turnierräume nicht verlassen, außer mit der ausdrücklichen Erlaubnis eines Schiedsrichters. In diesem Fall wird der Spieler immer von einem Schiedsrichter oder einem Mitglied der Organisation begleitet.

8. Gelöscht.

9. Ein Spieler darf sein Mobil-Telefon mit in die Spielräume nehmen, er muss dieses jedoch vor Spielbeginn aus schalten. Der Spieler kann das Gerät neben dem Schachbrett legen oder es wegräumen. Wenn ein Spieler während seiner Partie sein Mobil-Telefon verwendet oder sollte von diesem ein Geräusch ausgehen, verliert der Spieler die Partie, der Schiedsrichter entscheidet über das Resultat des Gegners.

10. Spieler dürfen keine schachbezogene Hilfsmittel mit in die Turnierräume nehmen.

11. Die Teilnehmer sind angehalten stille zu wahren. Jede unnötige Form der Kommunikation, mündlich oder nicht mündlich, ist verboten.

12. Bei Zuwiderhandlung werden Teilnehmer nach den FIDE Regeln geahndet. 


## Spielsäle

13. Gelöscht.

14. Ein Teilnehmer der seine Partie beendet hat wird als Zuschauer angesehen. Wie im Abschnitt Covid19-Maßnahmen angegeben, muss er sofort den Wartebereich betreten oder die Räumlichkeiten verlassen.

## Essen und Trinken

15. Alkohol, in jeglicher Form, ist in den Turnierräumen verboten.

16. Da seitens der Veranstalter keine Getränke angeboten werden, dürfen Spieler ihre eigenen Getränke in den Spielsaal mitbringen.

17. Spieler dürfen im Spielsaal einen Snack zu sich nehmen, nur hinter dem Spielbrett und nur wenn sie dran sind (um den Gegner niemals zu stören).

18. Nach beenden der Partie sind die Spieler angehalten ihren Spieltisch abfallfrei und sauber zu hinterlassen.

## Mitteilungen

19. Alle offizielle Mitteilungen der Veranstalter (z.B. Zusammenstellung der Kommissionen, Spielplan, Paarungen, Tabellen, …) werden nur über die Turnierwebsite veröffentlicht. Zusätzlich und unverbindlich, kann der Veranstalter auch andere Medien nutzen wie E-Mail, SMS, die Chessout-App (nur Android), … .

## Aufteilungssystem

20. Die von der FIDE vorgeschlagenAufteilungssysteme werden verwendet.
Siehe [das FIDE-Handbuch C02](https://handbook.fide.com/files/handbook/C02Standards.pdf) Art. 13.16.2. für Round-Robin-Gruppen und Art. 13.16.4 für Schweizer Gruppen.

## Paarungen

21. Die Paarungen werden mit der neusten Version von Swar festgelegt.

## Elo-Auswertungen

22. Die Ergebnisse aller Partien aller Gruppen werden sowohl für die Wertung der FIDE Elo als auch für die Wertung der belgischen Elo eingereicht.eingereicht.

## Anzahl der Runden und Tempo

23. Die Anzahl der Runden beträgt 7. Die Altersgruppen von -8 und -10 spielen nur samstags (4 Runden: um 9.30 Uhr, 12.30 Uhr, 15 Uhr, 17.30 Uhr) und sonntags (3 Runden um 9.30 Uhr, 12 Uhr, 14.30 Uhr). Die anderen Altersgruppen spielen 2 Runden am Donnerstag, Freitag und Samstag (um 9.30 Uhr und 15.00 Uhr) und 1 Runde am Sonntag (um 9.30 Uhr). Es gibt keine Eröffnungsfeier vor der ersten Runde und keine Abschlussfeier nach der letzten Runde.

24. Das Spieltempo ist wie folgt eingestellt:

 - für die Altersgruppen U12 - U20:  90 Minuten für das ganze Spiel + 30 Sekunden Zusatz pro Zug ab dem 1. Zug. Dieses Spieltempo hat zur Folge, dass alle Spieler alle Züge aufschreiben müssen, auch wenn die Restzeit unter 5 Minuten liegt!
 - für die Kategorien U8 - U10:  45 Minuten für das ganze Spiel + 15 Sekunden Zusatz pro Zug ab dem 1. Zug. Sobald ein Spieler zum ersten Mal weniger als 5 Minuten auf der Uhr hat, muss er nicht mehr aufschreiben


## Abwesenheit der Spieler

25. Erscheint ein Spieler von die Altersgruppen U12 – U20 mit mehr als 60 Minuten Verspätung am Schachbrett oder erscheint ein Spieler von die Altersgruppen U8 – U10 mit mehr als 45 Minuten Verspätung am Schachbrett beide Male relativ zu die zuvor angekündigte Startzeit, verliert er die Partie. Ist ein Spieler ohne berechtigten Grund abwesend oder benachrichtigt er den Veranstalter nicht rechtzeitig vor der nächsten Paarung wird er vom Turnier ausgeschlossen. Falls ein Spieler aus einem berechtigten Grund abwesend ist und die Turnierleitung informiert, wird er für die nächste(n) Runde(n) nicht gepaart. Falls die nächsten Paarungen schon veröffentlicht wurden ist das Spiel durch Forfait verloren, der Spieler wird aber bei der nächsten Runden für die er berichtet hat, anwesend zu sein, wieder aufgenommen.

26. Um eine Abwesenheit zu melden, ist die Turnierleitung (Luc Cornet  unter der Rufnummer +32/474/99.52.74) zu benachrichtigen. Hinterlassen sie immer eine Nachricht mit Ihrer Name und Rufnummer.

## Klagen

27. Jede Gruppe hat einen oder mehrere Schiedsrichter. Bei einem Problem am Brett, kann der Spieler die Uhr stoppen und einen Schiedsrichter rufen. Dieser trifft dann eine Entscheidung.

28. Wenn ein Spieler nicht mit dieser Entscheidung einverstanden ist, dann kann er dagegen sofort mündlich beim Hauptschiedsrichter Klage erheben. Der Hauptschiedsrichter wird sich dann die Darstellung des Spielers und des Schiedsrichters anhören und danach die Entscheidung des Schiedsrichters bestätigen oder annullieren. Anschließend wird die Partie fortgesetzt (wenn nötig).

29. Wenn ein Spieler auch mit der Entscheidung des Hauptschiedsrichters nicht einverstanden ist, kann er spätestens eine Viertelstunde nach Ende seiner Partie in die Berufung gehen. Er muss seine Klage schriftlich motivieren und sie dem Hauptschiedsrichter übergeben, mit einer Kaution von 50 EUR. Der Hauptschiedsrichter wird dann die Berufungskommission zusammenrufen, diesee wird eine endgültige Entscheidung treffen.

Gegen die Entscheidung der Berufungskommission ist es nicht möglich, Beschwerde einzureichen. Die Kommission entscheidet auch – auf Grundlage der Korrektheit der Motivierung der Klage – ob die Kaution dem Kläger völlständig oder teilweise erstattet wird.

## Selektionen

30. Wie in seinen Bestimmungen festgelegt, wird der KSB, sofern es noch Europameisterschaften und Weltmeisterschaften für Jugendliche gibt vor dem Start der nächsten belgischen Jugendmeisterschaft, die Resultate dieser Belgischen Schach-Jugendlandesmeisterschaft berücksichtigen bei der Auswahl der Teilnehmer für die Europa- und die Weltmeisterschaften.

31. Sofern vor Beginn der nächsten belgischen Meisterschaft keine belgische Jugendmeisterschaft stattfindet,  ist der Meister oder die Meisterin mit der höchsten ELO-Wertung aus allen Altersgruppen automatisch für die Teilnahme in der Expertengruppe der nächsten belgischen Landesmeisterschaft nominiert, vorausgesetzt er die Kriterien erfüllt.

## Sanktionen und Disziplinarmaßnahmen

32. Artikel 14 der Wettbewerbsordnung der KSB und Artikel 14 der Statuten der KSB sind jederzeit anwendbar.
`,
      },
    }
  },

  head: {
    title: 'Torunament rules',
    titleTemplate: '%s - BYCCO',
    link: [
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900',
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css?family=Material+Icons',
      },
      {
        rel: 'stylesheet',
        href:
          'https://cdn.jsdelivr.net/npm/@mdi/font@latest/css/materialdesignicons.min.css',
      },
      { rel: 'favicon', href: 'favicon.ico' },
    ],
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'home', name: 'description', content: 'Meta description' },
    ],
    script: [
      {
        src: 'https://apis.google.com/js/platform.js',
        async: true,
        defer: true,
      },
    ],
  },
}
</script>
