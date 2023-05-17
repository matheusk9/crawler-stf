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

    def run(self):
        """Método responsavel pela execução do script."""

        resultado_pdf_integral = self._obtem_url_integral()
        if resultado_pdf_integral:
            for url in resultado_pdf_integral:
                self._gera_hashcode(url)
            self._salva_cadernos()
        else:
            print("Não existem DJe na data informada!")

    def _obtem_content(self, link):
        response = requests.get(url=link, headers=self.HEADER, timeout=60)
        return response.content

    def _obtem_soup(self, link=None):
        """Faz a requisicao do link passado por parametro.

        Response = pega o HTML bruto.
        Soup = retorna um objeto do HTML.
        """

        if link is None:
            link = self.LINK_DE_BUSCA.format(data=self.data_de_busca)
        content = self._obtem_content(link)
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def _obtem_url_acesso(self):
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

    def _obtem_url_integral(self):
        """Acesso a pagina de PDFs integrais e paginados.

        Busca apenas links de PDFs integrais e armazena na lista url_pdf_integral.
        """
        lista_de_links_ul = self._obtem_url_acesso()
        if not lista_de_links_ul:
            return False

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

    def _gera_hashcode(self, link):
        """Faz a requisição do link passado por parâmetro.

        Gera os códigos MD5 e os retorna em um dicionário com seus respectivos links.
        """

        pdf_content = self._obtem_content(link)
        md5_hash = hashlib.md5(pdf_content).hexdigest()
        self.dicionario[md5_hash] = link
        return self.dicionario

    def _salva_cadernos(self):
        """Salva os cadernos em diretórios com suas respectivas datas.

        Método 'makedirs()' é o responsável pela criação dos diretórios que automaticamente
        verifica se a pasta já existe ou não. Se já existe, retorna uma excessão.
        O método 'open()' salva de fato o arquivo PDF (content) em sua respectiva data.
        """
        data = self._formata_data()
        diretorio = (
            "src/Cadernos/" + data["ano"] + "/" + data["mes"] + "/" + data["dia"] + "/"
        )
        try:
            os.makedirs(diretorio)
            for chave_hash, valor_link in self.dicionario.items():
                content = self._obtem_content(valor_link)
                with open(diretorio + chave_hash + ".pdf", "wb") as file:
                    file.write(content)
            print(self.dicionario)
        except FileExistsError:
            print("Os cadernos na data informada já existem!")

    def _formata_data(self):
        """Formata a data de busca.

        Remove uma cadeia de caracteres especiais utilizando regex e 'splita'.
        Realiza filtros para encontrar dia, mes e ano da lista 'data_formatada'.
        Popula um dicionario com as chaves dia, mes e ano.
        A data deve ter a seguinte formatação: dia-mês-ano
        """

        data = self.data_de_busca
        data_formatada = re.split(r"[-/\. ]", data)
        indice_mes = data_formatada[1]
        data_formatada.pop(1)

        data_final = {"dia": "", "mes": indice_mes, "ano": ""}
        for bloco in data_formatada:
            if len(bloco) == 4:
                data_final["ano"] = bloco
            else:
                data_final["dia"] = bloco
        return data_final
