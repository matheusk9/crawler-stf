"""docstriasdasd"""
import hashlib

import requests
from crawler import Crawler


class HashCode(Crawler):
    """docstriasdasd"""

    @staticmethod
    def generate(dicionario: dict, link, obj: Crawler):
        """docstring"""

        response = requests.get(url=link, headers=obj.get_user_agent(), timeout=60)
        pdf_content = response.content
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        dicionario[md5_hash] = link
        return dicionario
