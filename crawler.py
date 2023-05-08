"""Modulo de requisições."""
import requests
from bs4 import BeautifulSoup
import hashlib


class Crawler:
    """Responsavel pela configuração e requests."""

    def __init__(self):
        self.data = "13-12-2022"
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

    def generate(self, dicionario: dict, link):
        """Faz a requisição do link passado por parâmetro.

        Gera o código MD5 e popula um dicionário com seus respectivos links.
        """

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

        lista_pdf = self.requisicao().find(
            "ul", {"class": "result__container--simples"}
        )
        url = []
        for item in lista_pdf:
            links_dj = item.find("a")["href"]
            url.append("https://portal.stf.jus.br/servicos/dje/" + str(links_dj))
        return url

    def obtem_url_integral(self, url: list):
        """Acesso a pagina de PDFs integrais e paginados.

        Busca apenas links de PDFs integrais e armazena na lista pdf_url.
        """

        pdf_url = []
        for link in url:
            integ_pag = self.requisicao(link).find_all("a", {"target": "_blank"})
            for pdf_link in integ_pag:
                if "Integral" in pdf_link.text:
                    pdf_url.append("https://portal.stf.jus.br" + str(pdf_link["href"]))
        return pdf_url
