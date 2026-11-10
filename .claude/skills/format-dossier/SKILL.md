---
name: format-dossier
description: Comment un agent Polisible écrit son apport dans le dossier partagé d'une fiche (format YAML des dépôts, références, contrôle). À utiliser par les experts et le vérificateur.
---

# Écrire dans le dossier

Tu n'écris **que** le fichier de dépôt que le coordinateur t'a indiqué (`fiches/<fiche>/dossier/entrees/<agent>-p<passage>.yaml`). Tu ne modifies jamais les fichiers officiels du dossier (`questions.yaml`, `arguments.yaml`…) : l'outil `outils/dossier.py` les fusionne et numérote.

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
    sources:
      - {source: s1, extrait: "Une phrase au plus, copiée exactement de la source."}
arguments:
  - ref: a1
    question: Q1
    position: contre          # pour (oui) | contre (non) | nuance
    enonce: "L'argument en deux phrases, dans sa meilleure version."
    porte_par:                # qui défend réellement cet argument, d'après ses propres textes
      - {qui: "Parti, personne ou institution", source: s2}
    affirmations: [f1]
    repond_a: A3              # seulement pour un contre-argument (phase 4)
objections:                   # phase 4, uniquement de nature « fait »
  - vise: F2
    nature: fait
    contenu: "Ce qui est inexact, précisément."
    sources: [s3]             # ou bien :
    ce_que_la_source_ne_dit_pas: "…"
corrections:                  # phase 4, sur TES arguments seulement
  - {vise: A1, action: retirer}            # ou {vise: A1, action: corriger, enonce: "…"}
valeurs:                      # désaccords de valeur : pas des objections
  - {question: Q1, enonce: "Ce que ta famille met en priorité, sans verdict."}
incertitudes:                 # principe 6 : les points dont tu n'es pas sûr
  - "…"
```

Règles vérifiées par l'outil : extrait ≤ 320 caractères (une phrase), niveau 1 à 4, adresse web, `porte_par` sourcé, type et position valides. Une objection de **raisonnement** ne s'écrit pas en objection : écris un contre-argument (`arguments` avec `repond_a`).

## Dépôt du vérificateur

```yaml
agent: verificateur
role: verificateur
phase: 3
sources:
  - {id: S1, statut: conforme, note: "Bon document ; extrait présent, même périmètre."}
  # statut : conforme | non-conforme | inaccessible ; date_corrigee si la date annoncée est fausse
affirmations:
  - {id: F1, verdict: "Vrai", explication: "Une à trois phrases."}
  # fait : Vrai | Plutôt vrai | Trompeur | Faux | Invérifiable
  # estimation : Consensus large | Majorité des estimations | Débat entre experts | Pas d'estimation fiable
  # valeur : verdict vide (null)
objections:
  - {id: O1, statut: resolue, resolution: "Ce que disent les sources, en une à trois phrases."}
  # statut : resolue | remontee-fondateur
```
