# Mesures — annulation-dette

Relevé automatique (`outils/dossier.py`). Durées en temps réel, de l'horloge de la session. Jetons et appels d'outils : tels que renvoyés par l'outil de lancement des agents.

## Par phase

| Phase | Début | Fin | Durée | Passages | Agents lancés | Jetons | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Cadrage | 2026-11-10T20:31:37 | 2026-11-10T20:33:04 | 1 min 27 s | 1 | 7 | 142650 | 40 questions proposées ; regroupement soumis au fondateur |
| 1-bis. Cadrage | 2026-11-10T20:59:01 | 2026-11-10T21:05:58 | 6 min 57 s | 1 | 1 | 121320 | bibliothèque commune, 7 questions |
| 3. Vérification | 2026-11-10T21:05:59 | 2026-11-10T21:09:29 | 3 min 30 s | 1 | 3 | 121529 | vérification de la bibliothèque |
| 2. Contributions indépendantes | 2026-11-10T21:09:29 | 2026-11-10T21:16:23 | 6 min 54 s | 1 | 7 | 574670 |  |
| 3-bis. Vérification | 2026-11-10T21:16:23 | 2026-11-10T21:23:28 | 7 min 05 s | 1 | 7 | 296601 |  |
| 4. Confrontation | 2026-11-10T21:23:28 | 2026-11-11T00:52:16 | 208 min 48 s | 1 | 19 | 808525 | passages 1 et 2 de confrontation ; inclut l'interruption par la limite d'usage de l'abonnement (environ 21 h 30 → 0 h 51 UTC), donc la durée n'est pas une durée de travail |
| 3-ter. Vérification | 2026-11-10T21:25:20 | — | — | 1 | 1 | 22373 | objection O1 ; fin non relevée par le coordinateur (agent : 33 s) |
| 4-bis. Confrontation | 2026-11-11T00:52:32 | 2026-11-11T00:54:24 | 1 min 52 s | 1 | 0 | — | passage 3 de confrontation, ciblé (5 experts) |
| 5. Stabilisation | 2026-11-11T00:54:37 | 2026-11-11T00:54:37 | 0 min 00 s | 1 | 0 | — | plafond de 3 passages atteint, condition 1 non remplie |
| 6. Rédaction | 2026-11-11T00:54:38 | 2026-11-11T01:06:57 | 12 min 19 s | 1 | 1 | 231825 | 38 manques signalés ; 3 corrections du rédacteur appliquées mot pour mot |
| 6-bis. Rédaction | 2026-11-11T09:36:47 | — | — | 1 | 8 | 422818 | normalisation au format de fiche |

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
| 3-bis | verificateur-passage1-verdicts | 72096 | 17 | 3 min 25 s |
| 3-bis | verificateur-sources-ajoutees | 2370 | 3 | 0 min 31 s |
| 4 | expert-droite | 40309 | 4 | 0 min 14 s |
| 4 | expert-sociaux-democrates | 41695 | 6 | 0 min 17 s |
| 4 | expert-extreme-gauche | 47788 | 6 | 0 min 19 s |
| 4 | expert-extreme-droite | 45745 | 6 | 0 min 21 s |
| 4 | expert-ecologistes | 47726 | 7 | 0 min 23 s |
| 4 | expert-centre | 50096 | 8 | 0 min 29 s |
| 4 | expert-gauche-radicale | 72857 | 14 | 1 min 06 s |
| 3-ter | verificateur-objection-O1 | 22373 | 4 | 0 min 33 s |
| 4 | expert-extreme-gauche | 54778 | 4 | 0 min 25 s |
| 4 | expert-ecologistes | 55040 | 4 | 0 min 26 s |
| 4 | expert-centre | — | — | — |
| 4 | expert-droite | — | — | — |
| 4 | expert-extreme-droite | — | — | — |
| 4 | expert-gauche-radicale | — | — | — |
| 4 | expert-sociaux-democrates | — | — | — |
| 4 | expert-droite | 65772 | 4 | 0 min 22 s |
| 4 | expert-sociaux-democrates | 66424 | 4 | 0 min 26 s |
| 4 | expert-extreme-gauche | 67292 | 5 | 0 min 30 s |
| 4 | expert-centre | 74478 | 5 | 0 min 56 s |
| 4 | expert-gauche-radicale | 78525 | 9 | 1 min 24 s |
| 6 | redacteur | 231825 | 20 | 11 min 38 s |
| 6-bis | expert-extreme-droite | 42056 | 7 | 0 min 41 s |
| 6-bis | expert-droite | 47190 | 9 | 0 min 43 s |
| 6-bis | bibliothecaire | 49393 | 12 | 0 min 43 s |
| 6-bis | expert-extreme-gauche | 46012 | 8 | 0 min 55 s |
| 6-bis | expert-ecologistes | 48548 | 9 | 0 min 59 s |
| 6-bis | expert-sociaux-democrates | 53395 | 12 | 1 min 10 s |
| 6-bis | expert-centre | 62379 | 14 | 1 min 24 s |
| 6-bis | expert-gauche-radicale | 73845 | 15 | 2 min 09 s |
