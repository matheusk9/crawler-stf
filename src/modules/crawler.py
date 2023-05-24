import hashlib
import os
import re

import requests
from bs4 import BeautifulSoup


class Crawler:
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

    def __init__(self, data: str) -> None:
        self._data = data
        self._dicionario = {}

    @property
    def data_de_busca(self) -> str:
        """Metodo get."""
        return self._data

    @property
    def dicionario(self) -> dict:
        """Metodo get."""
        return self._dicionario

    def run(self) -> None:
        """Método responsavel pela execução do script."""
        data = self._formata_data(self.data_de_busca)
        diretorio = (
            "src/Cadernos/" + data["ano"] + "/" + data["mes"] + "/" + data["dia"] + "/"
        )
        lista_de_pdfs_integrais = self._obtem_url_integral()
        if lista_de_pdfs_integrais:
            for url in lista_de_pdfs_integrais:
                conteudo_do_pdf = self._obtem_content(url)
                self._gera_hashcode(conteudo_do_pdf)
            self._salva_cadernos(diretorio)
        else:
            print("Não existem DJe na data informada!")

    def _obtem_content(self, link: str) -> object:
        """Obtem conteudo do link passado por parametro"""

        response = requests.get(url=link, headers=self.HEADER, timeout=60)
        return response.content

    def _obtem_soup(self, link=None) -> object:
        """Faz a requisicao do link passado por parametro.

        content = pega o HTML bruto.
        Soup = retorna um objeto do HTML.
        """

        if link is None:
            link = self.LINK_DE_BUSCA.format(data=self.data_de_busca)
        content = self._obtem_content(link)
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def _obtem_url_acesso(self) -> list:
        """Acesso a primeira pagina.

        Faz o request da primeira pagina e busca pela 'ul' no html.
        Lista_pdf = contém o 'ul' e faz a busca por todos os links contidos ('a').
        Caso não tenha links, retorna a excessão FileNotFoundError e encerra o programa.
        Se não houver excessões, retorna os links na lista 'url'.
        """

        try:
            lista_pdf = self._obtem_soup()
            lista_pdf = lista_pdf.select_one('section[id="conteudo"]')
            lista_pdf = lista_pdf.select("a")

            if not lista_pdf:
                return []

            url = []
            url = [
                "https://portal.stf.jus.br/servicos/dje/" + str(item["href"])
                for item in lista_pdf
            ]

            return url
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return []
        finally:
            print("Processando...")

    def _obtem_url_integral(self) -> list:
        """Acesso a pagina de PDFs integrais e paginados.

        Busca apenas links de PDFs integrais e armazena na lista url_pdf_integral.
        """

        lista_de_links_ul = self._obtem_url_acesso()
        if not lista_de_links_ul:
            return []

        url_pdf_integral = []
        for link in lista_de_links_ul:
            integ_pag = self._obtem_soup(link)
            integ_pag = integ_pag.select_one('section[id="conteudo"]')
            if not integ_pag:
                break
            integ_pag = integ_pag.find_all("a", {"target": "_blank"})
            for pdf_link in integ_pag:
                if "Integral" in pdf_link.text:
                    url_pdf_integral.append(
                        "https://portal.stf.jus.br" + str(pdf_link["href"])
                    )
        return url_pdf_integral

    def _gera_hashcode(self, conteudo: object) -> None:
        """Faz a requisição do link passado por parâmetro.

        Gera os códigos MD5 e os retorna em um dicionário com seus respectivos conteudos.
        """
        md5_hash = hashlib.md5(conteudo).hexdigest()
        self.dicionario[md5_hash] = conteudo

    def _salva_cadernos(self, diretorio: str) -> None:
        """Salva os cadernos em diretórios com suas respectivas datas.

        Método 'makedirs()' é o responsável pela criação dos diretórios que automaticamente
        verifica se a pasta já existe, e se não existir, cria uma nova.
        Após a criação de diretório é verificado se o caderno em si já existe dentro da pasta.
        Se não existir, o método 'open()' salva de fato o arquivo PDF (content) em sua respectiva data.
        """

        os.makedirs(diretorio, exist_ok=True)
        for nome_do_caderno, conteudo_do_caderno in self.dicionario.items():
            if os.path.exists(diretorio + nome_do_caderno + ".pdf"):
                print(f"O caderno {nome_do_caderno}.pdf já existe!")
            else:
                with open(diretorio + nome_do_caderno + ".pdf", "wb") as file:
                    file.write(conteudo_do_caderno)
                    print(f"O caderno {nome_do_caderno} foi salvo com sucesso")

    def _formata_data(self, data: str) -> dict:
        """Formata a data de busca.

        Remove uma cadeia de caracteres especiais utilizando regex e 'splita'.
        Popula um dicionario com as chaves dia, mes e ano.
        A data deve ter a seguinte formatação: DD-MM-AAAA
        """

        data_formatada = re.split(r"[-/\. ]", data)
        data_final = {
            "dia": data_formatada[0],
            "mes": data_formatada[1],
            "ano": data_formatada[2],
        }
        return data_final
