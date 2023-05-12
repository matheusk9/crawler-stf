"""Modulo de requisições."""
import requests
from bs4 import BeautifulSoup
import hashlib


class Crawler:
    """Responsavel pela extração dos dados"""

    def __init__(self, data: str) -> None:
        self.__data = data
        self.__dicionario = {}

    @property
    def data_de_busca(self) -> str:
        """Metodo get."""
        return self.__data

    @property
    def dicionario(self):
        """Metodo get."""
        return self.__dicionario

    HEADER = {
        "User-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.90 Safari/537.36"
        )
    }

    LINK_DE_BUSCA = (
        "https://portal.stf.jus.br/servicos/dje/listarDiarioJustica.asp?"
        "tipoVisualizaDJ=periodoDJ&txtNumeroDJ=&txtAnoDJ=2022&"
        "dataInicial={data}&dataFinal={data}"
    )

    def obtem_soup(self, link=None, time=60):
        """Faz a requisicao do link passado por parametro.

        Response = pega o HTML bruto.
        Soup = retorna um objeto do HTML.
        """

        if link is None:
            link = self.LINK_DE_BUSCA.format(data=self.data_de_busca)
        response = requests.get(url=link, headers=self.HEADER, timeout=time)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def obtem_url_acesso(self):
        """Acesso a primeira pagina.

        Faz o request da primeira pagina e busca pela 'ul' no html.
        Lista_pdf = contém o 'ul' e faz a busca por todos os links contidos ('a').
        Caso não tenha links, retorna a excessão FileNotFoundError e encerra o programa.
        Se não houver excessões, retorna os links na lista 'url'.
        """

        try:
            lista_pdf = self.obtem_soup()
            lista_pdf = lista_pdf.select_one('section[id="conteudo"]')
            lista_pdf = lista_pdf.select("a")

            url = []
            if not lista_pdf:
                return url

            for item in lista_pdf:
                links_dj = item["href"]
                url.append("https://portal.stf.jus.br/servicos/dje/" + str(links_dj))
            return url
        except Exception as e:
            lista_vazia = []
            print(f"Ocorreu um erro inesperado: {e}")
            return lista_vazia
        finally:
            print("Processando...")

    def obtem_url_integral(self):
        """Acesso a pagina de PDFs integrais e paginados.

        Busca apenas links de PDFs integrais e armazena na lista url_pdf_integral.
        """
        lista_de_links_ul = self.obtem_url_acesso()
        if not lista_de_links_ul:
            return False

        url_pdf_integral = []
        for link in lista_de_links_ul:
            integ_pag = self.obtem_soup(link)
            integ_pag = integ_pag.select_one('section[id="conteudo"]')
            if not integ_pag:
                break
            integ_pag = integ_pag.find_all("a", {"target": "_blank"})
            for pdf_link in integ_pag:
                # import pdb; pdb.set_trace()
                if "Integral" in pdf_link.text:
                    url_pdf_integral.append(
                        "https://portal.stf.jus.br" + str(pdf_link["href"])
                    )
        return url_pdf_integral

    def gera_hashcode(self, link):
        """Faz a requisição do link passado por parâmetro.

        Gera os códigos MD5 e os retorna em um dicionário com seus respectivos links.
        """

        response = requests.get(url=link, headers=self.HEADER, timeout=60)
        pdf_content = response.content
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        self.dicionario[md5_hash] = link
        return self.dicionario

    def run(self):
        """Método responsavel pela execução do script."""

        resultado_pdf_integral = self.obtem_url_integral()

        if resultado_pdf_integral:
            for url in resultado_pdf_integral:
                self.gera_hashcode(url)
            return print(self.dicionario.items())
        else:
            print("Não existem DJe na data informada!")
