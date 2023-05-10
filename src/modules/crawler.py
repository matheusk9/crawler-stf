"""Modulo de requisições."""
import requests
from bs4 import BeautifulSoup
import hashlib
import sys


class Crawler:
    """Responsavel pela configuração e requests."""

    def __init__(self):
        self.data = sys.argv[1]
        self._user_agent = {
            "User-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/89.0.4389.90 Safari/537.36"
            )
        }
        self._url = (
            "https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?"
            "tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&"
            f"dataInicial={self.data}&dataFinal={self.data}&tipoPesquisaDJ=&argumento="
        )

    @property
    def user_agent(self):
        """Metodo get."""
        return self._user_agent

    def gera_hashcode(self, dicionario: dict, link):
        """Faz a requisição do link passado por parâmetro.


        response = requests.get(url=link, headers=self.user_agent, timeout=60)
        pdf_content = response.content
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        dicionario[md5_hash] = link
        return dicionario

    def obtem_soup(self, link=None, time=60):
        """Faz a requisicao do link passado por parametro.

        Response = pega o HTML bruto.
        Soup = analisa e processa o HTML.
        """

        if link is None:
            link = self._url
        response = requests.get(url=link, headers=self.user_agent, timeout=time)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def obtem_url_acesso(self):
        """Acesso a primeira pagina.

        Faz o request da primeira pagina e busca todo link na lista 'ul'.
        Armazena todos os links na lista 'url'.
        """
        try:
            lista_pdf = self.obtem_soup().find(
                "ul", {"class": "result__container--simples"}
            )

            if len(lista_pdf) < 1:
                raise FileNotFoundError

            url = []
            for item in lista_pdf:
                links_dj = item.find("a")["href"]
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
