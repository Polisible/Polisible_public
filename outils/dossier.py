#!/usr/bin/env python3
"""Gestion mécanique du dossier d'une fiche Polisible (aucun modèle, aucun jeton).

Seul cet outil écrit les fichiers officiels du dossier. Les agents écrivent
uniquement dans dossier/entrees/ ; le coordinateur fusionne ensuite.

Commandes (lancer depuis la racine du dépôt) :
  init <fiche> --question "..." --type fait|estimation|valeur --theme ... --sujet ...
  valider <fichier-entree>                 contrôle un dépôt sans rien écrire
  fusionner <fiche> <fichier-entree>...    contrôle puis intègre au dossier
  lot <fiche> verif [--taille N]           lot(s) du vérificateur ; avec --taille : sources seules,
                                           puis relancer sans --taille pour les verdicts
  lot <fiche> confrontation --agent NOM    prépare le lot d'un expert
  lot <fiche> redaction                    vue consolidée pour le rédacteur
  etat <fiche>                             état et condition d'arrêt
  chrono <fiche> debut|fin <phase> [--note "..."]
  mesure <fiche> <phase> <agent> [--jetons N] [--outils N] [--duree-ms N]
  journal <fiche>                          régénère journal.md
"""
import argparse, datetime as dt, pathlib, re, sys
import yaml

RACINE = pathlib.Path(__file__).resolve().parent.parent
TYPES = {"fait", "estimation", "valeur"}
POSITIONS = {"pour", "contre", "nuance"}
NATURES = {"fait", "raisonnement"}
VERDICTS = {
    "fait": {"Vrai", "Plutôt vrai", "Trompeur", "Faux", "Invérifiable"},
    "estimation": {"Consensus large", "Majorité des estimations", "Débat entre experts", "Pas d'estimation fiable"},
    "valeur": {None, ""},
}
STATUTS_SOURCE = {"conforme", "non-conforme", "inaccessible"}
STATUTS_OBJ = {"resolue", "remontee-fondateur"}
EXTRAIT_MAX = 320  # une phrase au plus (règle de citation courte, dépôt public)
FICHIERS = ["questions", "arguments", "affirmations", "sources", "objections", "valeurs", "journal"]
PREFIXE = {"arguments": "A", "affirmations": "F", "sources": "S", "objections": "O", "valeurs": "V", "questions": "Q"}
ID_GLOBAL = re.compile(r"^[AFSOVQ]\d+$")
PHASES = {"1": "Cadrage", "2": "Contributions indépendantes", "3": "Vérification",
          "4": "Confrontation", "5": "Stabilisation", "6": "Rédaction",
          "7": "Relecture de symétrie", "8": "Vérification humaine"}


def maintenant():
    return dt.datetime.now().replace(microsecond=0).isoformat()


def dossier(fiche):
    return RACINE / "fiches" / fiche / "dossier"


def charger(fiche, nom):
    p = dossier(fiche) / f"{nom}.yaml"
    if not p.exists():
        return {} if nom == "etat" else []
    return yaml.safe_load(p.read_text()) or ({} if nom == "etat" else [])


def ecrire(fiche, nom, data):
    p = dossier(fiche) / f"{nom}.yaml"
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))


def prochain(liste, prefixe):
    n = [int(x["id"][1:]) for x in liste if str(x.get("id", "")).startswith(prefixe)]
    return f"{prefixe}{max(n, default=0) + 1}"


def journaliser(fiche, agent, phase, action):
    j = charger(fiche, "journal")
    j.append({"date": maintenant(), "agent": agent, "phase": phase, "action": action})
    ecrire(fiche, "journal", j)


def norm_url(u):
    return re.sub(r"[#].*$", "", u.strip()).rstrip("/").lower()


# ---------------------------------------------------------------- validation

