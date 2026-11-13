# Décryptages

Un dossier par décryptage, selon la spécification des décryptages :

```text
decryptages/
  <identifiant>/
    decryptage.yaml   le contenu publié
    sources.yaml      les sources
    donnees/          les tableaux de données des graphiques (CSV)
    dossier/          le travail des agents (non affiché, mais public)
    journal.md        le résumé du journal
    controle.yaml     la liste de contrôle remplie par le fondateur
```

Le schéma qui valide ces fichiers est écrit dans le code du site (`src/contenu/schemas/`).
Chaque demande de modification est validée automatiquement : une erreur (champ manquant, verdict
hors échelle, appel `[S4]` sans source…) est affichée en commentaire, et aucun aperçu n'est produit.

Le site en ligne n'affiche que les décryptages au statut `publie`. Les deux dossiers `exemple-fictif-*`
sont des **exemples entièrement fictifs**, au statut `brouillon`, qui ne servent qu'à tester le site dans les aperçus.
