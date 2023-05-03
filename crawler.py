import hashlib
import requests
from bs4 import BeautifulSoup
import sys


def gerar_md5(link_pdf, conf):
    hashes = {}
    response = requests.get(link_pdf, headers=conf, timeout=TimeoutError)
    pdf_content = response.content

    md5_hash = hashlib.md5(pdf_content).hexdigest()
    hashes[md5_hash] = link_pdf
    return print(hashes)


def get_request(link_atual, conf):
    response = requests.get(link_atual, headers=conf, timeout=60)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


# entrada do usuario
data = input()
data_inicial = data
data_final = data

# necessário para que o servidor não bloqueie acesso
user_agent = {}
url = f"""https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?
        tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&
        dataInicial={data_inicial}
        &dataFinal={data_final}
        &tipoPesquisaDJ=&argumento="""

# pega as listas com os links
CONTAINER = "result__container--simples"
lista_de_links = get_request(url, user_agent).find("ul", {"class": CONTAINER})

# acessando as listas que contém links e extraindo-os
url_DJe = []
for link in lista_de_links:
    links_DJe = link.find("a")["href"]
    url_DJe.append("https://portal.stf.jus.br/servicos/dje/" + str(links_DJe))

# iterando pelos links da lista
pdf_url = []
for link in url_DJe:
    pdf_links = get_request(link, user_agent)
    pdf_links.find_all("a", {"target": "_blank"})
    for pdf_link in pdf_links:
        if "Integral" in pdf_link.text:
            pdf_url.append("https://portal.stf.jus.br" + str(pdf_link["href"]))

# iterando pela lista de pdf e gerando o hashcode MD5
for link in pdf_url:
    gerar_md5(link, user_agent)
