"""Módulo de execução e instâncias."""
from src.crawler import Crawler

app = Crawler()
dje_do_dia = app.obtem_url_acesso()
pdf_integral = app.obtem_url_integral(dje_do_dia)
hashcodes = {}
for url in pdf_integral:
    app.gera_hashcode(hashcodes, url)

print(hashcodes)
