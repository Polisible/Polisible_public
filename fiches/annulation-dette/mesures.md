# Mesures — annulation-dette

Relevé automatique (`outils/dossier.py`). Durées en temps réel, de l'horloge de la session. Jetons et appels d'outils : tels que renvoyés par l'outil de lancement des agents.

## Par phase

| Phase | Début | Fin | Durée | Passages | Agents lancés | Jetons | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1-bis. Cadrage | 2026-11-10T20:03:44 | 2026-11-10T20:07:34 | 3 min 50 s | 1 | 1 | 126533 | bibliothèque commune |
| 3. Vérification | 2026-11-10T20:07:34 | 2026-11-10T20:09:47 | 2 min 13 s | 1 | 1 | 46507 | vérification de la bibliothèque commune |
| 2. Contributions indépendantes | 2026-11-10T20:09:47 | — | — | 1 | 0 | — |  |

## Par agent

| Phase | Agent | Jetons | Appels d'outils | Durée |
| --- | --- | --- | --- | --- |
| 1-bis | bibliothecaire | 126533 | 30 | 3 min 36 s |
| 3 | verificateur-bibliotheque | 46507 | 15 | 2 min 00 s |
