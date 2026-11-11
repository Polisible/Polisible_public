# Comparaison des deux essais — annulation-dette, Q1

Même question, même contexte, un seul passage de confrontation dans les deux cas. L'essai 1 est archivé dans `essai-1/`, l'essai 2 dans `essai-2/`.

| | Essai 1 | Essai 2 |
| --- | --- | --- |
| Règles | version minimale | bibliothèque commune, outil d'ouverture unique, affirmations sur le fond, raisonnement obligatoire, « sans position » |
| Lancement des agents | agents génériques qui lisent leurs consignes | agents Polisible natifs |
| Durée (horloge de la session) | ≈ 16 min 30 s | ≈ 18 min |
| Lancements d'agents | 20 | 19 |
| Jetons (total des agents) | ≈ 1,95 million | ≈ 0,76 million (− 61 %) |
| Coût d'un expert, contributions | 90 000 à 135 000 | 25 000 à 40 000 |
| Arguments actifs (pour / contre / nuancés) | 15 (2 / 7 / 6) | 7 (1 / 5 / 1) |
| Familles déclarées « sans position » | 0 (mais 4 arguments sans porteur de la famille) | 3 (extrême gauche, sociaux-démocrates, écologistes) |
| Affirmations | 39 (27 Vrai, 12 Plutôt vrai) | 16 (13 Vrai, 3 Plutôt vrai) |
| Affirmations qui rapportent une déclaration | ≈ la moitié, non signalées | 2, signalées (`declaration: true`) |
| Sources (niveau 1) | 20 (7) | 17 (8), dont 4 inaccessibles (Banque de France, AFT) |
| Objections et contre-arguments en confrontation | 4 contre-arguments, 3 corrections, 1 retrait | 1 contre-argument, 2 corrections |
| Manques signalés par le rédacteur | 12 | 17 |

## Ce qui s'est amélioré

- **Lisibilité du fond.** La fiche sépare « ce qui est établi » (articles 123 et 130, arrêts de 2015 et 2018, achats sur le marché secondaire) et « ce qu'aucun texte ni arrêt ne tranche » (l'annulation elle-même). Le « tout le monde dit vrai » de l'essai 1 disparaît.
- **Honnêteté sur les positions.** Les familles sans position publique le disent, au lieu de fabriquer un argument d'autorité.
- **Coût** divisé par 2,5, grâce aux agents natifs et à la bibliothèque commune.
- **Une vraie erreur trouvée** : la déclaration de Christine Lagarde date du 10 septembre 2026 (conférence de presse), pas du 11 (article de presse).

## Ce qui s'est dégradé

- **Recherche trop courte.** Les experts natifs font 7 à 10 appels d'outils contre 13 à 36. L'expert des sociaux-démocrates ne retrouve pas la tribune de 2020 ni l'entretien d'Olivier Faure trouvés à l'essai 1. Une partie des « sans position » est peut-être une recherche insuffisante plutôt qu'une absence réelle.
- **Confrontation passive** : un seul contre-argument ; la plupart des experts ne rouvrent aucune source.
- **Porteurs hors famille** : faute de texte de parti, le centre, la droite et l'extrême droite attribuent leur argument à Christine Lagarde ou à la Fondation IFRAP. Question ouverte pour le fondateur.
- **Chiffre clé manquant** : la part de dette détenue par la Banque de France (pages officielles refusées aux robots).
