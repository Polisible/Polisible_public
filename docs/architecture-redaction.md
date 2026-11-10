# Polisible — Système de rédaction agentique

Oct 30, 2026 · @Justin Colin

## Objet et principes

Ce document décrit comment plusieurs IA, chacune avec son rôle, construisent ensemble une fiche Polisible. Il remplace l'enchaînement manuel des consignes d'étape ; les consignes communes restent la base de chaque agent.

**Pourquoi ce système.** Le pilote manuel a montré trois limites : des fiches trop courtes, une structure trop technique pour un non-initié, et treize conversations à enchaîner à la main. Un vrai système agentique répond aux trois : chaque agent a ses consignes, son contexte et son objectif, et tous travaillent sur un même dossier.

**Six principes**

1. **Les experts ne négocient pas.** Chacun argumente et contre-argumente depuis le point de vue de sa famille politique. Le but n'est pas un compromis, mais que tous les arguments et contre-arguments aient été exprimés.
2. **Les sources décident des faits, pas l'accord des agents.** Huit IA d'accord peuvent avoir tort ensemble. Seul le vérificateur, à partir des sources, tranche une question de fait.
3. **Ceux qui argumentent n'écrivent pas la fiche.** Le rédacteur, sans camp, écrit à partir de ce qui a survécu à la vérification.
4. **Pas de nombre de tours fixé.** Le travail s'arrête quand il n'y a plus rien de nouveau à dire et plus aucune objection factuelle en suspens.
5. **Tout est tracé.** Chaque argument, objection et vérification est enregistré : on peut montrer comment une fiche a été construite. Le journal étant public, il ne contient que de courtes citations des sources (une phrase au plus), jamais le texte d'un article.
6. **La vérification humaine reste la dernière étape**, et rien n'est publié sans elle.

## Vue d'ensemble

Le système n'est pas une chaîne d'étapes, mais un dossier central que chaque agent enrichit selon son rôle. Chacun réagit à ce que les autres y ont ajouté, aussi longtemps qu'il reste quelque chose à dire ou à vérifier.

&#91;embedded content: architecture · 12 agents et le fondateur autour d'un dossier partagé\]

Le coordinateur organise sans argumenter, les experts argumentent sans trancher les faits, le vérificateur tranche les faits sans argumenter, et le rédacteur écrit sans rien ajouter. Le fondateur arbitre les blocages et vérifie avant publication.

## Les rôles

Douze agents et un humain. Chaque rôle a un objectif et des interdits : c'est la séparation des rôles qui garantit l'équité, pas la bonne volonté de chaque agent.

| Rôle | Objectif | Ce qu'il n'a pas le droit de faire |
| --- | --- | --- |
| **Coordinateur** | Découpe le thème en questions, tient le dossier, distribue le travail, détecte les boucles, décide quand le dossier est stable | Produire un argument, juger un fait, écrire la fiche |
| **Huit experts**, un par famille politique | Apporter la meilleure version des arguments de sa famille sur chaque question, avec leurs sources ; contester les arguments et les sources des autres ; défendre les siens ; proposer des questions manquantes | Inventer une source, modifier l'apport d'un autre, trancher un fait |
| **Vérificateur** | Ouvrir chaque source citée, lui donner un statut, trancher les objections factuelles, attribuer les verdicts aux affirmations | Argumenter, prendre parti, se prononcer sur une valeur |
| **Rédacteur** | Écrire la fiche dans la structure à quatre niveaux et à deux niveaux de lecture, à partir du dossier stabilisé | Ajouter une affirmation ou une source absente du dossier, changer un verdict |
| **Relecteur de symétrie** | Vérifier le vocabulaire, la méthode et l'équité de traitement ; renvoyer au rédacteur ce qui ne va pas | Réécrire lui-même, modifier un verdict |
| **Fondateur** (humain) | Valider la liste des questions, trancher les désaccords que les agents ne peuvent pas résoudre, vérifier les sources, publier | Rédiger lui-même un passage |

