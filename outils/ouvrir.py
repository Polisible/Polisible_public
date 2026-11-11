#!/usr/bin/env python3
"""Ouvre une source web et n'en renvoie que l'utile.

Usage :
  python3 outils/ouvrir.py URL [--cherche "mot1|mot2"] [--fenetre 300] [--max 6]

Affiche : statut HTTP, adresse finale, titre, date trouvée dans les métadonnées,
puis, si --cherche est donné, au plus --max passages autour des mots cherchés
(expression régulière, insensible à la casse). Sans --cherche : les 1 500
premiers caractères du texte. Gère le HTML et le PDF (via pdftotext).
Règle 3 de CLAUDE.md : on extrait, on ne recharge pas la page entière.
"""
import argparse, re, subprocess, sys, tempfile, urllib.request, urllib.error

UA = "Mozilla/5.0 (compatible; Polisible-verification/0.1)"

def telecharger(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr,en;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, r.geturl(), r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, url, "", b""
    except Exception as e:  # réseau, DNS, TLS
        print(f"INACCESSIBLE : {type(e).__name__}: {e}")
        sys.exit(2)

def texte_pdf(octets):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(octets); f.flush()
        out = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True)
        return "", "", out.stdout.decode("utf-8", "replace")

def texte_html(octets):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(octets, "html.parser")
    titre = soup.title.get_text(strip=True) if soup.title else ""
    date = ""
    for attr in ("article:published_time", "date", "dc.date", "DC.date", "citation_publication_date", "og:updated_time"):
        m = soup.find("meta", attrs={"property": attr}) or soup.find("meta", attrs={"name": attr})
        if m and m.get("content"):
            date = m["content"]; break
    for t in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        t.decompose()
    return titre, date, soup.get_text(" ")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--cherche")
    p.add_argument("--fenetre", type=int, default=300)
    p.add_argument("--max", type=int, default=6)
    a = p.parse_args()
    statut, finale, ctype, octets = telecharger(a.url)
    print(f"STATUT : {statut}\nADRESSE FINALE : {finale}")
    if statut >= 400 or not octets:
        print("INACCESSIBLE : le site a refusé ou n'a rien renvoyé."); sys.exit(2)
    if "pdf" in ctype or octets[:4] == b"%PDF":
        titre, date, texte = texte_pdf(octets)
    else:
        titre, date, texte = texte_html(octets)
    texte = re.sub(r"\s+", " ", texte).strip()
    print(f"TITRE : {titre}\nDATE (métadonnées) : {date or 'non trouvée'}\nLONGUEUR : {len(texte)} caractères")
    if not a.cherche:
        print("DÉBUT :", texte[:1500]); return
    n = 0
    for m in re.finditer(a.cherche, texte, re.I):
        d, f = max(0, m.start() - a.fenetre), min(len(texte), m.end() + a.fenetre)
        print(f"--- passage {n+1} (car. {m.start()}) ---\n…{texte[d:f]}…")
        n += 1
        if n >= a.max: break
    if n == 0:
        print("AUCUN PASSAGE trouvé pour :", a.cherche)

if __name__ == "__main__":
    main()
