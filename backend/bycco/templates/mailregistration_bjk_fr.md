## Confirmation d'inscription CBJ 2025

### Détails du participant

- {{ first_name }} {{ last_name }}
- Année de naissance : {{ birthyear }}
- Matricule : {{ idbel }}
- Numéro de club : {{ idclub }}
- Nationalité FIDE : {{ nationalityfide }}
- Peut devenir champion de Belgique : {{ ['Oui', 'Non', 'à confirmer'][natstatus] }}
- Sexe : {{ gender }}
- Catégorie : {{ category }}
- Remarques: {{ (remarks if remarks else "Pas de remarques") | replace("\n", "<br>")}}


Cordialement.

_L'équipe Bycco_
