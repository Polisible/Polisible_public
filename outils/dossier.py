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
  lot <fiche> bibliotheque                 textes de base communs, transmis aux experts
  cadrage <fiche> <fichier>                fusion des questions proposées, décision du fondateur
  a-relancer <fiche> <expert>...           confrontation ciblée : qui relancer au passage suivant
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
ROLES = {"expert", "verificateur", "bibliothecaire"}
# Partis de chaque famille (porte_par d'un expert : un parti de SA famille, ou un de ses membres).
# Un autre parti de la famille : parti_hors_liste: true + justification, signalé au fondateur.
FAMILLES = {
    "expert-extreme-gauche": {"LO", "Lutte ouvrière", "NPA", "NPA-L'Anticapitaliste", "NPA-Révolutionnaires"},
    "expert-gauche-radicale": {"LFI", "La France insoumise", "PCF", "Parti communiste français"},
    "expert-sociaux-democrates": {"PS", "Parti socialiste", "Place publique"},
    "expert-ecologistes": {"Les Écologistes", "EELV"},
    "expert-centre": {"Renaissance", "MoDem", "Horizons", "UDI", "Ensemble"},
    "expert-droite": {"LR", "Les Républicains"},
    "expert-extreme-droite": {"RN", "Rassemblement national", "UDR", "Reconquête"},
}
# Recherche minimale avant de conclure « sans position » : chaque catégorie doit être consultée.
LIEUX_MINIMUM = {"programme", "site", "dirigeants", "parlement"}
STATUTS_OBJ = {"resolue", "remontee-fondateur"}
EXTRAIT_MAX = 320  # une phrase au plus (règle de citation courte, dépôt public)
FICHIERS = ["questions", "arguments", "affirmations", "sources", "objections", "valeurs", "journal"]
PREFIXE = {"arguments": "A", "affirmations": "F", "sources": "S", "objections": "O", "valeurs": "V", "questions": "Q"}
ID_GLOBAL = re.compile(r"^[AFSOVQ]\d+$")
# une affirmation porte sur le fond ; « X a dit que… » va dans porte_par (sauf declaration: true)
DECLARATIF = re.compile(r"\b(a|ont) (déclaré|écrit|dit|jugé|qualifié|estimé|affirmé|souligné|indiqué|rappelé|averti|proposé)\b|"
                        r"\b(déclare|qualifie|affirme|estime|juge|écrit|souligne|dénonce)\b|"
                        r"\bselon (lui|elle|eux|un|une|le|la|les|l'|[A-Z])|\b(estime|juge|considère|affirme) que\b", re.I)
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

def role_de(e):
    if e.get("role"):
        return e["role"]
    return {"verificateur": "verificateur", "bibliothecaire": "bibliothecaire"}.get(e.get("agent"), "expert")


