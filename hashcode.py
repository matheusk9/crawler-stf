"""docstriasdasd"""
import hashlib

import requests
from crawler import Crawler


class HashCode(Crawler):
    """docstriasdasd"""

    def requisicao(self, link: str, config: dict, time=60):
        """doc"""
        response = requests.get(link, headers=config, timeout=time)
        return response

    @staticmethod
    def generate(dicionario: dict, link, conf):
        """docstring"""
        response = HashCode.requisicao(HashCode, link, conf)
        pdf_content = response.content
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        dicionario[md5_hash] = link
        return dicionario
