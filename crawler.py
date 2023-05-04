"""doc"""
import requests
from bs4 import BeautifulSoup


class Crawler:
    """docstriasdasd"""

    def __init__(self, data: str):
        self._user_agent = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        }
        self._url = f"https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&dataInicial={data}&dataFinal={data}&tipoPesquisaDJ=&argumento="

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