Les huit experts correspondent aux huit familles politiques définies dans les consignes. Chacun s'appuie d'abord sur les textes, les données et les experts que sa famille reconnaît, tout en restant soumis à la même exigence de preuve que les autres.

## La structure d'une fiche

Une fiche ne répond plus à une seule question : elle traite un aspect précis d'un sujet, découpé en questions précises, chacune avec ses arguments pour et contre.

&#91;embedded content: structure d'une fiche · exemple sur la dette, 4 niveaux\]

**Les cinq niveaux**

- **Thème et sujet** : le thème de navigation (Économie et finances publiques), puis le sujet à l'intérieur de ce thème (la dette). Une fiche peut appartenir à plusieurs sujets, et un sujet à plusieurs thèmes.
- **Fiche** : un aspect précis d'un sujet, par exemple l'annulation de la dette.
- **Questions** : chacune appelle un oui ou un non et a un type (fait, estimation, valeur), qui détermine la façon de la juger. C'est l'unité qu'on partage, et à laquelle se rattacheront plus tard les positions des candidats, les votes et les déclarations.
- **Arguments** : pour, contre ou nuancés. Chacun repose sur des affirmations, qui gardent leur type, leur verdict et leurs sources.

**Deux niveaux de lecture partout.** Chaque partie de la fiche, et chaque question, commence par une lecture rapide qui suffit à comprendre l'essentiel, puis donne le détail complet. La lecture rapide n'est pas un résumé bâclé : quelqu'un qui ne lit qu'elle doit comprendre correctement la question et l'état des connaissances.

**Pas de plafond de longueur.** Une fiche est aussi longue que la matière l'exige, sans redite. La lisibilité vient de la lecture à deux niveaux, pas de la brièveté.

**Les parties d'une fiche** : lecture rapide de la fiche ; contexte et définitions ; chiffres clés ; les questions, chacune avec sa réponse rapide (l'état de la question) et ses arguments détaillés ; les valeurs en jeu ; pour aller plus loin ; informations sur la fiche (date, version, historique, journal des agents).

## Le dossier partagé

Tous les agents lisent et écrivent dans un même dossier, enregistré sous forme de fichiers : c'est lui, et non des messages échangés, qui porte l'état du travail. Un agent ne parle jamais directement à un autre ; il ajoute un élément au dossier, et le coordinateur répartit le travail qui en découle.

**Ce que contient le dossier**

| Élément | Ce qu'il porte | Statuts possibles |
| --- | --- | --- |
| Question | Énoncé, type (fait, estimation, valeur), famille et fiche de rattachement | Proposée, validée, close |
| Argument | Position (pour, contre, nuancé), énoncé, auteur (quel expert), affirmations sur lesquelles il repose | Ouvert, contesté, stable |
| Affirmation | Énoncé, type, sources, verdict | En attente, vérifiée, contestée, invérifiable |
| Source | Titre, auteur, date, adresse, niveau (1 à 4), extrait exact | À vérifier, conforme, non conforme, inaccessible |
| Objection | Élément visé, nature (fait ou raisonnement), contenu, sources | Ouverte, transmise au vérificateur, résolue, remontée au fondateur |
| Journal | Chaque action de chaque agent, datée | — |

**Exemple d'objection enregistrée**

```yaml
objection:
  id: O12
  vise: A4            # affirmation visée
  auteur: expert-centre-droit
  nature: fait
  contenu: "La source S7 date de 2019 ; le chiffre a été révisé depuis."
  sources: [S15]
  statut: transmise-verificateur
```

**Pourquoi des fichiers.** Le dossier peut être relu par le fondateur à tout moment, repris après une interruption, versionné dans GitHub comme le reste du contenu, et converti directement dans le format des fiches du site.

## Déroulement

Huit phases, mais pas une chaîne : les phases 3 et 4 tournent ensemble aussi longtemps qu'il reste quelque chose à dire ou à vérifier.

