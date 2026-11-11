# Polisible — Format d'une fiche

Ce document fixe chaque champ d'une fiche : ce qu'il contient, sous quelle forme, et comment il s'affiche. La fiche n'est pas écrite à la main : `outils/rendre_fiche.py` l'assemble à partir du dossier et des textes du rédacteur, en suivant ce document. `outils/dossier.py` refuse tout dépôt qui ne le respecte pas.

Principe : **une seule façon d'écrire chaque chose**. Si un cas n'est pas prévu ici, l'agent ne l'invente pas : il le signale dans `incertitudes`, et le format est complété.

## 1. Valeurs communes

| Élément | Forme dans le dossier | Affichage |
| --- | --- | --- |
| Date complète | `AAAA-MM-JJ` | « 24 août 2026 » |
| Date au mois | `AAAA-MM` (jour inconnu) | « août 2026 » |
| Date à l'année | `AAAA` (mois inconnu) | « 2026 » |
| Identifiants | `Q`, `A`, `F`, `S`, `V`, `O` suivis d'un nombre | entre crochets : « [F12] », « [S3, S7] » |
| Parti | sigle de la liste fermée (§ 2) | sigle seul, en capitales comme dans la liste |
| Position | `oui`, `non`, `nuance` (réponse à la **question**, jamais à la mesure) | « Oui », « Non », « Nuancé » |
| Type | `fait`, `estimation`, `valeur` | « Fait », « Estimation », « Valeur » |

Une date inconnue n'est jamais devinée : on écrit la précision connue (mois ou année) et, si rien n'est connu, la source ne peut pas porter un argument daté.

## 2. Partis (liste fermée)

| Sigle | Parti | Famille |
| --- | --- | --- |
| LO | Lutte ouvrière | Extrême gauche |
| NPA | Nouveau Parti anticapitaliste (toutes branches) | Extrême gauche |
| LFI | La France insoumise | Gauche radicale |
| PCF | Parti communiste français | Gauche radicale |
| PS | Parti socialiste | Sociaux-démocrates |
| PP | Place publique | Sociaux-démocrates |
| LE | Les Écologistes | Écologistes |
| RE | Renaissance | Centre |
| MoDem | Mouvement démocrate | Centre |
| HOR | Horizons | Centre |
| UDI | Union des démocrates et indépendants | Centre |
| LR | Les Républicains | Droite |
| RN | Rassemblement national | Extrême droite |
| UDR | Union des droites pour la République | Extrême droite |
| REC | Reconquête | Extrême droite |

Un parti absent de la liste ne peut pas porter d'argument tant que le fondateur ne l'a pas ajouté. Un groupe parlementaire, un courant ou une fondation n'est jamais un parti : on indique le parti dont il relève, et le groupe ou le courant va dans la fonction.

## 3. Porteur (« Porté par »)

Utilisé par les arguments, les valeurs et les positions des institutions.

| Champ | Contenu | Obligatoire |
| --- | --- | --- |
| `personne` | Prénom Nom, tel qu'écrit dans la source | non (vide si c'est le parti ou un groupe qui s'exprime) |
| `fonction` | Fonction **au moment de la déclaration**, sans majuscule initiale, sans abréviation : « députée européenne », « président du groupe LFI à l'Assemblée nationale », « candidat à l'élection présidentielle de 2027 », « courant Tendance CLAIRE » | oui si `personne` est renseigné |
| `parti` | sigle (§ 2) | oui, sauf pour une institution |
| `institution` | pour une position d'institution seulement (§ 8) | oui pour une institution |
| `date` | date de la déclaration ou du texte (§ 1) | oui |
| `source` | un identifiant `S…` qui établit **à la fois** la déclaration et l'appartenance au parti, ou un second identifiant `appartenance: S…` qui établit l'appartenance | oui |

Affichage, toujours dans cet ordre :
- personne : **Prénom Nom** (fonction, SIGLE), date [S…]
- parti seul : **SIGLE**, date [S…]
- institution : **Prénom Nom** (fonction, Institution), date [S…]

Jamais le lieu, jamais le média, jamais le groupe à la place du parti. Si l'appartenance n'est établie par aucune source, le porteur est refusé.

## 4. Question

| Champ | Contenu | Limite |
| --- | --- | --- |
| `id`, `numero` | `Q…` ; numéro d'ordre dans la fiche (1, 2, 3…) | |
| `enonce` | question fermée, terminée par « ? » | 35 mots |
| `type` | § 1 | |
| `reponse_rapide` | écrite par le rédacteur : l'état de la question, sans verdict global ; cite ses identifiants | 80 mots |

Affichage : « ## Question 3 — Énoncé ? » puis « Type : Estimation [Q43] », puis la réponse rapide.

## 5. Argument

| Champ | Contenu | Limite |
| --- | --- | --- |
| `position` | `oui`, `non`, `nuance` (§ 1) | |
| `enonce` | la thèse, à l'indicatif, sans qualificatif ni verbe d'opinion (« X affirme que… » est interdit) | 2 phrases, 50 mots |
| `raisonnement` | pourquoi les affirmations mènent à la thèse ; cite les `F…` | 3 phrases, 70 mots |
| `porte_par` | un ou plusieurs porteurs (§ 3) | |
| `affirmations` | liste de `F…` | au moins 1 |
| `repond_a` | identifiant de l'argument auquel celui-ci répond, sinon vide | |

