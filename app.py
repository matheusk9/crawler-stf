"""Módulo de execução e instâncias."""
from src.modules.crawler import Crawler

extracao = Crawler()

dje_do_dia = extracao.obtem_url_acesso()
pdf_integral = extracao.obtem_url_integral(dje_do_dia)

for url in pdf_integral:
    extracao.gera_hashcode(url)

hash_codes = extracao.dicionario
print(hash_codes.items())
