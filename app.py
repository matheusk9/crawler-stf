"""doc"""
import sys
from hashcode import HashCode
from crawler import Crawler


teste = Crawler()
# entrada do usuario
DATA = sys.argv[1]
DATA_INICIAL = DATA
DATA_FINAL = DATA

# necessário para que o servidor não bloqueie acesso
user_agent = {
    "User-agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64)
                AppleWebKit/537.36 (KHTML, like Gecko)
                Chrome/89.0.4389.90
                Safari/537.36"""
}
url = f"""https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?
        tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022
        &dataInicial={DATA_INICIAL}
        &dataFinal={DATA_FINAL}&tipoPesquisaDJ=&argumento="""

# pega as listas com os links
lista_de_links = teste.requisicao(url, user_agent).find(
    "ul", {"class": "result__container--simples"}
)

# acessando as listas que contém links e extraindo-os
url_DJe = []
for link in lista_de_links:
    links_DJe = link.find("a")["href"]
    url_DJe.append("https://portal.stf.jus.br/servicos/dje/" + str(links_DJe))

# iterando pelos links da lista
pdf_url = []
for link in url_DJe:
    pdf_links = teste.requisicao(link, user_agent)
    pdf_links.find_all("a", {"target": "_blank"})
    for pdf_link in pdf_links:
        if "Integral" in pdf_link.text:
            pdf_url.append("https://portal.stf.jus.br" + str(pdf_link["href"]))

# iterando pela lista de pdf e gerando o hashcode MD5
for link in pdf_url:
    HashCode.generate(link, user_agent)