Affichage en **fil** : les arguments qui ne répondent à rien sont listés par position (Oui, puis Non, puis Nuancé) ; chaque réponse est placée sous l'argument visé, en retrait, avec la mention « Réponse » à la place de la position, et ainsi de suite pour les réponses aux réponses.

```
▸ [A20] Oui — Énoncé.
  Raisonnement.
  Porté par : Jean-Luc Mélenchon (président du groupe LFI à l'Assemblée nationale, LFI), juin 2022 [S40]
  Appuis : [F45] Fait — Vrai · [F50] Fait — Vrai
  ↳ [A37] Réponse — Énoncé.
     Porté par : …
     ↳ [A20 corrigé] …
```

Un argument corrigé affiche sa dernière formulation et la mention « (corrigé) » ; l'ancienne formulation reste dans le dossier et le journal. Un argument retiré n'apparaît pas.

## 6. Affirmation

| Champ | Contenu | Limite |
| --- | --- | --- |
| `enonce` | une seule affirmation, un seul type, sur le fond (« X a dit que… » seulement avec `declaration: true`) | 1 phrase, 40 mots |
| `type` | § 1 | |
| `verdict` | une étiquette exacte de l'échelle du type ; aucune pour une valeur | |
| `explication` | une à trois phrases ; pour une estimation, qui l'a produite (institution, date, méthode) | 3 phrases, 70 mots |
| `sources` | `{source: S…, extrait: "…"}`, extrait copié mot pour mot | extrait : 1 phrase, 320 caractères |

Affichage, à la première apparition dans la fiche : « [F12] Énoncé — Fait — **Vrai** — Explication. Sources : [S3] « extrait ». » Ensuite : « [F12] Fait — Vrai (voir question 1) ».

## 7. Source

| Champ | Contenu |
| --- | --- |
| `titre` | titre exact du document, sans guillemets ajoutés |
| `auteur` | institution, organe de presse ou parti qui publie ; pour une personne : Prénom Nom |
| `date` | date de publication (§ 1) |
| `adresse` | adresse ouverte |
| `niveau` | 1 à 4 |
| `statut` | `conforme`, `non-conforme`, `inaccessible` |

Affichage dans le tableau final : `| S3 | Titre | Auteur | 11 décembre 2018 | 1 | Conforme | adresse |`.

## 8. Positions des institutions

Affirmations `declaration: true` déposées par le bibliothécaire, avec un porteur dont `institution` est pris dans cette liste : BCE, Banque de France, Cour des comptes, Haut Conseil des finances publiques, Conseil d'État, Conseil constitutionnel, Cour de justice de l'Union européenne, Commission européenne, Insee, Gouvernement. Affichage : sous-partie « Ce qu'en disent les institutions » de chaque question, une ligne par position : porteur (§ 3), puis l'énoncé et le verdict.

## 9. Familles sans position

`{question, parti, lieux_consultes}` ; une ligne par question : « Aucune position publique trouvée pour : LR, LE (programme, site, dirigeants, Parlement consultés). »

## 10. Valeur

| Champ | Contenu | Limite |
| --- | --- | --- |
| `question` | `Q…` | |
| `enonce` | commence par « Priorité à » ; aucun verdict | 1 phrase, 30 mots |
| `porte_par` | porteur (§ 3), même règle que les arguments | |

Affichage : section « Les valeurs en jeu », par question : « Priorité à … — **SIGLE**, date [S…] ».

## 11. Textes du rédacteur (`dossier/redaction.yaml`)

Le rédacteur n'écrit que ces textes ; tout le reste est assemblé par le programme.

| Champ | Contenu | Limite |
| --- | --- | --- |
| `lecture_rapide` | l'essentiel de la fiche : ce qui est établi, ce qui est disputé, qui défend quoi ; cite ses identifiants | 250 mots |
| `contexte` | ce qui a lancé le débat, daté | 150 mots |
| `definitions` | `{terme, definition, sources: [F… ou S…]}` ; une définition sans source n'est pas écrite | 40 mots chacune |
| `chiffres_cles` | `{libelle, affirmations: [F…]}` : un chiffre daté, repris d'une affirmation vérifiée | 20 mots chacun |
| `reponses_rapides` | `{question: Q…, texte}` (§ 4) | 80 mots |
| `valeurs_synthese` | `{question: Q…, texte}` : ce qui oppose les priorités, sans nommer de famille | 60 mots |
| `manques` | `{vise, nature, besoin}` | |

Style : celui des consignes communes (phrases courtes, aucun qualificatif, mêmes verbes pour tous, chaque chiffre daté). Le programme refuse un texte trop long ou sans identifiant.

## 12. Ordre des parties

1. Titre, thème, sujet, date, version, mention « rédigée avec l'assistance d'IA, non vérifiée » tant que le fondateur n'a pas validé.
2. Lecture rapide.
3. Contexte et définitions.
4. Chiffres clés.
5. Les questions, dans l'ordre des numéros : réponse de la commission (avec sa certitude), « Pourquoi » (thèses classées : tient, tient en partie, ne tient pas), « Qui défend quoi » (tableau), « En détail » (examen de chaque thèse, contre-examen, contestations), puis le fil des arguments, « Ce qu'en disent les institutions » et les familles sans position (voir `docs/commission.md` § 8).
6. Les valeurs en jeu.
7. Pour aller plus loin : les sources de niveau 1 et 2 citées.
8. Informations sur la fiche : date, version, nombre de passages de confrontation, condition d'arrêt, lien vers le journal et le dossier, tableau des sources, manques signalés.