def valider_entree(e):
    """Renvoie la liste des erreurs d'un dépôt (vide si correct)."""
    err = []
    if not isinstance(e, dict):
        return ["le fichier doit être un dictionnaire YAML"]
    if not e.get("agent"):
        err.append("champ « agent » manquant")
    role = e.get("role") or ("verificateur" if e.get("agent") == "verificateur" else "expert")
    refs = set()
    for s in e.get("sources", []) or []:
        if role == "verificateur":
            if not ID_GLOBAL.match(str(s.get("id", ""))):
                err.append(f"source sans id global : {s}")
            if s.get("statut") not in STATUTS_SOURCE:
                err.append(f"{s.get('id')} : statut doit être {sorted(STATUTS_SOURCE)}")
            if not s.get("note"):
                err.append(f"{s.get('id')} : « note » (une à trois phrases) obligatoire")
            continue
        for c in ("ref", "titre", "auteur", "date", "adresse", "niveau"):
            if not s.get(c):
                err.append(f"source {s.get('ref', '?')} : champ « {c} » manquant")
        if s.get("niveau") not in (1, 2, 3, 4):
            err.append(f"source {s.get('ref')} : niveau doit être 1, 2, 3 ou 4")
        if not str(s.get("adresse", "")).startswith("http"):
            err.append(f"source {s.get('ref')} : adresse invalide")
        refs.add(s.get("ref"))
    for f in e.get("affirmations", []) or []:
        if role == "verificateur":
            if not ID_GLOBAL.match(str(f.get("id", ""))):
                err.append(f"affirmation sans id global : {f}")
            if not f.get("explication"):
                err.append(f"{f.get('id')} : « explication » obligatoire")
            continue
        for c in ("ref", "enonce", "type", "sources"):
            if not f.get(c):
                err.append(f"affirmation {f.get('ref', '?')} : champ « {c} » manquant")
        if f.get("type") not in TYPES:
            err.append(f"affirmation {f.get('ref')} : type doit être {sorted(TYPES)}")
        for x in f.get("sources", []) or []:
            if isinstance(x, dict):
                if not x.get("source"):
                    err.append(f"affirmation {f.get('ref')} : chaque source doit avoir « source »")
                if len(str(x.get("extrait", ""))) > EXTRAIT_MAX:
                    err.append(f"affirmation {f.get('ref')} : extrait trop long (> {EXTRAIT_MAX} car., une phrase au plus)")
                if not x.get("extrait"):
                    err.append(f"affirmation {f.get('ref')} : extrait manquant pour {x.get('source')}")
            else:
                err.append(f"affirmation {f.get('ref')} : sources au format {{source: s1, extrait: \"...\"}}")
        refs.add(f.get("ref"))
    for a in e.get("arguments", []) or []:
        for c in ("ref", "question", "position", "enonce", "porte_par", "affirmations"):
            if not a.get(c):
                err.append(f"argument {a.get('ref', '?')} : champ « {c} » manquant")
        if a.get("position") not in POSITIONS:
            err.append(f"argument {a.get('ref')} : position doit être {sorted(POSITIONS)}")
        for p in a.get("porte_par", []) or []:
            if not isinstance(p, dict) or not p.get("qui") or not p.get("source"):
                err.append(f"argument {a.get('ref')} : porte_par = liste de {{qui, source}}")
        refs.add(a.get("ref"))
    for o in e.get("objections", []) or []:
        if role == "verificateur":
            if o.get("statut") not in STATUTS_OBJ or not o.get("resolution"):
                err.append(f"{o.get('id')} : statut {sorted(STATUTS_OBJ)} et « resolution » obligatoires")
            continue
        for c in ("vise", "nature", "contenu"):
            if not o.get(c):
                err.append(f"objection : champ « {c} » manquant ({o})")
        if o.get("nature") not in NATURES:
            err.append(f"objection visant {o.get('vise')} : nature doit être fait ou raisonnement")
        if o.get("nature") == "raisonnement":
            err.append(f"objection visant {o.get('vise')} : une objection de raisonnement s'écrit comme contre-argument (arguments, avec repond_a)")
        if o.get("nature") == "fait" and not o.get("sources") and not o.get("ce_que_la_source_ne_dit_pas"):
            err.append(f"objection visant {o.get('vise')} : une objection de fait s'appuie sur une source ou précise ce que la source citée ne dit pas")
    for v in e.get("valeurs", []) or []:
        if not v.get("question") or not v.get("enonce"):
            err.append(f"valeur : « question » et « enonce » obligatoires ({v})")
    # références locales résolubles
    def verif_ref(x, ou):
        if isinstance(x, str) and not ID_GLOBAL.match(x) and x not in refs:
            err.append(f"{ou} : référence « {x} » introuvable dans ce dépôt (utiliser une ref locale ou un id global)")
    for f in e.get("affirmations", []) or []:
        for x in f.get("sources", []) or []:
            if isinstance(x, dict):
                verif_ref(x.get("source"), f"affirmation {f.get('ref') or f.get('id')}")
    for a in e.get("arguments", []) or []:
        for x in a.get("affirmations", []) or []:
            verif_ref(x, f"argument {a.get('ref')}")
        for p in a.get("porte_par", []) or []:
            if isinstance(p, dict):
                verif_ref(p.get("source"), f"argument {a.get('ref')} (porte_par)")
    for o in e.get("objections", []) or []:
        for x in o.get("sources", []) or []:
            verif_ref(x, f"objection visant {o.get('vise')}")
    return err


