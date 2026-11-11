#!/usr/bin/env python3
"""Commission (docs/commission.md) : thèses, examen, contre-examen, relances, réponses.

Fichiers du dossier : theses.yaml, relances.yaml, reponses.yaml.
Commandes (depuis outils/) :
  python3 commission.py lot <fiche> rapporteur|contradicteur
  python3 commission.py lot <fiche> expert --agent expert-xxx      relances + examen de ses thèses
  python3 commission.py valider <fichier>
  python3 commission.py fusionner <fiche> <fichier>
  python3 commission.py etat <fiche>
"""
import argparse, re, sys
import yaml
import dossier as d

CRITERES = {"pertinence": {"oui", "en partie", "hors sujet"}, "appui": {"solide", "partiel", "faible"},
            "raisonnement": {"valide", "lacune"}, "objections": {"répondues", "en partie", "sans réponse"}}
CONCLUSIONS = {"tient", "tient en partie", "ne tient pas"}
CERTITUDE = {"fait": d.VERDICTS["fait"], "estimation": d.VERDICTS["estimation"], "valeur": {None, ""}}
ID = re.compile(r"\b[TFAS]\d+\b")


def conclusion_attendue(ex):
    """docs/commission.md § 3 : la conclusion découle des critères."""
    p, a, r, o = (ex[k]["valeur"] for k in ("pertinence", "appui", "raisonnement", "objections"))
    essentielle = ex["raisonnement"].get("essentielle", False)
    if p == "hors sujet" or a == "faible" or (r == "lacune" and essentielle):
        return "ne tient pas"
    if p == "oui" and a == "solide" and r == "valide" and o in ("répondues", "en partie"):
        return "tient"
    return "tient en partie"


def erreurs_examen(t, ex):
    err = []
    for k, ech in CRITERES.items():
        c = ex.get(k) or {}
        if c.get("valeur") not in ech:
            err.append(f"{t} : {k} = {sorted(ech)}")
        if not c.get("justification") or not ID.search(c.get("justification", "")):
            err.append(f"{t} : {k} sans justification citant des identifiants")
    if not (ex.get("portee") or {}).get("texte", "").startswith("établit"):
        err.append(f"{t} : portée = « établit … ; ne prouve pas … »")
    if (ex.get("raisonnement") or {}).get("valeur") == "lacune" and "essentielle" not in ex["raisonnement"]:
        err.append(f"{t} : lacune → préciser essentielle: true/false")
    if not err and ex.get("conclusion") != conclusion_attendue(ex):
        err.append(f"{t} : conclusion « {ex.get('conclusion')} » incohérente avec les critères (attendu : « {conclusion_attendue(ex)} »)")
    return err


def valider(e, D=None):
    err, role = [], e.get("role")
    if role not in ("rapporteur", "contradicteur"):
        return ["role = rapporteur ou contradicteur"]
    if role == "rapporteur":
        for t in e.get("theses", []) or []:
            for c in ("id", "question", "position", "enonce", "arguments"):
                if not t.get(c):
                    err.append(f"thèse {t.get('id', '?')} : « {c} » manquant")
            if t.get("position") not in d.POSITIONS:
                err.append(f"{t.get('id')} : position = oui, non ou nuance")
            if d.trop_long(t.get("enonce"), "arg_enonce"):
                err.append(f"{t.get('id')} : énoncé trop long (2 phrases, 50 mots)")
            if t.get("examen"):
                err += erreurs_examen(t["id"], t["examen"])
        if D is not None and e.get("theses"):
            actifs = {a["id"] for a in D["arguments"] if a.get("statut") != "retire"}
            vus = [a for t in e["theses"] for a in t["arguments"]]
            doublons = {a for a in vus if vus.count(a) > 1}
            if doublons:
                err.append(f"arguments dans plusieurs thèses : {sorted(doublons)}")
            if set(vus) != actifs and e.get("regroupement_complet", True):
                err.append(f"regroupement incomplet : manquent {sorted(actifs - set(vus))}, inconnus {sorted(set(vus) - actifs)}")
        for r in e.get("relances", []) or []:
            if not r.get("these") or not r.get("partis") or not r.get("question_posee"):
                err.append(f"relance : these, partis, question_posee obligatoires ({r})")
        for x in e.get("reponses", []) or []:
            if len(str(x.get("texte", "")).split()) > 120 or not ID.search(str(x.get("texte", ""))):
                err.append(f"réponse {x.get('question')} : 120 mots au plus, avec identifiants")
            if D is not None:
                q = next((q for q in D["questions"] if q["id"] == x.get("question")), None)
                if q and x.get("certitude") not in CERTITUDE[q["type"]]:
                    err.append(f"réponse {x.get('question')} ({q['type']}) : certitude hors échelle")
    else:
        for c in e.get("contre_examen", []) or []:
            if not c.get("these") or c.get("critere") not in list(CRITERES) + ["portee", "conclusion", "regroupement"]:
                err.append(f"contre-examen : these et critere obligatoires ({c})")
            if c.get("avis") not in ("confirme", "conteste") or not c.get("justification"):
                err.append(f"contre-examen {c.get('these')}/{c.get('critere')} : avis confirme|conteste + justification")
            if c.get("avis") == "conteste" and not c.get("proposition"):
                err.append(f"contre-examen {c.get('these')}/{c.get('critere')} : une contestation propose une valeur")
        for c in e.get("decisions_contestations", []) or []:
            if not c.get("contestation") or c.get("decision") not in ("acceptee", "rejetee", "remontee-fondateur"):
                err.append(f"décision : contestation et decision (acceptee|rejetee|remontee-fondateur) obligatoires")
    return err


