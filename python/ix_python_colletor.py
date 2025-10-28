################### Marcus Rônney - Linkedin:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
import re
import requests
from bs4 import BeautifulSoup

URL = "https://status.ix.br"
UA  = "Mozilla/5.0 (+ixbr-monitor; marcusronney@outlook.com)"

OK_WORDS = { # Deixei em PT e EN pois são as linguagens mais comuns em navegadores
    "operacional",      # PT
    "operational"       # EN
}

def fetch_html():
    r = requests.get(URL, headers={"User-Agent": UA}, timeout=15) # Aguarda 15 segundos para o GET.
    r.raise_for_status() #Falhas HTTP
    r.encoding = r.apparent_encoding or "utf-8" # Ajustando o Enconding
    return r.text

def norm(txt: str) -> str: # Normalizando o formato e tirando espaços com strip e identano.
    return re.sub(r"\s+", " ", (txt or "")).strip()

def status_to_bit(status_text: str) -> int: # Definindo 1 para OK, se não 0.
    s = norm(status_text).lower()
    return 1 if s in OK_WORDS else 0 

def parse_all(html: str): # Extraindo nome e Status de cada IX.
    """
    Retorna lista de dicts: [{"name": "IX.br Aracaju, SE", "status": "Operacional", "bit": 1}, ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    out = []

    # Cada grupo contém <ul class="list-group components"> com <li class="list-group-item">…</li>
    for ul in soup.find_all("ul", {"class": "list-group components"}) or []:
        # Dentro do UL, cada LI é um IX
        for li in ul.find_all("li", {"class": "list-group-item"}) or []:
            # Nome do IX = texto do LI menos o <small> do status
            small = li.find("small", {"class": "text-component-1"})
            status_text = norm(small.get_text()) if small else ""
            if small:
                small.extract()  # remove pra facilitar pegar o nome limpo

            name = norm(li.get_text())
            if not name:
                continue

            out.append({
                "name": name,
                "status": status_text,
                "bit": status_to_bit(status_text),
            })

    return out

def main():
    ap = argparse.ArgumentParser(description="Scrape status.ix.br e retornar 0/1 por IX")
    ap.add_argument("--name", help="Filtro por nome (trecho). Ex: --name 'Aracaju' (retorna 0/1 único)")
    ap.add_argument("--json", action="store_true", help="Força saída JSON completa mesmo sem --name")
    args = ap.parse_args()

    try:
        html = fetch_html()
    except Exception as e:
        # Para Zabbix: em erro, retorne 0 (ou ajuste conforme sua política)
        print("0" if args.name else json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    items = parse_all(html)

    if args.name:
        # Procura por substring (case-insensitive) no nome
        needle = args.name.lower()
        matches = [i for i in items if needle in i["name"].lower()]
        if not matches:
            # Se não achar, devolve 0 (ou 1, se preferir 'desconhecido=ok')
            print("0")
            return
        # Se houver vários, retorna 0 se QUALQUER um não estiver operacional; senão 1
        bit = 1 if all(i["bit"] == 1 for i in matches) else 0
        print(str(bit))
    else:
        # Saída JSON: { "IX.br Aracaju, SE": 1, ... } + campos extras
        result = {
            "data": [
                {"name": i["name"], "status": i["status"], "bit": i["bit"]}
                for i in items
            ],
            "as_map": {i["name"]: i["bit"] for i in items}
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Saída simples e enxuta por padrão
            print(json.dumps(result["as_map"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