def lire_entree(chemin):
    try:
        return yaml.safe_load(pathlib.Path(chemin).read_text())
    except yaml.YAMLError as ex:
        print(f"YAML illisible : {ex}")
        sys.exit(1)


# ---------------------------------------------------------------- fusion

def fusionner(fiche, chemin):
    e = lire_entree(chemin)
    err = valider_entree(e)
    if err:
        print(f"REFUSÉ {chemin} :\n  - " + "\n  - ".join(err))
        return False
    agent, phase = e["agent"], str(e.get("phase", "?"))
    etat = charger(fiche, "etat")
    passage = etat.get("passage", 1)
    D = {n: charger(fiche, n) for n in FICHIERS if n != "journal"}
    if (e.get("role") or ("verificateur" if agent == "verificateur" else "expert")) == "verificateur":
        return fusion_verif(fiche, e, D)
    carte, ajouts = {}, []

    def res(x):
        return x if ID_GLOBAL.match(str(x)) else carte[x]

    for s in e.get("sources", []) or []:
        exist = next((x for x in D["sources"] if norm_url(x["adresse"]) == norm_url(s["adresse"])), None)
        if exist:
            carte[s["ref"]] = exist["id"]
            continue
        sid = prochain(D["sources"], "S")
        carte[s["ref"]] = sid
        D["sources"].append({"id": sid, "titre": s["titre"], "auteur": s["auteur"], "date": str(s["date"]),
                             "adresse": s["adresse"], "niveau": s["niveau"], "ajoutee_par": agent,
                             "statut": "a-verifier", "note_verif": None})
        ajouts.append(sid)
    for f in e.get("affirmations", []) or []:
        fid = prochain(D["affirmations"], "F")
        carte[f["ref"]] = fid
        for x in f["sources"]:  # nouvel extrait sur une source déjà vérifiée : elle repasse à vérifier
            for s in D["sources"]:
                if s["id"] == res(x["source"]) and s["statut"] != "a-verifier":
                    s["statut"] = "a-verifier"
        D["affirmations"].append({"id": fid, "enonce": f["enonce"], "type": f["type"],
                                  "sources": [{"source": res(x["source"]), "extrait": x["extrait"]} for x in f["sources"]],
                                  "auteur": agent, "passage": passage, "verdict": None, "explication": None,
                                  "statut": "en-attente"})
        ajouts.append(fid)
    for a in e.get("arguments", []) or []:
        aid = prochain(D["arguments"], "A")
        carte[a["ref"]] = aid
        D["arguments"].append({"id": aid, "question": a["question"], "position": a["position"], "enonce": a["enonce"],
                               "porte_par": [{"qui": p["qui"], "source": res(p["source"])} for p in a["porte_par"]],
                               "affirmations": [res(x) for x in a["affirmations"]],
                               "repond_a": a.get("repond_a"), "auteur": agent, "passage": passage,
                               "statut": "ouvert"})
        if a.get("repond_a"):
            for cible in D["arguments"]:
                if cible["id"] == a["repond_a"] and cible["statut"] == "ouvert":
                    cible["statut"] = "conteste"
        ajouts.append(aid)
    for o in e.get("objections", []) or []:
        oid = prochain(D["objections"], "O")
        D["objections"].append({"id": oid, "vise": o["vise"], "auteur": agent, "nature": o["nature"],
                                "contenu": o["contenu"], "sources": [res(x) for x in o.get("sources", []) or []],
                                "ce_que_la_source_ne_dit_pas": o.get("ce_que_la_source_ne_dit_pas"),
                                "passage": passage, "statut": "transmise-verificateur", "resolution": None})
        for f in D["affirmations"]:
            if f["id"] == o["vise"]:
                f["statut"] = "contestee"
        ajouts.append(oid)
    for v in e.get("valeurs", []) or []:
        vid = prochain(D["valeurs"], "V")
        D["valeurs"].append({"id": vid, "question": v["question"], "auteur": agent, "enonce": v["enonce"],
                             "passage": passage})
        ajouts.append(vid)
    for c in e.get("corrections", []) or []:  # un expert retire ou corrige SON apport
        for a in D["arguments"]:
            if a["id"] == c.get("vise") and a["auteur"] == agent:
                if c.get("action") == "retirer":
                    a["statut"] = "retire"
                elif c.get("enonce"):
                    a["enonce"] = c["enonce"]
                ajouts.append(f"{c.get('action')} {a['id']}")
    for n, v in D.items():
        ecrire(fiche, n, v)
    inc = e.get("incertitudes") or []
    journaliser(fiche, agent, phase, f"a ajouté {', '.join(ajouts) or 'rien de nouveau'}"
                + (f" ; incertitudes signalées : {len(inc)}" if inc else ""))
    if inc:
        etat.setdefault("incertitudes", []).extend({"agent": agent, "texte": t} for t in inc)
        ecrire(fiche, "etat", etat)
    print(f"FUSIONNÉ {chemin} : {len(ajouts)} éléments ({', '.join(ajouts)})")
    return True


