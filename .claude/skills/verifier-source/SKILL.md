---
name: verifier-source
description: Comment ouvrir une source web pour Polisible et en garder seulement l'utile (outil outils/ouvrir.py, statuts, extrait court). Pour les experts et le vérificateur.
---

# Ouvrir et vérifier une source

**Ouvrir.** `python3 outils/ouvrir.py "<adresse>" --cherche "mot1|mot2" [--fenetre 300] [--max 6]`
L'outil renvoie statut, adresse finale, titre, date des métadonnées, puis les seuls passages autour des mots cherchés (expression régulière). Cherche des mots précis (numéro d'article, chiffre, nom) ; n'affiche pas la page entière. **C'est le seul outil d'ouverture**, le même pour tous les agents (équité d'accès). `WebSearch` sert à trouver les adresses ; un résumé de recherche n'est jamais une source.

**Une source n'est citée que si tu l'as ouverte pendant ce travail** et que l'extrait y figure. Jamais de mémoire. Une adresse trouvée par la recherche mais non ouverte n'est pas une source.

**Inaccessible.** Certains sites refusent les robots (Légifrance, Banque de France, EUR-Lex renvoie une page de contrôle). Ne contourne jamais un blocage. Réessaie une fois, puis cherche le même texte à une autre adresse (autre version linguistique, PDF, site du Conseil constitutionnel, de l'Assemblée, de la BCE, du Sénat…). Sinon : expert → `sources_demandees` ; vérificateur → `inaccessible`.

**Contrôles du vérificateur**, pour chaque source :
1. Bon document : titre, auteur, date correspondent.
2. L'extrait ou le chiffre y figure (recherche d'un fragment exact).
3. Il dit la même chose que l'affirmation : même périmètre, même année, même unité.
4. Existe-t-il une version plus récente de la donnée ? Si oui, le noter.
Statut : `conforme`, `non-conforme` (dire l'écart) ou `inaccessible`.

**Extraits** : une phrase au plus, copiée exactement. On garde le lien et l'extrait utile, jamais le texte d'un article (dépôt public).

**Une page n'est ouverte qu'une fois** : le lot indique toutes les affirmations qui citent la source ; vérifie-les toutes dans la même ouverture (plusieurs mots dans `--cherche`).