1. **Cadrage des questions.** Chaque expert propose les questions que sa famille juge essentielles sur le thème ; le coordinateur les fusionne. Le fondateur valide le périmètre : il peut écarter une question hors sujet, mais jamais une question proposée par une famille sans en noter la raison au journal.
2. **Contributions indépendantes.** Chaque expert écrit ses arguments sur chaque question, avec leurs sources, sans voir ceux des autres. Cela évite que le premier à parler oriente tous les autres.
3. **Vérification continue.** Le vérificateur contrôle chaque source dès qu'elle entre dans le dossier, et donne un premier verdict à chaque affirmation.
4. **Confrontation.** Les experts lisent tout le dossier et réagissent : contre-arguments, réfutations, objections sur une source ou un verdict, réponses aux objections reçues. Chaque objection factuelle retourne au vérificateur (phase 3) ; chaque objection de raisonnement devient un contre-argument.
5. **Stabilisation.** Le coordinateur déclare le dossier stable quand la condition d'arrêt est remplie. Les désaccords bloqués sont remontés au fondateur, qui tranche.
6. **Rédaction.** Le rédacteur écrit la fiche partie par partie, chaque partie avec sa lecture rapide puis son détail.
7. **Relecture de symétrie.** Le relecteur contrôle le vocabulaire et l'équité de traitement ; ses remarques retournent au rédacteur jusqu'à ce qu'il n'en reste aucune.
8. **Vérification humaine et publication.** Le fondateur vérifie les sources avec la liste de contrôle, puis publie.

## Règles de confrontation

La confrontation est libre dans sa durée, mais encadrée dans sa forme : chaque intervention doit faire avancer le dossier.

1. **Toute intervention vise un élément précis** du dossier (une question, un argument, une affirmation, une source), jamais « la fiche en général ».
2. **Toute objection dit sa nature** : fait (une source, un chiffre, une date) ou raisonnement (une conclusion qui ne découle pas des prémisses, un argument incomplet).
3. **Une objection factuelle s'appuie sur une source**, ou signale précisément ce que la source citée ne dit pas.
4. **Pas de répétition.** Une objection déjà résolue ne peut revenir que si elle apporte un élément nouveau : une autre source, un autre raisonnement.
5. **Un expert peut défendre ses arguments**, les corriger ou les retirer, mais jamais modifier l'apport d'un autre.
6. **Un expert doit signaler une erreur factuelle même dans un argument de son propre camp.** La même exigence de preuve vaut pour tous.
7. **Aucune attaque contre un autre expert** : on conteste un élément, pas celui qui l'a écrit.
8. **Les désaccords de valeur ne sont pas des objections.** Ils sont enregistrés comme tels et deviennent, dans la fiche, la partie « valeurs en jeu ».

## Condition d'arrêt et garde-fous

Le travail ne s'arrête jamais sur un compteur, seulement quand il est fini ; les garde-fous servent à repérer un blocage, pas à couper la discussion.

**Condition d'arrêt.** Le coordinateur déclare le dossier stable quand les trois conditions suivantes sont réunies :

1. un passage complet de tous les experts n'a apporté aucun nouvel argument ni aucune nouvelle objection ;
2. toutes les objections factuelles ont été tranchées par le vérificateur, ou remontées au fondateur ;
3. chaque question a au moins une réponse argumentée de chaque position présente dans le débat.

**Ce qui n'a pas à converger.** Un désaccord de valeur, ou deux estimations sérieuses qui se contredisent, ne bloquent pas l'arrêt. Ils sont enregistrés tels quels et deviennent « valeurs en jeu » ou « débat entre experts » dans la fiche.

**Garde-fous**

- **Alerte de boucle** : si une même objection revient deux fois sans élément nouveau, ou si deux experts se répondent sur le même point sans avancer, le coordinateur arrête ce fil et le remonte au fondateur avec un résumé des positions. Le reste du travail continue.
- **Pause et reprise** : tout l'état est dans le dossier. Si l'abonnement atteint sa limite d'usage, le travail s'interrompt et reprend exactement là où il s'était arrêté, sans rien perdre ni recommencer.
- **Suivi de la consommation** : le coordinateur note dans le journal le nombre de passages et la durée de chaque phase. Ce n'est pas une limite : c'est la mesure qui permettra de savoir si l'abonnement suffit.

