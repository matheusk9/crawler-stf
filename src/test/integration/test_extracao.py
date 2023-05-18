import os
import shutil
import time

from unittest.mock import patch
import unittest
from bs4 import BeautifulSoup

from src.modules.crawler import Crawler


class TestExtracao(unittest.TestCase):
    """Testes de integração."""

    crawler = Crawler("29-01-2021")

    def test_fake_request(self):
        head = {
            "User-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/89.0.4389.90 Safari/537.36"
            )
        }
        with open("src/test/integration/fixtures/resultado_busca.html", "r") as file:
            pagina_resultado_busca = file.read()

        soup_esperado = BeautifulSoup(pagina_resultado_busca, "html.parser")
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = pagina_resultado_busca
            soup_obtido = self.crawler._obtem_soup("python.org")
        self.assertEqual(soup_esperado, soup_obtido)
        mock_get.assert_called_once_with(url="python.org", headers=head, timeout=60)

    def test_salva_caderno(self):
        cadernos_de_teste = {
            "s12ndasdn1": b"arquivo1",
            "1q23e5ts3e": b"arquiv2",
            "2fasd212as": b"arquivo3",
        }
        data = self.crawler._formata_data()
        diretorio = (
            "src/test/integration/Cadernos/" + data["ano"] + "/" + data["mes"] + "/" + data["dia"] + "/"
        )
        os.makedirs(diretorio)
        for chave, valor in cadernos_de_teste.items():
            with open(diretorio + chave + ".pdf", "wb") as file:
                file.write(valor)

        try:
            time.sleep(5)
            apagar_pasta = "src/test/integration/Cadernos/"
            shutil.rmtree(apagar_pasta)
        except FileExistsError:
            print("Falha ao apagar")
