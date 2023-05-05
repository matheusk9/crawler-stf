"""Módulo de execução e instâncias."""
from hashcode import HashCode
from crawler import Crawler


app = Crawler()
dje_do_dia = app.get_url_acesso()
pdf_integral = app.get_url_integral(dje_do_dia)
hashcodes = {}
for url in pdf_integral:
    HashCode.generate(hashcodes, url, app)

print(hashcodes)
