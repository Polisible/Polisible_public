# Mesures — annulation-dette

Relevé automatique (`outils/dossier.py`). Durées en temps réel, de l'horloge de la session. Jetons et appels d'outils : tels que renvoyés par l'outil de lancement des agents.

## Par phase

| Phase | Début | Fin | Durée | Passages | Agents lancés | Jetons | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Cadrage | 2026-11-10T18:58:39 | 2026-11-10T18:58:39 | 0 min 00 s | 1 | 0 | — | question imposée par le fondateur, pas de cadrage par les experts |
| 2. Contributions indépendantes | 2026-11-10T18:58:39 | 2026-11-10T19:03:48 | 5 min 09 s | 1 | 7 | 756686 |  |
| 3. Vérification | 2026-11-10T19:03:48 | 2026-11-10T19:07:57 | 4 min 09 s | 1 | 4 | 357290 |  |
| 4. Confrontation | 2026-11-10T19:07:57 | 2026-11-10T19:09:56 | 1 min 59 s | 1 | 7 | 633617 | un seul passage, fixé par le fondateur |
| 3-bis. Vérification | 2026-11-10T19:09:56 | 2026-11-10T19:10:41 | 0 min 45 s | 1 | 1 | 73561 | second passage : 3 affirmations nouvelles de la confrontation |
| 5. Stabilisation | 2026-11-10T19:10:41 | 2026-11-10T19:10:42 | 0 min 01 s | 1 | 0 | — |  |
| 6. Rédaction | 2026-11-10T19:10:42 | 2026-11-10T19:15:10 | 4 min 28 s | 1 | 1 | 125048 | 12 manques signalés, non traités (voir bilan) |

## Par agent

| Phase | Agent | Jetons | Appels d'outils | Durée |
| --- | --- | --- | --- | --- |
| 2 | expert-centre | 90141 | 14 | 1 min 23 s |
| 2 | expert-droite | 95274 | 18 | 1 min 37 s |
| 2 | expert-gauche-radicale | 102013 | 13 | 1 min 37 s |
| 2 | expert-ecologistes | 102744 | 19 | 2 min 01 s |
| 2 | expert-extreme-droite | 103549 | 24 | 2 min 36 s |
| 2 | expert-extreme-gauche | 134597 | 33 | 3 min 33 s |
| 2 | expert-sociaux-democrates | 128368 | 36 | 3 min 57 s |
| 3 | verificateur-lot1 | 90105 | 14 | 1 min 02 s |
| 3 | verificateur-lot3 | 81252 | 11 | 1 min 02 s |
| 3 | verificateur-lot2 | 88824 | 19 | 1 min 28 s |
| 3 | verificateur-verdicts | 97109 | 9 | 2 min 02 s |
| 4 | expert-extreme-gauche | 87248 | 8 | 0 min 19 s |
| 4 | expert-extreme-droite | 88795 | 10 | 0 min 29 s |
| 4 | expert-droite | 88282 | 9 | 0 min 30 s |
| 4 | expert-sociaux-democrates | 89011 | 9 | 0 min 35 s |
| 4 | expert-centre | 90194 | 10 | 0 min 38 s |
| 4 | expert-gauche-radicale | 93212 | 13 | 0 min 53 s |
| 4 | expert-ecologistes | 96875 | 13 | 1 min 03 s |
| 3-bis | verificateur-passage2 | 73561 | 8 | 0 min 30 s |
| 6 | redacteur | 125048 | 8 | 3 min 52 s |

## Totaux du test (étape 1, une question, un passage de confrontation)

- Durée totale (horloge de la session) : 18:58:39 → 19:15:10, soit environ 16 min 30 s, agents lancés en parallèle.
- 20 lancements d'agents ; environ 1,95 million de jetons au total, dont environ 1,39 million pour les experts (sonnet) et 0,56 million pour le vérificateur et le rédacteur (opus). Ces chiffres comptent les jetons de contexte relus à chaque tour par chaque agent, pas seulement les jetons produits.
- Coût fixe par agent : environ 80 000 jetons même pour un expert qui n'a rien ajouté (lecture des consignes et des skills, contexte de base de l'agent générique).
- La session du coordinateur n'est pas comptée.
