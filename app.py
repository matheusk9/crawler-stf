"""Módulo de execução e instâncias."""
from src.modules.crawler import Crawler

extracao = Crawler('02-11-2022')

pdf_integral = extracao.obtem_url_integral()

for url in pdf_integral:
    extracao.gera_hashcode(url)
print(extracao.dicionario.items())
