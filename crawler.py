import requests
from bs4 import BeautifulSoup

url = "https://portal.stf.jus.br/servicos/dje/pesquisarDiarioJustica.asp"

# necessário para que o servidor não bloqueie acesso
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


response = requests.get(url, headers = user_agent)

# obtem o html da pagina
html = response.content
print(html)