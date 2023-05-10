from unittest.mock import patch
import unittest
from src.modules.crawler import Crawler
from bs4 import BeautifulSoup


class TestExtracao(unittest.TestCase):
    """Doc"""

    def test_fake_request(self):
        head = {
            "User-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkksadasdkasldkslkdmasldmlsakmdlsakmdskdm"
                "Chrome/89.0.4389.90 Safari/537.36"
            )
        }
        crawler = Crawler("13-12-2022")
        with open("src/test/fixtures/resultado_busca.html", "r") as file:
            pagina_resultado_busca = file.read()

        soup_esperado = BeautifulSoup(pagina_resultado_busca, "html.parser")
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = pagina_resultado_busca
            soup_obtido = crawler.obtem_soup("python.org")
            # import pdb; pdb.set_trace()
        self.assertEqual(soup_esperado, soup_obtido)
        mock_get.assert_called_once_with(url="python.org", headers=head, timeout=60)


# if __name__ == '__main__':
#     unittest.main()