def fusion_verif(fiche, e, D):
    faits = []
    idx = {x["id"]: x for n in ("sources", "affirmations", "objections") for x in D[n]}
    for s in e.get("sources", []) or []:
        x = idx.get(s["id"])
        if not x:
            print(f"  ignoré : {s['id']} inconnu"); continue
        x["statut"], x["note_verif"] = s["statut"], s["note"]
        if s.get("date_corrigee"):
            x["date"] = str(s["date_corrigee"])
        faits.append(f"{s['id']}→{s['statut']}")
    for f in e.get("affirmations", []) or []:
        x = idx.get(f["id"])
        if not x:
            print(f"  ignoré : {f['id']} inconnu"); continue
        v = f.get("verdict")
        if v not in VERDICTS[x["type"]]:
            print(f"REFUSÉ : {f['id']} ({x['type']}) verdict « {v} » hors échelle {sorted(map(str, VERDICTS[x['type']]))}")
            return False
        x["verdict"], x["explication"] = v, f["explication"]
        x["statut"] = "inverifiable" if v in ("Invérifiable", "Pas d'estimation fiable") else "verifiee"
        faits.append(f"{f['id']}→{v or 'valeur, sans verdict'}")
    for o in e.get("objections", []) or []:
        x = idx.get(o["id"])
        if not x:
            print(f"  ignoré : {o['id']} inconnu"); continue
        x["statut"], x["resolution"] = o["statut"], o["resolution"]
        faits.append(f"{o['id']}→{o['statut']}")
    for n, v in D.items():
        ecrire(fiche, n, v)
    journaliser(fiche, "verificateur", str(e.get("phase", "3")), "a tranché " + ", ".join(faits))
    print(f"FUSIONNÉ vérification : {len(faits)} décisions")
    return True


# ---------------------------------------------------------------- lots

