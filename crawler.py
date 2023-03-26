import requests
from bs4 import BeautifulSoup
import hashlib


def gerar_md5(link_pdf):
    lista_hash = []
    response = requests.get(link_pdf, headers=user_agent)
    pdf_content = response.content

    md5_hash = hashlib.md5(pdf_content).hexdigest()
    lista_hash.append(md5_hash)
    return print(lista_hash)


data = input()
data_inicial = data
data_final = data

url = f'https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&dataInicial={data_inicial}&dataFinal={data_final}&tipoPesquisaDJ=&argumento='

# necessário para que o servidor não bloqueie acesso
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


response = requests.get(url, headers = user_agent)

soup = BeautifulSoup(response.content, 'html.parser')


# pega as listas com os links
listas = soup.find('ul', {'class':'result__container--simples'})

url_DJe = []

# acessando as listas que contém links e extraindo-os
for link in listas:
    links_DJe = link.find('a')['href']
    url_DJe.append('https://portal.stf.jus.br/servicos/dje/'+str(links_DJe))


pdf_url = []
# iterando pelos links da lista
for link in url_DJe:
    response_processo = requests.get(link, headers=user_agent)
    
    soup_processo = BeautifulSoup(response_processo.content, 'html.parser')
    pdf_links = soup_processo.find_all('a', {'target': '_blank'})

    for pdf_link in pdf_links:
        if 'Integral' in pdf_link.text:
            pdf_url.append( 'https://portal.stf.jus.br'+str(pdf_link['href']) )
        else:
           pass

for link in pdf_url:
    gerar_md5(link)
