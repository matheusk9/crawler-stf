"""docstriasdasd"""
import hashlib
import requests


class HashCode:
    """docstriasdasd"""

    hashcodes = {}

    @staticmethod
    def generate(link: str, config: str):
        """docstring"""
        response = requests.get(link, headers=config, timeout=60)
        pdf_content = response.content
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        HashCode.hashcodes[md5_hash] = link
        return print(HashCode.hashcodes)
