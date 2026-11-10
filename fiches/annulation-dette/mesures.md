# Mesures — annulation-dette

Relevé automatique (`outils/dossier.py`). Durées en temps réel, de l'horloge de la session. Jetons et appels d'outils : tels que renvoyés par l'outil de lancement des agents.

## Par phase

| Phase | Début | Fin | Durée | Passages | Agents lancés | Jetons | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Cadrage | 2026-11-10T20:31:37 | 2026-11-10T20:33:04 | 1 min 27 s | 1 | 7 | 142650 | 40 questions proposées ; regroupement soumis au fondateur |
| 1-bis. Cadrage | 2026-11-10T20:59:01 | 2026-11-10T21:05:58 | 6 min 57 s | 1 | 1 | 121320 | bibliothèque commune, 7 questions |
| 3. Vérification | 2026-11-10T21:05:59 | 2026-11-10T21:09:29 | 3 min 30 s | 1 | 3 | 121529 | vérification de la bibliothèque |
| 2. Contributions indépendantes | 2026-11-10T21:09:29 | 2026-11-10T21:16:23 | 6 min 54 s | 1 | 7 | 574670 |  |
| 3-bis. Vérification | 2026-11-10T21:16:23 | — | — | 1 | 5 | 222135 |  |

## Par agent

| Phase | Agent | Jetons | Appels d'outils | Durée |
| --- | --- | --- | --- | --- |
| 1 | expert-extreme-gauche | 18425 | 3 | 0 min 15 s |
| 1 | expert-extreme-droite | 18377 | 3 | 0 min 18 s |
| 1 | expert-gauche-radicale | 20622 | 4 | 0 min 22 s |
| 1 | expert-sociaux-democrates | 20991 | 4 | 0 min 23 s |
| 1 | expert-droite | 21614 | 4 | 0 min 26 s |
| 1 | expert-centre | 21439 | 5 | 0 min 27 s |
| 1 | expert-ecologistes | 21182 | 5 | 0 min 27 s |
| 1-bis | bibliothecaire | 121320 | 51 | 6 min 33 s |
| 3 | verificateur-bibliotheque-1 | 38503 | 11 | 1 min 05 s |
| 3 | verificateur-bibliotheque-2 | 48842 | 16 | 2 min 02 s |
| 3 | verificateur-bibliotheque-verdicts | 34184 | 5 | 0 min 53 s |
| 2 | expert-extreme-gauche | 67087 | 17 | 2 min 29 s |
| 2 | expert-extreme-droite | 78478 | 22 | 2 min 30 s |
| 2 | expert-droite | 70923 | 19 | 2 min 36 s |
| 2 | expert-centre | 66106 | 16 | 2 min 44 s |
| 2 | expert-sociaux-democrates | 71291 | 22 | 2 min 50 s |
| 2 | expert-ecologistes | 111515 | 42 | 4 min 50 s |
| 2 | expert-gauche-radicale | 109270 | 29 | 6 min 03 s |
| 3-bis | verificateur-passage1-5 | 23686 | 6 | 0 min 31 s |
| 3-bis | verificateur-passage1-4 | 49181 | 15 | 1 min 29 s |
| 3-bis | verificateur-passage1-2 | 47020 | 18 | 2 min 01 s |
| 3-bis | verificateur-passage1-1 | 49736 | 17 | 2 min 03 s |
| 3-bis | verificateur-passage1-3 | 52512 | 21 | 2 min 12 s |