## Ce qui remonte au fondateur

Le fondateur n'intervient qu'à quatre moments, tous prévus d'avance ; le reste du temps, le système travaille seul.

| Moment | Ce qu'il reçoit | Ce qu'il fait |
| --- | --- | --- |
| Après le cadrage | La liste des questions, avec la famille qui a proposé chacune | Valide le périmètre ; toute question écartée est justifiée au journal |
| Pendant la confrontation, si besoin | Un désaccord bloqué, avec le résumé des positions et des sources | Tranche, ou demande une recherche complémentaire ; sa décision et sa raison sont notées au journal |
| Après la rédaction | La fiche, le dossier complet, le journal et la liste des sources | Vérifie chaque source avec la liste de contrôle ; tout écart renvoie au rédacteur ou au vérificateur |
| À la publication | La fiche validée | Accepte la demande de modification dans GitHub |

**Une règle protège la méthode** : quand le fondateur tranche un désaccord, il le fait à partir des sources présentées, et sa décision est publique dans le journal de la fiche. C'est ce qui évite que ses propres opinions ne s'invitent par cette porte.

## Consignes de rôle

Chaque agent reçoit les consignes communes (principes, types et verdicts, hiérarchie des sources, règles juridiques, style), puis les consignes de son rôle ci-dessous. Ce sont des premières versions, à ajuster sur la fiche de test.

**Coordinateur**

```text
Tu es le coordinateur de la rédaction d'une fiche Polisible sur le thème : [THÈME].
Tu ne produis aucun argument, ne juges aucun fait, n'écris pas la fiche.
Ton travail :
1. Fusionner les questions proposées par les experts en une liste sans doublon, chaque question appelant un oui ou un non et typée (fait, estimation, valeur). Indiquer quelle famille a proposé chaque question.
2. Répartir le travail : signaler à chaque expert les éléments du dossier qui le concernent, envoyer chaque nouvelle source et chaque objection factuelle au vérificateur.
3. Détecter les boucles : une objection qui revient sans élément nouveau, ou deux experts qui se répondent sans avancer. Arrêter ce fil et préparer un résumé pour le fondateur.
4. Déclarer le dossier stable seulement quand la condition d'arrêt est remplie.
5. Tenir le journal : chaque action, datée, et le nombre de passages.
```

**Expert** (un par famille)

```text
Tu es l'expert de la famille [FAMILLE] (priorités : [PRIORITÉS] ; partis de cette famille, à titre d'exemple : [PARTIS]).
Tu représentes le lecteur le plus exigeant et le mieux informé de cette famille, pas la ligne officielle d'un parti.
Ton travail :
1. Proposer les questions que ta famille juge essentielles sur le thème.
2. Sur chaque question, écrire la meilleure version des arguments de ta famille, chacun appuyé sur des sources que tu as réellement ouvertes, en priorité de niveau 1 et 2.
3. Lire les apports des autres experts et réagir : contre-argument, réfutation, objection sur une source ou un verdict. Chaque intervention vise un élément précis et dit sa nature (fait ou raisonnement).
4. Défendre, corriger ou retirer tes propres arguments quand on les conteste.
5. Signaler aussi les erreurs factuelles de ton propre camp.
Tu ne cherches pas de compromis. Tu ne modifies jamais l'apport d'un autre. Un désaccord de valeur s'enregistre comme tel, ce n'est pas une objection.
```

**Vérificateur**

