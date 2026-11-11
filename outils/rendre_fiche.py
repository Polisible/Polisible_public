#!/usr/bin/env python3
"""Assemble fiches/<fiche>/fiche.md à partir du dossier et des textes du rédacteur.

Usage : python3 outils/rendre_fiche.py <fiche> [--verifier]

Suit docs/format-fiche.md : aucune mise en forme n'est laissée au choix d'un agent.
--verifier : contrôle seulement dossier/redaction.yaml (limites, identifiants) sans écrire la fiche.
"""
import argparse, re, sys
import dossier as d

LIM = {"lecture_rapide": 250, "contexte": 150, "definition": 40, "chiffre": 20, "reponse_rapide": 80, "valeurs": 60}
VERDICT_LIB = {None: "sans verdict", "": "sans verdict"}
POS_LIB = {"oui": "Oui", "non": "Non", "nuance": "Nuancé"}
ID = re.compile(r"\[(?:[QAFSVO]\d+(?:,\s*)?)+\]")


def mots(s):
    return len(str(s or "").split())


def verifier_textes(R, ids_valides):
    err = []
    def ctl(nom, texte, lim, ids=True):
        if mots(texte) > lim:
            err.append(f"{nom} : {mots(texte)} mots (limite {lim})")
        if ids and not ID.search(str(texte or "")):
            err.append(f"{nom} : aucun identifiant entre crochets")
        for x in re.findall(r"[QAFSVO]\d+", str(texte or "")):
            if x not in ids_valides:
                err.append(f"{nom} : identifiant inconnu {x}")
    ctl("lecture_rapide", R.get("lecture_rapide"), LIM["lecture_rapide"])
    ctl("contexte", R.get("contexte"), LIM["contexte"])
    for x in R.get("definitions", []):
        ctl(f"définition « {x.get('terme')} »", x.get("definition"), LIM["definition"], ids=False)
        if not x.get("sources"):
            err.append(f"définition « {x.get('terme')} » : sans source, à retirer")
    for x in R.get("chiffres_cles", []):
        ctl(f"chiffre « {x.get('libelle')} »", x.get("libelle"), LIM["chiffre"], ids=False)
        if not x.get("affirmations"):
            err.append(f"chiffre « {x.get('libelle')} » : sans affirmation")
    for x in R.get("reponses_rapides", []):
        ctl(f"réponse rapide {x.get('question')}", x.get("texte"), LIM["reponse_rapide"])
    for x in R.get("valeurs_synthese", []):
        ctl(f"synthèse des valeurs {x.get('question')}", x.get("texte"), LIM["valeurs"], ids=False)
    return err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fiche")
    ap.add_argument("--verifier", action="store_true")
    a = ap.parse_args()
    F = a.fiche
    D = {n: d.charger(F, n) for n in ("questions", "arguments", "affirmations", "sources", "valeurs", "objections")}
    E = d.charger(F, "etat")
    R = d.charger(F, "redaction") or {}
    if not isinstance(R, dict):
        R = {}
    aff = {f["id"]: f for f in D["affirmations"]}
    src = {s["id"]: s for s in D["sources"]}
    ids = set(aff) | set(src) | {x["id"] for n in ("questions", "arguments", "valeurs") for x in D[n]}
    err = verifier_textes(R, ids)
    if err:
        print("TEXTES DU RÉDACTEUR À CORRIGER :\n  - " + "\n  - ".join(err))
        if a.verifier:
            sys.exit(1)
    elif a.verifier:
        print("TEXTES VALIDES"); return

    qs = [q for q in D["questions"] if q["statut"] == "validee"]
    num = {q["id"]: i for i, q in enumerate(qs, 1)}
    args = [x for x in D["arguments"] if x.get("statut") != "retire"]
    vus = {}  # affirmation -> numéro de question de première apparition
    L = []
    w = L.append

    def ligne_aff(fid, qnum):
        f = dict(aff[fid])
        f["enonce"] = re.sub(r"\s*\([^()]*\bQ\d+[^()]*\)", "", f["enonce"])  # marques internes
        verdict = f["verdict"] or "sans verdict"
        if fid in vus:
            return f"[{fid}] {f['type'].capitalize()} — {verdict} (voir question {vus[fid]})"
        vus[fid] = qnum
        srcs = " ; ".join(f"[{x['source']}] « {x['extrait']} »" for x in f["sources"])
        expl = f" — {f['explication']}" if f.get("explication") else ""
        return f"[{fid}] {f['enonce']} — {f['type'].capitalize()} — **{verdict}**{expl} Sources : {srcs}"

    def fil(arg, qnum, niveau):
        ind = "   " * niveau
        tete = "Réponse" if niveau else POS_LIB.get(arg["position"], arg["position"])
        corr = " (corrigé)" if arg.get("corrige") else ""
        w(f"{ind}{'↳' if niveau else '▸'} **[{arg['id']}{corr}] {tete}** — {arg['enonce']}")
        if arg.get("raisonnement"):
            w(f"{ind}   *Raisonnement* : {arg['raisonnement']}")
        w(f"{ind}   *Porté par* : " + " ; ".join(d.fmt_porteur(p) for p in arg["porte_par"]))
        for fid in arg["affirmations"]:
            if fid in aff:
                w(f"{ind}   - {ligne_aff(fid, qnum)}")
        w("")
        for rep in [x for x in args if x.get("repond_a") == arg["id"]]:
            fil(rep, qnum, niveau + 1)

    # 1. En-tête
    w(f"# {E.get('titre_fiche', F.replace('-', ' ').capitalize())}")
    w("")
    w(f"Thème : {E.get('theme', '')} · Sujet : {E.get('sujet', '')} · Date : {d.fmt_date(R.get('date'))} · "
      f"Version : {R.get('version', '0.1')}")
    w("")
    w("> Rédigée avec l'assistance d'IA. **Non vérifiée par le fondateur** : ne pas publier.")
    w("")
    # 2. Lecture rapide
    w("## Lecture rapide"); w(""); w(str(R.get("lecture_rapide", "*(à rédiger)*"))); w("")
    # 3. Contexte et définitions
    w("## Contexte et définitions"); w(""); w(str(R.get("contexte", "*(à rédiger)*"))); w("")
    for x in R.get("definitions", []):
        absents = [s for s in x["sources"] if s not in x["definition"]]
        w(f"- **{x['terme']}** : {x['definition']}" + (f" [{', '.join(absents)}]" if absents else ""))
    w("")
    # 4. Chiffres clés
    w("## Chiffres clés"); w("")
    for x in R.get("chiffres_cles", []):
        verdicts = ", ".join(f"{i} {aff[i]['verdict']}" for i in x["affirmations"] if i in aff)
        w(f"- {x['libelle']} [{verdicts}]")
    w("")
    # 5. Questions
    rr = {x["question"]: x["texte"] for x in R.get("reponses_rapides", [])}
    for q in qs:
        n = num[q["id"]]
        w(f"## Question {n} — {q['enonce']}"); w("")
        w(f"Type : {q['type'].capitalize()} [{q['id']}]"); w("")
        w(f"**Réponse rapide.** {rr.get(q['id'], '*(à rédiger)*')}"); w("")
        actifs = {x["id"] for x in args}
        # une réponse à un argument retiré devient une racine (sinon elle disparaîtrait du fil)
        racines = [x for x in args if x["question"] == q["id"] and x.get("repond_a") not in actifs]
        for pos in ("oui", "non", "nuance"):
            for arg in [x for x in racines if x["position"] == pos]:
                fil(arg, n, 0)
        inst = [f for f in D["affirmations"] if f.get("declaration") and f.get("porteur", {}).get("institution")
                and q["id"] in f.get("questions", [])]
        if inst:
            w("### Ce qu'en disent les institutions"); w("")
            for f in inst:
                w(f"- {d.fmt_porteur(f['porteur'])} — {f['enonce']} — **{f['verdict']}**")
            w("")
        partis = sorted({p for x in q.get("sans_position", []) for p in x.get("partis", [])})
        if partis:
            w(f"*Aucune position publique trouvée pour : {', '.join(partis)} "
              "(programme, site, dirigeants et travaux parlementaires consultés).*")
            w("")
    # 6. Valeurs
    w("## Les valeurs en jeu"); w("")
    vs = {x["question"]: x["texte"] for x in R.get("valeurs_synthese", [])}
    for q in qs:
        vals = [v for v in D["valeurs"] if v["question"] == q["id"] and v.get("statut") != "retire" and v.get("porte_par")]
        if not vals and q["id"] not in vs:
            continue
        w(f"**Question {num[q['id']]}.** {vs.get(q['id'], '')}"); w("")
        for v in vals:
            w(f"- {v['enonce']} — " + " ; ".join(d.fmt_porteur(p) for p in v["porte_par"]))
        w("")
    # 7. Pour aller plus loin
    cites = {x["source"] for f in aff.values() for x in f["sources"]}
    w("## Pour aller plus loin"); w("")
    for s in D["sources"]:
        if s["id"] in cites and s.get("niveau") in (1, 2) and s["statut"] == "conforme":
            w(f"- [{s['id']}] {s['titre']} — {s['auteur']}, {d.fmt_date(s['date'])} — {s['adresse']}")
    w("")
    # 8. Informations sur la fiche
    w("## Informations sur la fiche"); w("")
    passages = max(0, E.get("passage", 1) - 1)
    w(f"- Passages de confrontation : {passages}. Condition d'arrêt : {R.get('condition_arret', 'voir le journal')}.")
    w("- Journal : [journal.md](journal.md) · Dossier : [dossier/](dossier/) · Mesures : [mesures.md](mesures.md)")
    w(""); w("| Source | Titre | Auteur | Date | Niveau | Statut | Adresse |"); w("| --- | --- | --- | --- | --- | --- | --- |")
    for s in D["sources"]:
        w(f"| {s['id']} | {s['titre']} | {s['auteur']} | {d.fmt_date(s['date'])} | {s.get('niveau') or '—'} | "
          f"{str(s['statut']).capitalize()} | {s['adresse']} |")
    w("")
    if R.get("manques"):
        w("### Manques signalés"); w("")
        for m in R["manques"]:
            w(f"- {m.get('vise')} ({m.get('nature')}) : {m.get('besoin')}")
        w("")
    (d.RACINE / "fiches" / F / "fiche.md").write_text("\n".join(L))
    print(f"fiche.md : {sum(len(l.split()) for l in L)} mots, {len(qs)} questions, {len(args)} arguments")


if __name__ == "__main__":
    main()
