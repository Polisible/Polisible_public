# Polisible — La commission

*Proposition soumise au fondateur, 11 novembre 2026.*

La commission est un groupe neutre qui instruit chaque question à partir des arguments collectés et vérifiés. Elle ne collecte pas : elle regroupe, examine, interroge les familles, puis répond. Elle ne juge jamais une valeur.

## 1. Composition et rôles

| Rôle | Ce qu'il fait | Ce qu'il n'a pas le droit de faire |
| --- | --- | --- |
| **Rapporteur** (opus) | Regroupe les arguments en thèses, les examine avec la grille, formule les relances, rédige la réponse à chaque question | Ajouter un fait absent du dossier, juger une valeur, examiner deux thèses avec des critères différents |
| **Contradicteur** (opus) | Teste chaque conclusion du rapporteur avec la même grille, dans les deux sens : une thèse jugée faible est-elle sous-estimée ? une thèse jugée solide est-elle surestimée ? | Proposer sa propre réponse, juger une valeur |
| **Experts** | Répondent aux relances ; exercent un droit de réponse sur l'examen de leurs thèses | Modifier l'examen, contester sur un autre terrain que le fait ou le raisonnement |
| **Vérificateur** | Contrôle tout fait nouveau apporté par une relance ou un droit de réponse ; tranche les contestations factuelles | Examiner la solidité d'une thèse |
| **Fondateur** | Tranche un désaccord persistant entre rapporteur et contradicteur, ou une contestation d'expert non résolue | Rédiger un passage |

Les deux agents de la commission ne voient pas l'appartenance des experts à une famille : les thèses sont présentées avec les partis qui les portent, mais l'examen porte sur le contenu.

## 2. Les thèses

Une **thèse** regroupe les arguments qui défendent la même conclusion **par le même raisonnement**. Deux arguments qui arrivent à la même conclusion par des chemins différents font deux thèses.

| Champ | Contenu | Limite |
| --- | --- | --- |
| `id` | `T…` | |
| `question` | `Q…` | |
| `position` | `oui`, `non`, `nuance` | |
| `enonce` | la conclusion et le raisonnement commun, à l'indicatif | 2 phrases, 50 mots |
| `arguments` | les `A…` regroupés | au moins 1 |
| `portee_par` | sigles des partis qui portent au moins un des arguments (calculé) | |
| `repond_a` | thèses auxquelles celle-ci répond | |

Le regroupement est mécanique dans sa trace : chaque argument appartient à une seule thèse, et la liste est publiée.

## 3. La grille d'examen

Chaque thèse est examinée sur cinq critères, toujours dans cet ordre, avec la même échelle pour toutes.

| Critère | Question | Échelle | Ce qui compte |
| --- | --- | --- | --- |
| **Pertinence** | La thèse répond-elle à la question posée ? | `oui` · `en partie` · `hors sujet` | Une thèse sur l'utilité d'une mesure ne répond pas à une question sur sa légalité. |
| **Appui** | Ses affirmations sont-elles vérifiées et suffisent-elles à la porter ? | `solide` · `partiel` · `faible` | Verdicts des affirmations ; niveau des sources ; une affirmation « Invérifiable » ou « Pas d'estimation fiable » ne peut pas porter seule une thèse. |
| **Raisonnement** | La conclusion découle-t-elle des affirmations ? | `valide` · `lacune` | Nommer la lacune : généralisation, conclusion plus large que les prémisses, cause supposée, silence d'un texte pris pour une permission ou une interdiction. |
| **Portée** | Qu'établit réellement la thèse ? | une phrase : « établit … ; ne prouve pas … » | Distinguer ce qui est montré de ce qui est affirmé. |
| **Objections** | Les thèses qui lui répondent ont-elles reçu une réponse ? | `répondues` · `en partie` · `sans réponse` | Une objection sans réponse affaiblit la thèse, qu'elle vienne de n'importe quel camp. |

**Conclusion de l'examen**, déduite des critères :