```text
Tu es le vérificateur. Tu n'as aucun camp et tu n'argumentes jamais.
Pour chaque source qui entre dans le dossier : ouvre-la, vérifie qu'il s'agit du bon document (titre, auteur, date), que l'extrait ou le chiffre y figure, et qu'il dit la même chose que l'affirmation (même périmètre, même année, même unité). Donne-lui un statut : conforme, non conforme ou inaccessible.
Pour chaque affirmation : attribue le verdict de l'échelle de son type, avec une explication d'une à trois phrases.
Pour chaque objection factuelle : tranche à partir des sources, ou déclare le point invérifiable. Si deux sources sérieuses se contredisent, dis-le : c'est un « débat entre experts », pas une victoire de l'un des camps.
Tu ne te prononces jamais sur une valeur.
```

**Rédacteur**

```text
Tu es le rédacteur. Tu n'as aucun camp.
À partir du dossier stabilisé, écris la fiche dans la structure à quatre niveaux (famille, thème, questions, arguments), en commençant chaque partie par une lecture rapide qui suffit à comprendre, puis le détail complet.
Tu n'utilises que les arguments, affirmations, sources et verdicts du dossier. Tu n'ajoutes rien, tu ne changes aucun verdict. Si quelque chose manque pour être clair, signale-le au coordinateur au lieu de le compléter.
Tu écris partie par partie. La fiche doit être complète, sans redite : sa longueur suit la matière.
```

**Relecteur de symétrie**

```text
Tu es le relecteur de symétrie. Pour chaque position et chaque famille, vérifie : le vocabulaire employé pour rapporter les propos, l'absence de qualificatif, l'application de la même méthode et de la même exigence de preuve. Pour chaque paragraphe, imagine-le appliqué au camp opposé avec les mêmes mots : la formulation reste-t-elle acceptable ?
Un écart de longueur ou de verdicts n'est pas un problème s'il découle de la matière et des sources. Ne propose jamais de modifier un verdict pour équilibrer.
Tu ne réécris rien : tu listes les problèmes, et le rédacteur corrige.
```

## Mise en œuvre avec Claude Code

Le système sera le premier projet construit avec Claude Code, avant le site : la fiche sur la dette servira de test.

**Organisation proposée**

- **Un dépôt GitHub dédié à la rédaction**, distinct de celui du site, contenant les consignes communes, les consignes de chaque rôle, et un dossier par fiche (questions, arguments, affirmations, sources, objections, journal, fiche finale).
- **Chaque rôle est un sous-agent** de Claude Code, avec son propre fichier de consignes et son propre contexte. Le coordinateur lance les experts en parallèle, puis distribue le travail selon l'état du dossier.
- **Recherche web activée** pour les experts et le vérificateur.
- **Sessions dans le cloud**, pour que le travail continue ordinateur éteint et se suive depuis le téléphone.
- **Reprise** : une simple consigne du type « reprends le dossier de la fiche dette » relance le travail là où il s'était arrêté.
- **Sortie** : le dossier étant déjà structuré, la fiche finale se convertit directement au format des fiches du site.

**Construction par étapes**

1. Version minimale : coordinateur, experts, vérificateur, rédacteur, sur une seule question.
2. Le thème complet de la dette, avec la confrontation et la condition d'arrêt.
3. Ajout du relecteur de symétrie, des alertes de boucle et du suivi de consommation.
4. Bilan : temps, consommation de l'abonnement, qualité de la fiche, ajustements des consignes.

**À vérifier au moment de construire** : les possibilités exactes des sous-agents de Claude Code et les limites d'usage de l'abonnement Pro évoluent ; la documentation officielle fera foi.

## Questions ouvertes

Trois points seront tranchés par la fiche de test, pas par avance.

1. **La consommation** : l'abonnement Pro suffit-il pour une fiche complète ? Sinon, quelles parties alléger (moins de familles par question, passages espacés) ou faut-il envisager l'API, avec un budget ?
2. **La publication du journal** : décidé le 8 novembre 2026 : chaque fiche affiche par défaut un résumé du journal, et le journal complet est téléchargeable.
3. **Le rôle des experts sur les questions de valeur** : sur une question de valeur, chaque famille expose ce qu'elle priorise ; faut-il quand même une confrontation, ou seulement une présentation de chaque position ?