def lot(fiche, sorte, agent=None, taille=0):
    D = {n: charger(fiche, n) for n in FICHIERS if n != "journal"}
    lots = dossier(fiche) / "lots"
    lots.mkdir(exist_ok=True)
    src = {s["id"]: s for s in D["sources"]}
    if sorte == "verif":
        a_verif = [s for s in D["sources"] if s["statut"] == "a-verifier"]
        aff = [f for f in D["affirmations"] if f["verdict"] is None and f["statut"] != "verifiee"]
        objs = [o for o in D["objections"] if o["statut"] == "transmise-verificateur"]
        # une source à vérifier + toutes les affirmations qui la citent : la page n'est ouverte qu'une fois
        paquets = []
        for s in a_verif:
            paquets.append({"source": {k: s[k] for k in ("id", "titre", "auteur", "date", "adresse", "niveau")},
                            "a_controler": [{"affirmation": f["id"], "enonce": f["enonce"], "type": f["type"],
                                             "extrait_annonce": x["extrait"]}
                                            for f in D["affirmations"] for x in f["sources"]
                                            if x["source"] == s["id"] and f["verdict"] is None]})
        restant = [{"id": f["id"], "enonce": f["enonce"], "type": f["type"],
                    "sources": [{"source": x["source"], "niveau": src[x["source"]]["niveau"], "statut": src[x["source"]]["statut"],
                                 "note_verif": src[x["source"]]["note_verif"], "extrait": x["extrait"]}
                                for x in f["sources"]]} for f in aff]
        cibles = {x["id"]: x for n in ("arguments", "affirmations", "sources") for x in D[n]}
        objections = [{**{k: o[k] for k in ("id", "vise", "auteur", "contenu", "sources", "ce_que_la_source_ne_dit_pas")},
                       "element_vise": cibles.get(o["vise"]),
                       "sources_detail": [src[s] for s in o["sources"] if s in src]} for o in objs]
        decoupe = [paquets[i:i + taille] for i in range(0, len(paquets), taille)] if taille else [paquets]
        ecrits = []
        for i, part in enumerate(decoupe or [[]], 1):
            data = {"sources_a_verifier": part}
            if not taille and not a_verif or (not taille and i == len(decoupe or [[]])):
                # verdicts seulement dans un lot non découpé ; avec --taille, les lots ne portent
                # que les sources, et un lot final (relancer sans --taille) attribue les verdicts
                data["verdicts_a_attribuer"] = restant
                data["objections_a_trancher"] = objections
            p = lots / f"verif-{dt.datetime.now():%H%M%S}-{i}.yaml"
            p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))
            ecrits.append(str(p.relative_to(RACINE)))
        print("\n".join(ecrits))
        print(f"{len(a_verif)} sources, {len(restant)} affirmations, {len(objections)} objections")
        return
    affs = {f["id"]: f for f in D["affirmations"]}

    def vue_arg(a):
        return {"id": a["id"], "auteur": a["auteur"], "question": a["question"], "position": a["position"],
                "enonce": a["enonce"], "porte_par": a["porte_par"], "repond_a": a.get("repond_a"), "statut": a["statut"],
                "affirmations": [{"id": f, "enonce": affs[f]["enonce"], "type": affs[f]["type"],
                                  "verdict": affs[f]["verdict"], "explication": affs[f]["explication"],
                                  "sources": [{"source": x["source"], "extrait": x["extrait"],
                                               "statut_source": src[x["source"]]["statut"]} for x in affs[f]["sources"]]}
                                 for f in a["affirmations"] if f in affs]}
    if sorte == "confrontation":
        data = {"questions": D["questions"],
                "tes_arguments": [vue_arg(a) for a in D["arguments"] if a["auteur"] == agent and a["statut"] != "retire"],
                "arguments_des_autres": [vue_arg(a) for a in D["arguments"] if a["auteur"] != agent and a["statut"] != "retire"],
                "objections_deja_posees": [{k: o[k] for k in ("id", "vise", "auteur", "contenu", "statut", "resolution")}
                                           for o in D["objections"]],
                "sources": {s["id"]: f"{s['titre']} ({s['auteur']}, {s['date']}, niveau {s['niveau']}) — {s['statut']}"
                            for s in D["sources"]}}
        p = lots / f"confrontation-{agent}.yaml"
    elif sorte == "redaction":
        args = [a for a in D["arguments"] if a["statut"] != "retire"]
        data = {"questions": [{**q, "arguments": [vue_arg(a) for a in args if a["question"] == q["id"]],
                               "valeurs": [v for v in D["valeurs"] if v["question"] == q["id"]]}
                              for q in D["questions"]],
                "objections": D["objections"],
                "sources": D["sources"]}
        p = lots / "redaction.yaml"
    else:
        sys.exit(f"lot inconnu : {sorte}")
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))
    print(p.relative_to(RACINE))


# ---------------------------------------------------------------- état

