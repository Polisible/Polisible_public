---
name: format-dossier
description: Comment un agent Polisible écrit son apport dans le dossier partagé d'une fiche (format YAML des dépôts, références, contrôle). À utiliser par les experts et le vérificateur.
---

# Écrire dans le dossier

Le format de chaque champ est fixé par `docs/format-fiche.md` (dates, sigles des partis, porteur, positions, longueurs) : l'outil refuse tout écart.

Tu n'écris **que** le fichier de dépôt que le coordinateur t'a indiqué (`fiches/<fiche>/dossier/entrees/<agent>-passage<N>.yaml`). Tu ne modifies jamais les fichiers officiels du dossier (`questions.yaml`, `arguments.yaml`…) : l'outil `outils/dossier.py` les fusionne et numérote.

**Références.** Dans ton dépôt, nomme tes nouveaux éléments avec des références locales en minuscules (`s1`, `f1`, `a1`). Pour viser un élément déjà au dossier, utilise son identifiant global (`S4`, `F2`, `A7`, `Q1`). Une source déjà au dossier (même adresse) est reconnue automatiquement.

**Avant de finir**, lance `python3 outils/dossier.py valider <ton fichier>` et corrige jusqu'à obtenir `VALIDE`.

## Dépôt d'un expert

```yaml
agent: expert-centre          # ton nom d'agent
phase: 2                      # 2 = contributions, 4 = confrontation
sources:
  - ref: s1
    titre: "Titre exact du document"
    auteur: "Institution ou auteur"
    date: "2026-08-27"        # date du document
    adresse: "https://…"      # adresse réellement ouverte
    niveau: 1                 # 1 à 4, hiérarchie des sources
affirmations:                 # une affirmation = un seul type
  - ref: f1
    enonce: "Énoncé simple et vérifiable."
    type: fait                # fait | estimation | valeur
    # declaration: true       # seulement si le fait à établir est la déclaration elle-même
    sources:
      - {source: s1, extrait: "Une phrase au plus, copiée exactement de la source."}
arguments:
  - ref: a1
    question: Q1
    position: non             # oui | non | nuance : réponse à la QUESTION, pas à la mesure
    enonce: "La thèse, à l'indicatif, sans « selon X » (2 phrases, 50 mots)."
    raisonnement: "Pourquoi les affirmations mènent à la thèse, en citant f1, F3 (3 phrases, 70 mots)."
    porte_par:                # qui défend réellement cet argument, d'après ses propres textes
      - {personne: "Prénom Nom", fonction: "sénateur", parti: LR, date: "2026-10-12", source: s2}
      # parti : sigle de la liste ; fonction au moment de la déclaration ; personne vide si c'est le parti
      # appartenance: sX si la source de la déclaration n'établit pas le parti de la personne
    affirmations: [f1]
    repond_a: A3              # seulement pour un contre-argument (phase 4)
objections:                   # phase 4, uniquement de nature « fait »
  - vise: F2
    nature: fait
    contenu: "Ce qui est inexact, précisément."
    sources: [s3]             # ou bien :
    ce_que_la_source_ne_dit_pas: "…"
examen:                       # phase 4 : une ligne par question, obligatoire
  - {question: Q41, conclusion: "A3 conclut X, mais F12 ne porte que sur Y (contre-argument a1)."}
corrections:                  # sur TES arguments et valeurs seulement
  - {vise: A1, action: retirer}
  - {vise: A2, action: corriger, enonce: "…", raisonnement: "…", position: oui, porte_par: [ … ]}  # champs utiles seulement
valeurs:                      # même règle de porteur que les arguments
  - {question: Q1, enonce: "Priorité à … (1 phrase, 30 mots).", porte_par: [{parti: LR, date: "2026-10", source: s2}]}
questions_proposees:          # phase 1 (cadrage) uniquement
  - {enonce: "Question fermée ?", type: estimation, pourquoi: "Une phrase."}
sans_position:                # après la recherche minimale (les 4 catégories)
  - question: Q2
    partis: [LR]
    lieux_consultes:
      - {categorie: programme, ou: "programme 2027 du parti", resultat: "rien sur ce point"}
      - {categorie: site, ou: "communiqués 2026", resultat: "…"}
      - {categorie: dirigeants, ou: "presse, août-novembre 2026", resultat: "…"}
      - {categorie: parlement, ou: "propositions de loi et de résolution, votes", resultat: "…"}
sources_demandees:            # page impossible à ouvrir : le vérificateur réessaie
  - {adresse: "https://…", pourquoi: "texte de l'arrêt C-493/17", erreur: "403"}
incertitudes:                 # principe 6 : les points dont tu n'es pas sûr
  - "…"
```

Règles vérifiées par l'outil : extrait ≤ 320 caractères (une phrase), niveau 1 à 4, adresse web, `porte_par` sourcé, `raisonnement` présent, type et position valides, pas d'affirmation déclarative (« X a dit que… ») sans `declaration: true`. Une affirmation de la bibliothèque commune se cite par son id (`F3`). Une objection de **raisonnement** ne s'écrit pas en objection : écris un contre-argument (`arguments` avec `repond_a`).

## Dépôt du vérificateur

```yaml
agent: verificateur
role: verificateur
phase: 3
sources:
  - {id: S1, statut: conforme, note: "Bon document ; extrait présent, même périmètre."}
  # statut : conforme | non-conforme | inaccessible ; date_corrigee si la date annoncée est fausse
  # source demandée (statut « demandee » dans le lot) : réessaie, puis donne titre, auteur, niveau si tu l'as ouverte
affirmations:
  - {id: F1, verdict: "Vrai", explication: "Une à trois phrases."}
  # fait : Vrai | Plutôt vrai | Trompeur | Faux | Invérifiable
  # estimation : Consensus large | Majorité des estimations | Débat entre experts | Pas d'estimation fiable
  # valeur : verdict vide (null)
objections:
  - {id: O1, statut: resolue, resolution: "Ce que disent les sources, en une à trois phrases."}
sources_ajoutees:             # source officielle trouvée en vérifiant, rattachée à une affirmation
  - {titre: "…", auteur: "…", date: "…", adresse: "https://…", niveau: 1, pour: F10, extrait: "Une phrase."}
  # statut : resolue | remontee-fondateur
```