def fusionner(fiche, chemin):
    e = d.lire_entree(chemin)
    D = {n: d.charger(fiche, n) for n in ("questions", "arguments", "theses", "relances", "reponses")}
    err = valider(e, D)
    if err:
        print("REFUSÉ :\n  - " + "\n  - ".join(err)); return False
    faits = []
    if e["role"] == "rapporteur":
        if e.get("theses"):
            parti = {a["id"]: {p.get("parti") or p.get("institution") for p in a["porte_par"]} for a in D["arguments"]}
            anciens = {t["id"]: t for t in D["theses"]}
            for t in e["theses"]:
                t["portee_par"] = sorted({s for a in t["arguments"] for s in parti.get(a, set()) if s})
                if t["id"] in anciens and anciens[t["id"]].get("contre_examen"):
                    t["contre_examen"] = anciens[t["id"]]["contre_examen"]
                if t["id"] in anciens and anciens[t["id"]].get("examen") and t.get("examen") \
                        and anciens[t["id"]]["examen"] != t["examen"]:
                    t.setdefault("versions", anciens[t["id"]].get("versions", [])).append(anciens[t["id"]]["examen"])
            D["theses"] = e["theses"]
            faits.append(f"{len(e['theses'])} thèses")
        for r in e.get("relances", []) or []:
            r["id"] = d.prochain(D["relances"], "R")
            r["statut"] = "posee"
            D["relances"].append(r)
            faits.append(r["id"])
        if e.get("reponses"):
            D["reponses"] = e["reponses"]
            faits.append(f"{len(e['reponses'])} réponses")
    else:
        th = {t["id"]: t for t in D["theses"]}
        for c in e.get("contre_examen", []) or []:
            if c["these"] in th:
                th[c["these"]].setdefault("contre_examen", []).append(
                    {k: c.get(k) for k in ("critere", "avis", "justification", "proposition")})
        for c in e.get("decisions_contestations", []) or []:
            for t in D["theses"]:
                for x in t.get("contestations", []):
                    if x["id"] == c["contestation"]:
                        x["decision"], x["motif"] = c["decision"], c.get("motif")
        n = sum(1 for c in e.get("contre_examen", []) or [] if c.get("avis") == "conteste")
        faits.append(f"contre-examen : {n} contestations")
    for n in ("theses", "relances", "reponses"):
        d.ecrire(fiche, n, D[n])
    d.journaliser(fiche, e["role"], "5", ", ".join(faits) or "rien")
    print("FUSIONNÉ :", ", ".join(faits)); return True


def fusionner_expert(fiche, e, agent):
    """Réponses aux relances et contestations de l'examen, déposées par un expert."""
    D = {n: d.charger(fiche, n) for n in ("theses", "relances")}
    for r in e.get("reponses_relances", []) or []:
        for x in D["relances"]:
            if x["id"] == r["relance"]:
                x.setdefault("reponses", []).append({"agent": agent, "texte": r["texte"], "elements": r.get("elements", [])})
                x["statut"] = "repondue"
    for c in e.get("contestations", []) or []:
        for t in D["theses"]:
            if t["id"] == c["these"]:
                lst = t.setdefault("contestations", [])
                lst.append({"id": f"{t['id']}-C{len(lst) + 1}", "agent": agent, "critere": c["critere"],
                            "nature": c["nature"], "contenu": c["contenu"], "sources": c.get("sources", []),
                            "decision": None})
    d.ecrire(fiche, "theses", D["theses"]); d.ecrire(fiche, "relances", D["relances"])


