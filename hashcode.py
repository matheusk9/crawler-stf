"""Módulo específico para HashCode."""
import hashlib

import requests
from crawler import Crawler


class HashCode(Crawler):
    """Responsável apenas para gerar chaves Hash."""

    @staticmethod
    def generate(dicionario: dict, link, obj: Crawler):
        """Faz a requisição do link passado por parâmetro.

        Gera o código MD5 e popula um dicionário com seus respectivos links.
        """

        response = requests.get(url=link, headers=obj.user_agent, timeout=60)
        pdf_content = response.content
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        dicionario[md5_hash] = link
        return dicionario