def valider_entree(e):
    """Renvoie la liste des erreurs d'un dépôt (vide si correct)."""
    err = []
    if not isinstance(e, dict):
        return ["le fichier doit être un dictionnaire YAML"]
    if not e.get("agent"):
        err.append("champ « agent » manquant")
    role = role_de(e)
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
        if role == "bibliothecaire" and s.get("niveau") not in (1, 2):
            err.append(f"source {s.get('ref')} : la bibliothèque commune ne contient que des sources de niveau 1 ou 2")
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
        if DECLARATIF.search(str(f.get("enonce", ""))) and not f.get("declaration"):
            err.append(f"affirmation {f.get('ref')} : énoncé déclaratif (« X a dit que… »). Écris le fond vérifiable ; "
                       "la déclaration va dans porte_par. Si le fait à établir EST la déclaration, ajoute declaration: true")
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
    if role == "bibliothecaire" and (e.get("arguments") or e.get("objections") or e.get("valeurs")):
        err.append("la bibliothèque ne dépose que des sources et des affirmations de fait, sans argument")
    for a in e.get("arguments", []) or []:
        for c in ("ref", "question", "position", "enonce", "raisonnement", "porte_par", "affirmations"):
            if not a.get(c):
                err.append(f"argument {a.get('ref', '?')} : champ « {c} » manquant")
        if a.get("position") not in POSITIONS:
            err.append(f"argument {a.get('ref')} : position doit être {sorted(POSITIONS)}")
        for p in a.get("porte_par", []) or []:
            if not isinstance(p, dict) or not p.get("qui") or not p.get("source") or not p.get("parti"):
                err.append(f"argument {a.get('ref')} : porte_par = liste de {{qui, parti, source}}")
                continue
            fam = FAMILLES.get(e.get("agent"))
            if fam and p["parti"] not in fam and not (p.get("parti_hors_liste") and p.get("justification")):
                err.append(f"argument {a.get('ref')} : « {p['parti']} » n'est pas un parti de ta famille ({', '.join(sorted(fam))}). "
                           "Un argument n'est porté que par un parti de ta famille ou un de ses membres ; une institution "
                           "ou un groupe de réflexion ne porte pas l'argument d'une famille. Autre parti de la famille : "
                           "parti_hors_liste: true et justification.")
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
    for s in e.get("sources_ajoutees", []) or []:
        if role != "verificateur":
            err.append("sources_ajoutees : réservé au vérificateur")
        for c in ("titre", "auteur", "date", "adresse", "niveau", "pour", "extrait"):
            if not s.get(c):
                err.append(f"sources_ajoutees : champ « {c} » manquant ({s.get('adresse')})")
        if len(str(s.get("extrait", ""))) > EXTRAIT_MAX:
            err.append("sources_ajoutees : extrait trop long (une phrase au plus)")
    for x in e.get("sans_position", []) or []:
        if not x.get("question"):
            err.append(f"sans_position : « question » obligatoire ({x})")
        lieux = x.get("lieux_consultes") or []
        vus = {str(l.get("categorie")) for l in lieux if isinstance(l, dict) and l.get("ou") and l.get("resultat")}
        if not LIEUX_MINIMUM <= vus:
            err.append(f"sans_position sur {x.get('question')} : recherche minimale incomplète, il manque "
                       f"{sorted(LIEUX_MINIMUM - vus)} (lieux_consultes : liste de {{categorie, ou, resultat}})")
    for x in e.get("sources_demandees", []) or []:
        if not str(x.get("adresse", "")).startswith("http") or not x.get("pourquoi") or not x.get("erreur"):
            err.append(f"sources_demandees : « adresse », « pourquoi » et « erreur » obligatoires ({x})")
    for q in e.get("questions_proposees", []) or []:
        if not q.get("enonce") or q.get("type") not in TYPES or not q.get("pourquoi"):
            err.append(f"questions_proposees : enonce, type ({sorted(TYPES)}) et pourquoi obligatoires ({q})")
        elif not str(q["enonce"]).rstrip().endswith("?"):
            err.append(f"questions_proposees : l'énoncé doit être une question fermée (oui ou non) : {q['enonce']}")
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
    if role_de(e) == "verificateur":
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
                                  "declaration": bool(f.get("declaration")),
                                  "auteur": agent, "passage": passage, "verdict": None, "explication": None,
                                  "statut": "en-attente"})
        ajouts.append(fid)
    for a in e.get("arguments", []) or []:
        aid = prochain(D["arguments"], "A")
        carte[a["ref"]] = aid
        D["arguments"].append({"id": aid, "question": a["question"], "position": a["position"], "enonce": a["enonce"],
                               "porte_par": [{"qui": p["qui"], "parti": p["parti"], "source": res(p["source"]),
                                              **({"parti_hors_liste": True, "justification": p["justification"]}
                                                 if p.get("parti_hors_liste") else {})} for p in a["porte_par"]],
                               "affirmations": [res(x) for x in a["affirmations"]],
                               "raisonnement": re.sub(r"\b[a-z]\d+\b", lambda m: carte.get(m.group(0), m.group(0)), a["raisonnement"]),
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
    for q in e.get("questions_proposees", []) or []:
        qid = prochain(D["questions"], "Q")
        D["questions"].append({"id": qid, "enonce": q["enonce"], "type": q["type"], "pourquoi": q["pourquoi"],
                               "proposee_par": [agent], "statut": "proposee"})
        ajouts.append(f"{qid} (proposée)")
    for x in e.get("sans_position", []) or []:
        for q in D["questions"]:
            if q["id"] == x["question"]:
                q.setdefault("sans_position", []).append({"auteur": agent, "lieux_consultes": x["lieux_consultes"]})
                ajouts.append(f"sans position sur {q['id']}")
    for x in e.get("sources_demandees", []) or []:
        if any(norm_url(s["adresse"]) == norm_url(x["adresse"]) for s in D["sources"]):
            continue
        sid = prochain(D["sources"], "S")
        D["sources"].append({"id": sid, "titre": x.get("titre", "(à établir)"), "auteur": x.get("auteur", "(à établir)"),
                             "date": str(x.get("date", "(à établir)")), "adresse": x["adresse"], "niveau": x.get("niveau"),
                             "ajoutee_par": agent, "statut": "demandee", "demande": {"pourquoi": x["pourquoi"], "erreur": x["erreur"]},
                             "note_verif": None})
        ajouts.append(f"{sid} (demandée)")
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
        for c in ("titre", "auteur", "niveau"):
            if s.get(c):
                x[c] = s[c]
        if s.get("date_corrigee"):
            x["date"] = str(s["date_corrigee"])
        faits.append(f"{s['id']}→{s['statut']}")
    for s in e.get("sources_ajoutees", []) or []:  # source officielle trouvée en vérifiant
        exist = next((x for x in D["sources"] if norm_url(x["adresse"]) == norm_url(s["adresse"])), None)
        sid = exist["id"] if exist else prochain(D["sources"], "S")
        if not exist:
            D["sources"].append({"id": sid, "titre": s["titre"], "auteur": s["auteur"], "date": str(s["date"]),
                                 "adresse": s["adresse"], "niveau": s["niveau"], "ajoutee_par": "verificateur",
                                 "statut": "conforme", "note_verif": "ajoutée par le vérificateur"})
        cible = idx.get(s["pour"])
        if cible:
            cible["sources"].append({"source": sid, "extrait": s["extrait"]})
        faits.append(f"{sid} ajoutée pour {s['pour']}")
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
        a_verif = [s for s in D["sources"] if s["statut"] in ("a-verifier", "demandee")]
        aff = [f for f in D["affirmations"] if f["verdict"] is None and f["statut"] != "verifiee"]
        objs = [o for o in D["objections"] if o["statut"] == "transmise-verificateur"]
        # une source à vérifier + toutes les affirmations qui la citent : la page n'est ouverte qu'une fois
        paquets = []
        for s in a_verif:
            paquets.append({"source": {k: s.get(k) for k in ("id", "titre", "auteur", "date", "adresse", "niveau", "statut", "demande")},
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
                "enonce": a["enonce"], "raisonnement": a.get("raisonnement"), "porte_par": a["porte_par"],
                "repond_a": a.get("repond_a"), "statut": a["statut"],
                "affirmations": [{"id": f, "enonce": affs[f]["enonce"], "type": affs[f]["type"],
                                  "verdict": affs[f]["verdict"], "explication": affs[f]["explication"],
                                  "sources": [{"source": x["source"], "extrait": x["extrait"],
                                               "statut_source": src[x["source"]]["statut"]} for x in affs[f]["sources"]]}
                                 for f in a["affirmations"] if f in affs]}
    if sorte == "bibliotheque":
        data = {"note": "Bibliothèque commune : textes de base de niveau 1 ou 2, vérifiés. Tu peux citer ces ids, "
                        "et tu restes libre de chercher et citer toute autre source.",
                "affirmations": [{"id": f["id"], "enonce": f["enonce"], "verdict": f["verdict"],
                                  "sources": [{"source": x["source"], "extrait": x["extrait"]} for x in f["sources"]]}
                                 for f in D["affirmations"] if f["auteur"] == "bibliothecaire"],
                "sources": {s["id"]: f"{s['titre']} ({s['auteur']}, {s['date']}, niveau {s['niveau']}) — {s['adresse']}"
                            for s in D["sources"] if s["ajoutee_par"] == "bibliothecaire"}}
        p = lots / "bibliotheque.yaml"
    elif sorte == "confrontation":
        data = {"questions": [q for q in D["questions"] if q["statut"] == "validee"],
                "tes_arguments": [vue_arg(a) for a in D["arguments"] if a["auteur"] == agent and a["statut"] != "retire"],
                "arguments_des_autres": [vue_arg(a) for a in D["arguments"] if a["auteur"] != agent and a["statut"] != "retire"],
                "objections_deja_posees": [{k: o[k] for k in ("id", "vise", "auteur", "contenu", "statut", "resolution")}
                                           for o in D["objections"]],
                "tes_sources_demandees": [{k: s.get(k) for k in ("id", "adresse", "titre", "statut", "note_verif")}
                                          for s in D["sources"] if s["ajoutee_par"] == agent and s.get("demande")],
                "sources": {s["id"]: f"{s['titre']} ({s['auteur']}, {s['date']}, niveau {s['niveau']}) — {s['statut']}"
                            for s in D["sources"]}}
        p = lots / f"confrontation-{agent}.yaml"
    elif sorte == "redaction":
        args = [a for a in D["arguments"] if a["statut"] != "retire"]
        data = {"questions": [{**q, "arguments": [vue_arg(a) for a in args if a["question"] == q["id"]],
                               "valeurs": [v for v in D["valeurs"] if v["question"] == q["id"]]}
                              for q in D["questions"] if q["statut"] == "validee"],
                "affirmations_hors_argument": [  # bibliothèque, arguments retirés : utilisables pour contexte et chiffres
                    {k: f[k] for k in ("id", "enonce", "type", "verdict", "explication", "sources")}
                    for f in D["affirmations"] if f["verdict"] is not None
                    and not any(f["id"] in a["affirmations"] for a in args)],
                "objections": D["objections"],
                "sources": D["sources"]}
        p = lots / "redaction.yaml"
    else:
        sys.exit(f"lot inconnu : {sorte}")
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))
    print(p.relative_to(RACINE))


# ---------------------------------------------------------------- état

def cadrage(fiche, chemin):
    """Applique un fichier de cadrage : fusion des questions proposées et décision du fondateur.
    Format : {retenues: [{enonce, type, fusion_de: [Q..]}], ecartees: [{id, raison}], validee_par: "..."}"""
    c = lire_entree(chemin)
    qs = charger(fiche, "questions")
    idx = {q["id"]: q for q in qs}
    for q in c.get("retenues", []):
        sources = [idx[i] for i in q["fusion_de"]]
        qid = prochain(qs, "Q")
        qs.append({"id": qid, "enonce": q["enonce"], "type": q["type"], "fiche": fiche,
                   "proposee_par": sorted({a for s in sources for a in s["proposee_par"]}),
                   "fusion_de": q["fusion_de"], "statut": "validee"})
        for s in sources:
            s["statut"] = f"fusionnee dans {qid}"
        journaliser(fiche, "coordinateur", "1", f"{qid} validée par {c['validee_par']} (fusion de {', '.join(q['fusion_de'])})")
    for x in c.get("ecartees", []):
        idx[x["id"]]["statut"] = "ecartee"
        idx[x["id"]]["raison"] = x["raison"]
        journaliser(fiche, "fondateur", "1", f"{x['id']} écartée : {x['raison']}")
    ecrire(fiche, "questions", qs)
    print("\n".join(f"{q['id']} [{q['statut']}] {q['enonce']}" for q in qs))


def a_relancer(fiche, experts):
    """Confrontation ciblée : un expert est relancé s'il est visé par un élément du dernier passage
    (objection ou contre-argument sur ses éléments) ou s'il a lui-même déposé quelque chose à ce passage."""
    D = {n: charger(fiche, n) for n in ("arguments", "affirmations", "objections")}
    passage = charger(fiche, "etat").get("passage", 1)
    auteur = {x["id"]: x["auteur"] for n in D for x in D[n]}
    derniers = [x for n in ("arguments", "objections") for x in D[n] if x.get("passage") == passage]
    vises = {auteur.get(x.get("repond_a") or x.get("vise")) for x in derniers} - {None}
    actifs = {x["auteur"] for x in derniers}
    for ex in experts:
        motif = "visé" if ex in vises else ("a déposé au dernier passage" if ex in actifs else None)
        print(f"{ex}: {'RELANCER (' + motif + ')' if motif else 'pas de relance'}")


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
    non_verif = [s["id"] for s in D["sources"] if s["statut"] in ("a-verifier", "demandee")]
    sans_verdict = [f["id"] for f in D["affirmations"] if f["verdict"] is None and f["type"] != "valeur"]
    print("Condition d'arrêt :")
    print(f"  1. aucun nouvel argument ni objection au dernier passage : {'oui' if not nouveaux else 'non (' + ', '.join(nouveaux) + ')'}")
    print(f"  2. objections factuelles toutes tranchées : {'oui' if not ouvertes else 'non (' + ', '.join(ouvertes) + ')'}")
    for q in [q for q in D["questions"] if q["statut"] == "validee"]:
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
        ag = [x for x in E.get("agents", []) if str(x["phase"]) == str(ph)]  # 3-bis : agents notés « 3-bis »
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
    ph = E.setdefault("phases", {})
    cle = str(phase)
    if quand == "debut":
        n = 1
        while cle in ph and ph[cle].get("fin"):  # phase déjà close : nouvelle ligne (3-bis, 3-ter…)
            n += 1
            cle = f"{phase}-{['', '', 'bis', 'ter', 'quater'][n] if n < 5 else n}"
        E["phase"] = str(phase)
    else:
        ouvertes = [k for k in ph if k.split("-")[0] == str(phase) and not ph[k].get("fin")]
        cle = ouvertes[-1] if ouvertes else cle
    m = ph.setdefault(cle, {})
    m[quand] = maintenant()
    if quand == "debut":
        m["passages"] = 1
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
    if question:
        qid = prochain(qs, "Q")
        qs.append({"id": qid, "enonce": question, "type": qtype, "fiche": fiche,
                   "proposee_par": ["fondateur"], "statut": "validee"})
    ecrire(fiche, "questions", qs)
    for n in FICHIERS:
        if not (d / f"{n}.yaml").exists():
            ecrire(fiche, n, [])
    E = charger(fiche, "etat")
    E.update({"fiche": fiche, "theme": theme, "sujet": sujet, "phase": E.get("phase", "1"), "passage": E.get("passage", 1)})
    ecrire(fiche, "etat", E)
    journaliser(fiche, "coordinateur", "1", f"dossier créé" + (f" ; question {qid} validée par {validee_par}" if question else ""))
    print(f"dossier {d.relative_to(RACINE)} prêt")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("init"); x.add_argument("fiche"); x.add_argument("--question")
    x.add_argument("--type", choices=sorted(TYPES), default="fait"); x.add_argument("--theme", required=True)
    x.add_argument("--sujet", required=True); x.add_argument("--validee-par", default="fondateur")
    x = s.add_parser("valider"); x.add_argument("fichier")
    x = s.add_parser("fusionner"); x.add_argument("fiche"); x.add_argument("fichiers", nargs="+")
    x = s.add_parser("lot"); x.add_argument("fiche"); x.add_argument("sorte", choices=["verif", "confrontation", "redaction", "bibliotheque"])
    x.add_argument("--agent"); x.add_argument("--taille", type=int, default=0)
    x = s.add_parser("etat"); x.add_argument("fiche")
    x = s.add_parser("chrono"); x.add_argument("fiche"); x.add_argument("quand", choices=["debut", "fin"])
    x.add_argument("phase"); x.add_argument("--note")
    x = s.add_parser("mesure"); x.add_argument("fiche"); x.add_argument("phase"); x.add_argument("agent")
    x.add_argument("--jetons", type=int); x.add_argument("--outils", type=int); x.add_argument("--duree-ms", type=int)
    x = s.add_parser("passage"); x.add_argument("fiche")
    x = s.add_parser("journal"); x.add_argument("fiche")
    x = s.add_parser("cadrage"); x.add_argument("fiche"); x.add_argument("fichier")
    x = s.add_parser("a-relancer"); x.add_argument("fiche"); x.add_argument("experts", nargs="+")
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
    elif a.cmd == "cadrage":
        cadrage(a.fiche, a.fichier)
    elif a.cmd == "a-relancer":
        a_relancer(a.fiche, a.experts)


if __name__ == "__main__":
    main()
