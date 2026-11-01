#!/usr/bin/env python3
"""Gera uma pagina por vendedor a partir de tools/template.html + sellers.json.
Uso: python3 tools/build.py   (na raiz do repositorio)"""
import json, os, re, html

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = open(os.path.join(root, "tools", "template.html"), encoding="utf-8").read()
sellers = json.load(open(os.path.join(root, "sellers.json"), encoding="utf-8"))

def join_cities(c):
    return ", ".join(c[:-1]) + " e " + c[-1] if len(c) > 1 else c[0]

def render(s):
    h = T
    esc = html.escape
    # cidades: texto do cartao do chip fisico
    names = [re.sub(r"\s*\((PB|RN)\)", "", x) for x in s["cities"]]
    h = re.sub(r'<p class="cities">.*?</p>',
               '<p class="cities">Disponível em ' + esc(join_cities(s["cities"])) + '.</p>', h, count=1, flags=re.S)
    # cidades: opcoes do formulario
    opts = "".join("<option>%s</option>" % esc(c) for c in s["cities"])
    h = re.sub(r'(<optgroup label="Minhas cidades de atendimento">\s*).*?(\s*</optgroup>)',
               lambda m: m.group(1) + opts + m.group(2), h, count=1, flags=re.S)
    sd, sdn = s["same_day_city"], s["same_day_name"]
    h = h.replace("<li><strong>São Bento:</strong>", "<li><strong>%s:</strong>" % esc(sdn))
    h = h.replace('val("cidade") === "São Bento (PB)"', 'val("cidade") === %s' % json.dumps(sd, ensure_ascii=False))
    h = h.replace("Em São Bento a entrega", "Em %s a entrega" % sdn)
    # identidade
    h = h.replace("5583999727048", s["phone"])
    h = h.replace("83 9 9972-7048", s["phone_display"])
    h = h.replace("Ivam Alves", s["name"])
    h = h.replace("Olá, Ivam!", "Olá, %s!" % s["first"])
    h = h.replace("<title>Brisanet com Ivam</title>", "<title>Brisanet com %s</title>" % esc(s["first"]))
    og = ('<meta property="og:title" content="Brisanet com %s"><meta property="og:description" '
          'content="Faça seu pré-cadastro Brisanet e fale direto com %s no WhatsApp.">'
          '<meta property="og:type" content="website">') % (esc(s["first"]), esc(s["first"]))
    h = h.replace("</title>", "</title>" + og, 1)
    return h

for s in sellers:
    out = render(s)
    d = os.path.join(root, s["slug"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
    if s.get("default"):
        open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(out)
    print("ok", s["slug"])
