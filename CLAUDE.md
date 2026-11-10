# Polisible — instructions pour Claude Code

## Le projet

Polisible est un site d'information politique français, gratuit et sans publicité, destiné d'abord aux personnes qui ne savent pas par où commencer. Sa promesse : être transparent et vérifiable, pas « neutre ». Chaque fiche traite un aspect précis d'un sujet (exemple : l'annulation de la dette), découpé en questions qui appellent oui ou non, chacune avec ses arguments pour et contre, appuyés sur des affirmations vérifiées et sourcées.

Les fiches sont construites par un système de plusieurs agents aux rôles séparés, puis vérifiées par un humain, le fondateur, qui n'en écrit aucune phrase.

## Ce dépôt

Dépôt **public** du contenu : consignes des agents, définitions des agents, dossiers de rédaction, fiches. Le code du site vit dans un autre dépôt, privé.

Parce qu'il est public :

- **Jamais de secret** dans ce dépôt (clé d'accès, mot de passe, jeton).
- **Jamais de donnée personnelle** (signalements de lecteurs, adresses e-mail, demandes de droit de réponse).
- **Citations courtes** : aucune source n'est recopiée au-delà d'une phrase, y compris dans les journaux des agents. On garde le lien et l'extrait utile, jamais le texte d'un article.

## Documents de référence (dans `docs/`)

- `docs/architecture-redaction.md` : **fait foi** pour le système de rédaction (rôles, dossier partagé, déroulement, règles de confrontation, condition d'arrêt, consignes de rôle).
- `docs/consignes-ia.md` : les **consignes communes** (principes, types et verdicts, hiérarchie des sources, règles juridiques, style) sont la base de chaque agent. Les consignes d'étape 2 à 5 de ce document sont obsolètes, remplacées par l'architecture.
- `docs/charte-editoriale.md` : règles éditoriales publiques. En cas de contradiction, la charte prévaut.

## Règles de travail

- **Tout en français** : fichiers, consignes, commentaires, messages au fondateur.
- **Le fondateur décide** : proposer un plan et attendre sa validation avant tout changement de structure ou toute action difficile à annuler. Travailler sur une branche et ouvrir une demande de modification (pull request) ; ne jamais publier directement sur la branche principale.
- **Ne jamais inventer** une source, un chiffre, une citation ou une adresse web.

## Économie de tokens

L'abonnement a des limites d'usage partagées : chaque règle ci-dessous compte.

1. **Le bon modèle pour chaque agent** : un modèle économique pour les tâches simples (collecte, tri), le plus capable seulement là où le jugement est critique (vérification, rédaction).
2. **Chaque agent ne lit que ce qui le concerne** : on lui transmet les identifiants des éléments à traiter, jamais tout le dossier sans raison.
3. **Extraire, puis ne plus relire** : d'une page web, on ne garde dans le dossier que l'extrait utile et ses références ; on ne recharge la page qu'en cas de doute.
4. **Consignes courtes et stables** : chaque phrase inutile dans une consigne coûte à chaque appel.
5. **Mesurer** : pour chaque fiche, noter dans `fiches/<sujet>/mesures.md` le nombre de passages et la durée de chaque phase.

## Arborescence prévue

```
.claude/
  agents/      un fichier par rôle (coordination éventuelle, 8 experts, vérificateur, rédacteur, relecteur de symétrie)
  skills/      savoir-faire partagés (écrire dans le dossier, vérifier une source, règles juridiques…)
  commands/    commandes de lancement (ex. /rediger-fiche)
docs/          documents de référence
fiches/
  <sujet>/
    dossier/   questions, arguments, affirmations, sources, objections (YAML)
    journal.md
    mesures.md
    fiche.md   fiche finale
```