| Conclusion | Règle |
| --- | --- |
| **Tient** | pertinence `oui`, appui `solide`, raisonnement `valide`, objections `répondues` ou `en partie` |
| **Tient en partie** | pertinence `oui` ou `en partie`, et au moins un critère intermédiaire (`partiel`, `lacune` limitée à une partie de la conclusion, objections `en partie` ou `sans réponse`) |
| **Ne tient pas** | pertinence `hors sujet`, ou appui `faible`, ou raisonnement `lacune` sur l'essentiel de la conclusion |

Chaque critère est accompagné d'une à deux phrases de justification qui citent les identifiants. Une conclusion qui ne suit pas cette règle est refusée par l'outil.

**Ce que la grille ne juge jamais** : qu'une priorité soit meilleure qu'une autre, qu'un objectif soit souhaitable, la sincérité ou les intentions d'une personne. Une thèse de valeur est examinée seulement sur ses présupposés factuels (« cette priorité suppose que X ; X est … ») et sur sa pertinence.

## 4. Les relances

Quand une thèse a une lacune, un appui partiel ou une objection sans réponse, le rapporteur peut poser **une question précise** à la ou aux familles qui la portent : « Votre thèse T4 suppose X, que le dossier n'établit pas. Avez-vous une source ? » ou « Que répondez-vous à T9 ? ». L'expert répond par les moyens habituels (argument, correction, affirmation sourcée), le vérificateur contrôle les faits nouveaux, et l'examen est repris. **Deux tours de relances au plus** par fiche. La même règle s'applique à toutes les thèses : une lacune de même nature donne lieu à une relance de même nature, quel que soit le camp.

## 5. La réponse à chaque question

| Type de question | Ce que répond la commission | Forme |
| --- | --- | --- |
| **Fait** | Une réponse, avec le degré de certitude de l'échelle des faits (Vrai, Plutôt vrai, Trompeur, Faux, Invérifiable), appliquée à la réponse à la question | « En l'état [du droit / des données], … » ; puis la thèse la plus solide de chaque position, et pourquoi |
| **Estimation** | L'état des estimations (Consensus large, Majorité des estimations, Débat entre experts, Pas d'estimation fiable), et qui les a produites | Puis ce que valent les thèses de chaque camp au regard de ces estimations |
| **Valeur** | Aucune réponse | Ce qu'implique chaque choix, quels présupposés factuels sont établis ou non |

Limites : la réponse tient en 120 mots au plus, et chaque phrase cite ses identifiants (thèses `T…`, affirmations `F…`). Elle ne désigne aucun camp par une famille ni par un qualificatif.

## 6. Garde-fous

1. **Contradicteur** : pour chaque thèse, il confirme ou conteste chaque critère, avec justification. Un désaccord sur un critère est noté ; après un échange, s'il persiste, il remonte au fondateur, et la fiche affiche les deux appréciations.
2. **Droit de réponse des experts** : chaque famille reçoit l'examen des thèses qu'elle porte et peut le contester une fois, sur le fait (tranché par le vérificateur) ou sur le raisonnement (tranché par le contradicteur ; en cas de désaccord, par le fondateur).
3. **Symétrie** : le relecteur de symétrie contrôle que la même lacune a reçu la même appréciation dans tous les camps, et que les relances ont été posées de la même façon.
4. **Traçabilité** : thèses, examens, relances, contestations et décisions sont dans le dossier et le journal, publics.

## 7. Place dans le déroulement

1. Cadrage · 1 bis. Bibliothèque · 2. Contributions · 3. Vérification · 4. **Une** passe de confrontation libre
5. **Commission** : regroupement → examen (rapporteur) → contre-examen (contradicteur) → relances (au plus deux tours, avec vérification) → droit de réponse → réponses aux questions
6. Rédaction (textes de synthèse) · 7. Relecture de symétrie · 8. Vérification humaine

## 8. Forme de la fiche (pour chaque question)

1. **La réponse de la commission** (§ 5).
2. **Pourquoi** : les thèses qui tiennent, puis celles qui tiennent en partie, puis celles qui ne tiennent pas, une ligne chacune : énoncé, conclusion de l'examen, raison principale.
3. **Qui défend quoi** : tableau, une ligne par thèse, colonnes Position · Thèse · Partis · Conclusion.
4. **En détail** (annexe de la question) : examen complet de chaque thèse, fil des arguments, affirmations, positions des institutions, partis sans position.
