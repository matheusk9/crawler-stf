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

    def test_baixa_caderno(self):
        link_de_teste = (
            "https://www.caceres.mt.gov.br/fotos_institucional_downloads/2.pdf"
        )
        nome_do_caderno = "caderno1.pdf"
        with open("src/test/integration/fixtures/caderno.pdf", "rb") as file:
            resultado_esperado_caderno = file.read()

        resultado_obtido_caderno = self.crawler._baixa_cadernos(
            link_de_teste, nome_do_caderno
        )
        self.assertEqual(resultado_esperado_caderno, resultado_obtido_caderno)
        self.assertTrue()
        # apagar arquivo try except

    def test_formata_data(self):
        data_esperada = {"dia": "13", "mes": "12", "ano": "2022"}
        data_obtida = self.crawler._formata_data()
        self.assertEqual(data_esperada, data_obtida)
