"""doc"""
import requests
from bs4 import BeautifulSoup


class Crawler:
    """docstriasdasd"""

    def requisicao(self, link: str, config: dict, time=60):
        """doc"""
        response = requests.get(link, headers=config, timeout=time)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
