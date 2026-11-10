# Mesures — annulation-dette

Relevé automatique (`outils/dossier.py`). Durées en temps réel, de l'horloge de la session. Jetons et appels d'outils : tels que renvoyés par l'outil de lancement des agents.

## Par phase

| Phase | Début | Fin | Durée | Passages | Agents lancés | Jetons | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1-bis. Cadrage | 2026-11-10T20:03:44 | 2026-11-10T20:07:34 | 3 min 50 s | 1 | 1 | 126533 | bibliothèque commune |
| 3. Vérification | 2026-11-10T20:07:34 | 2026-11-10T20:09:47 | 2 min 13 s | 1 | 2 | 95701 | vérification de la bibliothèque commune |
| 2. Contributions indépendantes | 2026-11-10T20:09:47 | 2026-11-10T20:11:41 | 1 min 54 s | 1 | 7 | 211044 |  |
| 3-bis. Vérification | 2026-11-10T20:11:42 | 2026-11-10T20:14:34 | 2 min 52 s | 1 | 0 | — |  |
| 4. Confrontation | 2026-11-10T20:14:34 | 2026-11-10T20:16:13 | 1 min 39 s | 1 | 7 | 231410 | un passage, 7 experts (premier passage : tous) |
| 3-ter. Vérification | 2026-11-10T20:16:13 | — | — | 1 | 0 | — | second passage : affirmations de la confrontation |

## Par agent

| Phase | Agent | Jetons | Appels d'outils | Durée |
| --- | --- | --- | --- | --- |
| 1-bis | bibliothecaire | 126533 | 30 | 3 min 36 s |
| 3 | verificateur-bibliotheque | 46507 | 15 | 2 min 00 s |
| 2 | expert-sociaux-democrates | 24812 | 7 | 0 min 40 s |
| 2 | expert-ecologistes | 27916 | 8 | 0 min 44 s |
| 2 | expert-centre | 26293 | 7 | 0 min 45 s |
| 2 | expert-droite | 28670 | 9 | 0 min 53 s |
| 2 | expert-extreme-gauche | 31190 | 9 | 0 min 53 s |
| 2 | expert-extreme-droite | 31901 | 9 | 1 min 02 s |
| 2 | expert-gauche-radicale | 40262 | 10 | 1 min 20 s |
| 3 | verificateur-passage1 | 49194 | 18 | 2 min 32 s |
| 4 | expert-ecologistes | 31068 | 3 | 0 min 09 s |
| 4 | expert-sociaux-democrates | 30779 | 3 | 0 min 09 s |
| 4 | expert-extreme-gauche | 31130 | 3 | 0 min 12 s |
| 4 | expert-gauche-radicale | 31465 | 3 | 0 min 14 s |
| 4 | expert-extreme-droite | 32216 | 3 | 0 min 20 s |
| 4 | expert-droite | 32879 | 3 | 0 min 24 s |
| 4 | expert-centre | 41873 | 10 | 1 min 04 s |
