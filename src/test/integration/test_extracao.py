import hashlib
import os
import re
import shutil
import time

from unittest.mock import patch
import unittest
from bs4 import BeautifulSoup

from src.modules.crawler import Crawler


class TestExtracao(unittest.TestCase):
    """Testes de integração."""

    def setUp(self) -> None:
        self.crawler = Crawler("29-12-2022")
        self.head = {
            "User-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/89.0.4389.90 Safari/537.36"
            )
        }
        self.cadernos_de_testes = {
            "1bdfe4baf9061c3667ded70d8f66142c": b"arquivo1",
            "8eed470a9ac3c36ef139ece144537f46": b"arquiv2",
            "91e3b288eab8d59598a52221296f8995": b"arquivo3",
        }
        self.data_de_testes_esperada = {
            "dia": "29",
            "mes": "12",
            "ano": "2022",
        }
        return super().setUp()

    def test_fake_request(self):
        with open("src/test/integration/fixtures/resultado_busca.html", "r") as file:
            pagina_resultado_busca = file.read()

        soup_esperado = BeautifulSoup(pagina_resultado_busca, "html.parser")
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = pagina_resultado_busca
            soup_obtido = self.crawler._obtem_soup("python.org")
        self.assertEqual(soup_esperado, soup_obtido)
        mock_get.assert_called_once_with(
            url="python.org", headers=self.head, timeout=60
        )

    def test_salva_caderno(self):
        data = self.test_formata_data()
        diretorio = (
            "src/test/integration/Cadernos/"
            + data["ano"]
            + "/"
            + data["mes"]
            + "/"
            + data["dia"]
            + "/"
        )
        os.makedirs(diretorio, exist_ok=True)
        for chave, valor in self.cadernos_de_testes.items():
            if os.path.exists(diretorio + chave + ".pdf"):
                continue
            else:
                with open(diretorio + chave + ".pdf", "wb") as file:
                    file.write(valor)

        try:
            time.sleep(3)
            apagar_pasta = "src/test/integration/Cadernos/"
            shutil.rmtree(apagar_pasta)
        except FileNotFoundError:
            print("Falha ao apagar")

    def test_formata_data(self):
        data = self.crawler.data_de_busca
        formata_data = r"(?P<dia>\d{2})[^\d](?P<mes>\d{2})[^\d](?P<ano>\d{4})"
        data_match = re.match(formata_data, data)
        data_resultado = data_match.groupdict()

        self.assertDictEqual(self.data_de_testes_esperada, data_resultado)
        return data_resultado

    def test_gera_hashcode(self):
        dicionario_esperado = {}
        for caderno in self.cadernos_de_testes.values():
            md5_hash = hashlib.md5(caderno).hexdigest()
            dicionario_esperado[md5_hash] = caderno
        self.assertDictEqual(dicionario_esperado, self.cadernos_de_testes)
