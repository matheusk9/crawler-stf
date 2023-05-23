import shutil

from unittest.mock import patch
import unittest
from bs4 import BeautifulSoup

from src.modules.crawler import Crawler


class TestExtracao(unittest.TestCase):
    """Testes de integração."""

    REQUESTS_GET = "requests.get"

    def setUp(self) -> None:
        self.crawler = Crawler("29-12-2022")
        self.head = {
            "User-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/89.0.4389.90 Safari/537.36"
            )
        }

        with open("src/test/integration/fixtures/resultado_busca.html", "r") as file:
            self.pagina_resultado_busca = file.read()

        with open("src/test/integration/fixtures/pagina_integral_paginado.html", "r") as file:
            self.pagina_integral_paginado = file.read()

        self.cadernos_de_testes = {
            "1bdfe4baf9061c3667ded70d8f66142c": b"arquivo1",
            "8eed470a9ac3c36ef139ece144537f46": b"arquiv2",
            "91e3b288eab8d59598a52221296f8995": b"arquivo3",
        }
        return super().setUp()

    def test_obtem_soup(self):
        soup_esperado = BeautifulSoup(self.pagina_resultado_busca, "html.parser")
        with patch(self.REQUESTS_GET) as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = self.pagina_resultado_busca
            soup_obtido = self.crawler._obtem_soup("python.org")
        self.assertEqual(soup_esperado, soup_obtido)
        mock_get.assert_called_once_with(
            url="python.org", headers=self.head, timeout=60
        )

    def test_obtem_content(self):
        content_esperado = b"algum conteudo"

        with patch(self.REQUESTS_GET) as mock_get:
            mock_get.return_value.content = content_esperado

            content_obtido = self.crawler._obtem_content("https://www.python.org/")

            self.assertEqual(content_esperado, content_obtido)
            mock_get.assert_called_once_with(
                url="https://www.python.org/", headers=self.head, timeout=60
            )

    def test_obtem_url_acesso(self):
        lista_esperada = [
            (
                "https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?"
                "tipoVisualizaDJ=numeroDJ&txtNumeroDJ=253&txtAnoDJ=2022"
            ),
            (
                "https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?"
                "tipoVisualizaDJ=numeroDJ&txtNumeroDJ=252&txtAnoDJ=2022"
            ),
            (
                "https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?"
                "tipoVisualizaDJ=numeroDJ&txtNumeroDJ=0&txtAnoDJ="
            ),
        ]

        with patch(self.REQUESTS_GET) as mock_get:
            # 'Mockei' o soup interno e defini o content com a fixture pagina_resultado_busca
            mock_get.return_value.content = self.pagina_resultado_busca
            lista_obtida = self.crawler._obtem_url_acesso()

        self.assertEqual(lista_obtida, lista_esperada)
        mock_get.assert_called_once_with(
            url=self.crawler.LINK_DE_BUSCA.format(data="29-12-2022"),
            headers=self.head,
            timeout=60,
        )

    def test_obtem_url_integral(self):
        retorno_obtem_url_acesso = [
            (
                "https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?"
                "tipoVisualizaDJ=numeroDJ&txtNumeroDJ=253&txtAnoDJ=2022"
            )
        ]
        url_integral_esperado = [
            "https://portal.stf.jus.br/servicos/dje/verDiarioEletronico.asp?numero=253&data=12/12/2022"
        ]

        with patch.object(
            self.crawler, "_obtem_url_acesso", return_value=retorno_obtem_url_acesso
        ) as mock_obtem_url_acesso:
            with patch(self.REQUESTS_GET) as mock_get:
                mock_get.return_value.content = self.pagina_integral_paginado
                url_integral_obtido = self.crawler._obtem_url_integral()

        self.assertEqual(url_integral_obtido, url_integral_esperado)
        mock_obtem_url_acesso.assert_called_once()
        mock_get.assert_called()

    def test_salva_caderno(self):
        conteudo_esperado = b"conteudo do arquivo"
        self.crawler._dicionario = {
            "1bdfe4baf9061c3667ded70d8f66142c": conteudo_esperado
        }
        data = self.crawler._formata_data(self.crawler.data_de_busca)
        diretorio = (
            "src/test/integration/Cadernos/"
            + data["ano"]
            + "/"
            + data["mes"]
            + "/"
            + data["dia"]
            + "/"
        )

        self.crawler._salva_cadernos(diretorio)

        try:
            with open(diretorio + "1bdfe4baf9061c3667ded70d8f66142c.pdf", "rb") as file:
                conteudo_do_arquivo = file.read()

            self.assertEqual(conteudo_do_arquivo, conteudo_esperado)
        except FileNotFoundError:
            raise AssertionError("Falha ao criar o arquivo!")

        try:
            apagar_pasta = "src/test/integration/Cadernos/"
            shutil.rmtree(apagar_pasta)
        except FileNotFoundError:
            print("Falha ao apagar")

    def test_formata_data(self):
        data_para_testes = ["29-12-2022", "29/12/2022", "29.12/2022", "29 12 2022"]
        data_de_testes_esperada = {
            "dia": "29",
            "mes": "12",
            "ano": "2022",
        }
        for data in data_para_testes:
            data_resultado_obtido = self.crawler._formata_data(data)
            self.assertDictEqual(data_de_testes_esperada, data_resultado_obtido)

    def test_gera_hashcode(self):
        conteudo_para_teste = b"arquivo1"
        dicionario_esperado = {"1bdfe4baf9061c3667ded70d8f66142c": conteudo_para_teste}

        self.crawler._gera_hashcode(conteudo_para_teste)
        self.assertDictEqual(self.crawler.dicionario, dicionario_esperado)
