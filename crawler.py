import requests
from bs4 import BeautifulSoup

data_inicial = "2022-12-13"
data_final = "2022-12-25"

url = f'https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&dataInicial={data_inicial}&dataFinal={data_final}&tipoPesquisaDJ=&argumento='

# necessário para que o servidor não bloqueie acesso
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


response = requests.get(url, headers = user_agent)

# obtem o html da pagina
html = response.content


soup = BeautifulSoup(html, 'html.parser')


# pega as listas com os links
listas = soup.find('ul', {'class':'result__container--simples'})

url_DJe = []

# acessando as listas que contém links e extraindo-os
for link in listas:
    links_DJe = link.find('a')['href']
    url_DJe.append('https://portal.stf.jus.br/servicos/dje/'+str(links_DJe))


# fazendo requisição dos links
for link in url_DJe:
    response_processo = requests.get(link, headers=user_agent)
    print(f'link:{link} code:{response_processo.status_code}')