"""Modulo de requisições."""
import requests
from bs4 import BeautifulSoup
import hashlib
import sys


class Crawler():
    """Responsavel pela extração dos dados"""

    def __init__(self) -> None:
        self.data = sys.argv[1]
        self.__dicionario = {}
        self.__user_agent = {
            "User-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/89.0.4389.90 Safari/537.36"
            )
        }
        self.__url = (
            "https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?"
            "tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&"
            f"dataInicial={self.data}&dataFinal={self.data}&tipoPesquisaDJ=&argumento="
        )

    @property
    def user_agent(self):
        """Metodo get."""
        return self.__user_agent

    @property
    def url_padrao(self):
        """Metodo get."""
        return self.__url

    @property
    def dicionario(self):
        """Metodo get."""
        return self.__dicionario

    def obtem_soup(self, link=None, time=60):
        """Faz a requisicao do link passado por parametro.

        Response = pega o HTML bruto.
        Soup = retorna um objeto do HTML.
        """

        if link is None:
            link = self.url_padrao
        response = requests.get(url=link, headers=self.user_agent, timeout=time)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def obtem_url_acesso(self):
        """Acesso a primeira pagina.

        Faz o request da primeira pagina e busca pela 'ul' no html.
        Lista_pdf = contém o 'ul' e faz a busca por todos os links contidos ('a').
        Caso não tenha links, retorna a excessão FileNotFoundError e encerra o programa.
        Se não houver excessões, retorna os links na lista 'url'.
        """
        try:
            lista_pdf = self.obtem_soup().find(
                "ul", {"class": "result__container--simples"}
            )

            lista_pdf = lista_pdf.select('a')
            if not lista_pdf:
                raise FileNotFoundError("Não encontrado!")

            url = []
            for item in lista_pdf:
                links_dj = item["href"]
                url.append("https://portal.stf.jus.br/servicos/dje/" + str(links_dj))
            return url
        except FileNotFoundError:
            print("Não existem DJe na data informada! Tente outra data.")

    def obtem_url_integral(self, url: list):
        """Acesso a pagina de PDFs integrais e paginados.

        Busca apenas links de PDFs integrais e armazena na lista pdf_url.
        """

        pdf_url = []
        for link in url:
            integ_pag = self.obtem_soup(link).find_all("a", {"target": "_blank"})
            for pdf_link in integ_pag:
                if "Integral" in pdf_link.text:
                    pdf_url.append("https://portal.stf.jus.br" + str(pdf_link["href"]))
        return pdf_url

    def gera_hashcode(self, link):
        """Faz a requisição do link passado por parâmetro.

        Gera os códigos MD5 e os retorna em um dicionário com seus respectivos links.
        """

        response = requests.get(url=link, headers=self.user_agent, timeout=60)
        pdf_content = response.content
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        self.dicionario[md5_hash] = link
        return self.dicionario
