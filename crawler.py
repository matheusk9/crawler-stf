"""doc"""
import requests
from bs4 import BeautifulSoup


class Crawler:
    """docstriasdasd"""

    def __init__(self):
        # TODO document why this method is empty
        pass

    def requisicao(self, link: str, config: str, time=60):
        """doc"""
        response = requests.get(link, headers=config, timeout=time)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