def etat(fiche):
    D = {n: charger(fiche, n) for n in FICHIERS}
    E = charger(fiche, "etat")
    passage = E.get("passage", 1)
    print(f"Fiche {fiche} — phase {E.get('phase')} — passage {passage}")
    for n in ("questions", "arguments", "affirmations", "sources", "objections", "valeurs"):
        c = {}
        for x in D[n]:
            c[x.get("statut", "—")] = c.get(x.get("statut", "—"), 0) + 1
        print(f"  {n:13} {len(D[n]):3}  {c}")
    nouveaux = [x["id"] for n in ("arguments", "objections") for x in D[n] if x.get("passage") == passage]
    ouvertes = [o["id"] for o in D["objections"] if o["nature"] == "fait" and o["statut"] not in STATUTS_OBJ]
    non_verif = [s["id"] for s in D["sources"] if s["statut"] == "a-verifier"]
    sans_verdict = [f["id"] for f in D["affirmations"] if f["verdict"] is None and f["type"] != "valeur"]
    print("Condition d'arrêt :")
    print(f"  1. aucun nouvel argument ni objection au dernier passage : {'oui' if not nouveaux else 'non (' + ', '.join(nouveaux) + ')'}")
    print(f"  2. objections factuelles toutes tranchées : {'oui' if not ouvertes else 'non (' + ', '.join(ouvertes) + ')'}")
    for q in D["questions"]:
        pos = sorted({a["position"] for a in D["arguments"] if a["question"] == q["id"] and a["statut"] != "retire"})
        print(f"  3. {q['id']} positions argumentées : {pos or 'aucune'}")
    print(f"  sources non vérifiées : {non_verif or 'aucune'} ; affirmations sans verdict : {sans_verdict or 'aucune'}")


# ---------------------------------------------------------------- mesures

