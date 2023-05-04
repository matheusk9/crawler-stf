"""doc"""
import requests
from bs4 import BeautifulSoup


class Crawler():
    """docstriasdasd"""

    def __init__(self):
        self.data = '13-12-2022'
        self._user_agent = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        }
        self._url = f"https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&dataInicial={self.data}&dataFinal={self.data}&tipoPesquisaDJ=&argumento="

    def get_user_agent(self):
        """doc"""
        return self._user_agent

    def requisicao(self, link=None, time=60):
        """doc"""

        if link is None:
            link = self._url
        response = requests.get(url=link, headers=self._user_agent, timeout=time)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def get_url_acesso(self):
        """doc"""

        # page 1 - LISTAS
        lista_pdf = self.requisicao().find(
            "ul", {"class": "result__container--simples"}
        )
        url = []
        # pega cada link de cada item que aparece na page 1
        for item in lista_pdf:
            links_dj = item.find("a")["href"]
            url.append("https://portal.stf.jus.br/servicos/dje/" + str(links_dj))
        return url

    def get_url_integral(self, url: list):
        """doc"""

        pdf_url = []
        # page 2 (integral e paginado)
        for link in url:
            integ_pag = self.requisicao(link).find_all("a", {"target": "_blank"})
            # page 3 - pegando link apenas dos PDFs integrais
            for pdf_link in integ_pag:
                if "Integral" in pdf_link.text:
                    pdf_url.append("https://portal.stf.jus.br" + str(pdf_link["href"]))
        return pdf_url