def lot(fiche, sorte, agent=None):
    D = {n: d.charger(fiche, n) for n in ("questions", "arguments", "affirmations", "sources", "theses",
                                          "relances", "valeurs", "objections")}
    aff = {f["id"]: f for f in D["affirmations"]}
    qs = [q for q in D["questions"] if q["statut"] == "validee"]
    args = [a for a in D["arguments"] if a.get("statut") != "retire"]

    def arg_neutre(a):  # la commission voit les partis, pas la famille de l'expert
        return {"id": a["id"], "question": a["question"], "position": a["position"], "enonce": a["enonce"],
                "raisonnement": a.get("raisonnement"), "repond_a": a.get("repond_a"),
                "partis": sorted({p.get("parti", "") for p in a["porte_par"]}),
                "affirmations": [f"{i} [{aff[i]['type']}, {aff[i]['verdict'] or 'sans verdict'}] {aff[i]['enonce']}"
                                 + (f" — {aff[i]['explication']}" if aff[i]["verdict"] not in ("Vrai", None) else "")
                                 for i in a["affirmations"] if i in aff]}
    base = {"grille": "docs/commission.md § 3 (à relire)",
            "questions": [f"{q['id']} ({q['type']}) {q['enonce']}" for q in qs],
            "institutions": [f"{f['id']} {d.fmt_porteur(f['porteur'])} — {f['enonce']} [{f['verdict']}]"
                             for f in D["affirmations"] if f.get("porteur")],
            "objections": [{k: o[k] for k in ("id", "vise", "contenu", "resolution")} for o in D["objections"]]}
    lots = d.dossier(fiche) / "lots"
    if sorte == "rapporteur":
        data = {**base, "arguments": [arg_neutre(a) for a in args], "theses_actuelles": D["theses"],
                "relances": D["relances"],
                "sans_position": {q["id"]: sorted({p for x in q.get("sans_position", []) for p in x.get("partis", [])})
                                  for q in qs}}
    elif sorte == "contradicteur":
        data = {**base, "arguments": [arg_neutre(a) for a in args],
                "theses": D["theses"], "relances": D["relances"], "reponses": D["reponses"]}
    elif sorte == "expert":
        fam = d.FAMILLES[agent]
        mes = [t for t in D["theses"] if set(t.get("portee_par", [])) & fam]
        data = {"consigne": "Réponds aux relances qui te sont adressées (reponses_relances, avec arguments, "
                            "corrections ou affirmations sourcées si besoin). Tu peux contester une fois l'examen "
                            "de tes thèses (contestations : these, critere, nature fait|raisonnement, contenu, sources). "
                            "Pas de contestation de valeur.",
                "relances": [r for r in D["relances"] if set(r["partis"]) & fam],
                "tes_theses": mes, "questions": base["questions"]}
    else:
        sys.exit("lot inconnu")
    p = lots / f"commission-{sorte}{'-' + agent if agent else ''}.yaml"
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))
    print(p.relative_to(d.RACINE))


def etat(fiche):
    T = d.charger(fiche, "theses")
    from collections import Counter
    print("thèses :", len(T), Counter(t.get("examen", {}).get("conclusion") for t in T))
    print("contestées par le contradicteur :", [t["id"] for t in T if any(c["avis"] == "conteste" for c in t.get("contre_examen", []))])
    print("contestations d'experts :", [(c["id"], c.get("decision")) for t in T for c in t.get("contestations", [])])
    print("relances :", [(r["id"], r["statut"]) for r in d.charger(fiche, "relances")])
    print("réponses :", [r["question"] for r in d.charger(fiche, "reponses")])


def main():
    ap = argparse.ArgumentParser()
    s = ap.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("lot"); x.add_argument("fiche"); x.add_argument("sorte"); x.add_argument("--agent")
    x = s.add_parser("valider"); x.add_argument("fichier")
    x = s.add_parser("fusionner"); x.add_argument("fiche"); x.add_argument("fichier")
    x = s.add_parser("etat"); x.add_argument("fiche")
    a = ap.parse_args()
    if a.cmd == "lot":
        lot(a.fiche, a.sorte, a.agent)
    elif a.cmd == "valider":
        f = d.fiche_de(a.fichier)
        D = {n: d.charger(f, n) for n in ("questions", "arguments")} if f else None
        err = valider(d.lire_entree(a.fichier), D)
        print("VALIDE" if not err else "ERREURS :\n  - " + "\n  - ".join(err)); sys.exit(1 if err else 0)
    elif a.cmd == "fusionner":
        sys.exit(0 if fusionner(a.fiche, a.fichier) else 1)
    elif a.cmd == "etat":
        etat(a.fiche)


if __name__ == "__main__":
    main()