def ecrire_mesures(fiche):
    E = charger(fiche, "etat")
    L = [f"# Mesures — {fiche}", "",
         "Relevé automatique (`outils/dossier.py`). Durées en temps réel, de l'horloge de la session. "
         "Jetons et appels d'outils : tels que renvoyés par l'outil de lancement des agents.", "",
         "## Par phase", "", "| Phase | Début | Fin | Durée | Passages | Agents lancés | Jetons | Note |",
         "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for ph, m in (E.get("phases") or {}).items():
        d = "—"
        if m.get("debut") and m.get("fin"):
            s = int((dt.datetime.fromisoformat(m["fin"]) - dt.datetime.fromisoformat(m["debut"])).total_seconds())
            d = f"{s // 60} min {s % 60:02d} s"
        ag = [x for x in E.get("agents", []) if str(x["phase"]) == str(ph)]
        jet = sum(x.get("jetons") or 0 for x in ag)
        L.append(f"| {ph}. {PHASES.get(str(ph).split('-')[0], '')} | {m.get('debut', '—')} | {m.get('fin', '—')} | {d} | "
                 f"{m.get('passages', 1)} | {len(ag)} | {jet or '—'} | {m.get('note', '')} |")
    L += ["", "## Par agent", "", "| Phase | Agent | Jetons | Appels d'outils | Durée |", "| --- | --- | --- | --- | --- |"]
    for x in E.get("agents", []):
        ms = x.get("duree_ms")
        L.append(f"| {x['phase']} | {x['agent']} | {x.get('jetons') or '—'} | {x.get('outils') or '—'} | "
                 f"{f'{ms // 60000} min {ms // 1000 % 60:02d} s' if ms else '—'} |")
    (RACINE / "fiches" / fiche / "mesures.md").write_text("\n".join(L) + "\n")


def chrono(fiche, quand, phase, note=None):
    E = charger(fiche, "etat")
    m = E.setdefault("phases", {}).setdefault(str(phase), {})
    m[quand] = maintenant()
    if quand == "debut":
        m["passages"] = m.get("passages", 0) + 1
        E["phase"] = str(phase)
    if note:
        m["note"] = note
    ecrire(fiche, "etat", E)
    journaliser(fiche, "coordinateur", str(phase), f"{quand} de la phase {phase}" + (f" ({note})" if note else ""))
    ecrire_mesures(fiche)
    print(f"phase {phase} : {quand} {m[quand]}")


def mesure(fiche, phase, agent, jetons, outils, duree):
    E = charger(fiche, "etat")
    E.setdefault("agents", []).append({"phase": str(phase), "agent": agent, "jetons": jetons,
                                       "outils": outils, "duree_ms": duree})
    ecrire(fiche, "etat", E)
    ecrire_mesures(fiche)


def journal_md(fiche):
    j = charger(fiche, "journal")
    L = [f"# Journal — {fiche}", "", "Généré à partir de `dossier/journal.yaml`. Chaque action de chaque agent, datée.", "",
         "| Date | Phase | Agent | Action |", "| --- | --- | --- | --- |"]
    L += [f"| {x['date']} | {x['phase']} | {x['agent']} | {x['action']} |" for x in j]
    (RACINE / "fiches" / fiche / "journal.md").write_text("\n".join(L) + "\n")
    print(f"journal.md : {len(j)} entrées")


def init(fiche, question, qtype, theme, sujet, validee_par):
    d = dossier(fiche)
    (d / "entrees").mkdir(parents=True, exist_ok=True)
    (d / "lots").mkdir(exist_ok=True)
    qs = charger(fiche, "questions")
    qid = prochain(qs, "Q")
    qs.append({"id": qid, "enonce": question, "type": qtype, "fiche": fiche, "sujet": sujet, "theme": theme,
               "proposee_par": "fondateur", "statut": "validee"})
    ecrire(fiche, "questions", qs)
    for n in FICHIERS:
        if not (d / f"{n}.yaml").exists():
            ecrire(fiche, n, [])
    E = charger(fiche, "etat")
    E.update({"fiche": fiche, "phase": E.get("phase", "1"), "passage": E.get("passage", 1)})
    ecrire(fiche, "etat", E)
    journaliser(fiche, "coordinateur", "1", f"question {qid} ajoutée, validée par {validee_par}")
    print(f"{qid} créée dans {d.relative_to(RACINE)}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("init"); x.add_argument("fiche"); x.add_argument("--question", required=True)
    x.add_argument("--type", required=True, choices=sorted(TYPES)); x.add_argument("--theme", required=True)
    x.add_argument("--sujet", required=True); x.add_argument("--validee-par", default="fondateur")
    x = s.add_parser("valider"); x.add_argument("fichier")
    x = s.add_parser("fusionner"); x.add_argument("fiche"); x.add_argument("fichiers", nargs="+")
    x = s.add_parser("lot"); x.add_argument("fiche"); x.add_argument("sorte", choices=["verif", "confrontation", "redaction"])
    x.add_argument("--agent"); x.add_argument("--taille", type=int, default=0)
    x = s.add_parser("etat"); x.add_argument("fiche")
    x = s.add_parser("chrono"); x.add_argument("fiche"); x.add_argument("quand", choices=["debut", "fin"])
    x.add_argument("phase"); x.add_argument("--note")
    x = s.add_parser("mesure"); x.add_argument("fiche"); x.add_argument("phase"); x.add_argument("agent")
    x.add_argument("--jetons", type=int); x.add_argument("--outils", type=int); x.add_argument("--duree-ms", type=int)
    x = s.add_parser("passage"); x.add_argument("fiche")
    x = s.add_parser("journal"); x.add_argument("fiche")
    a = p.parse_args()
    if a.cmd == "init":
        init(a.fiche, a.question, a.type, a.theme, a.sujet, a.validee_par)
    elif a.cmd == "valider":
        err = valider_entree(lire_entree(a.fichier))
        print("VALIDE" if not err else "ERREURS :\n  - " + "\n  - ".join(err))
        sys.exit(1 if err else 0)
    elif a.cmd == "fusionner":
        ok = all([fusionner(a.fiche, f) for f in a.fichiers])
        sys.exit(0 if ok else 1)
    elif a.cmd == "lot":
        lot(a.fiche, a.sorte, a.agent, a.taille)
    elif a.cmd == "etat":
        etat(a.fiche)
    elif a.cmd == "chrono":
        chrono(a.fiche, a.quand, a.phase, a.note)
    elif a.cmd == "mesure":
        mesure(a.fiche, a.phase, a.agent, a.jetons, a.outils, a.duree_ms)
    elif a.cmd == "passage":  # nouveau passage de confrontation
        E = charger(a.fiche, "etat"); E["passage"] = E.get("passage", 1) + 1; ecrire(a.fiche, "etat", E)
        journaliser(a.fiche, "coordinateur", E.get("phase", "4"), f"début du passage {E['passage']}")
        print(f"passage {E['passage']}")
    elif a.cmd == "journal":
        journal_md(a.fiche)


if __name__ == "__main__":
    main()
