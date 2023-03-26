
# Crawler STF

O objetivo desse projeto é extrair códigos hash MD5 dos Diários da Justiça Eletrônico (DJe) de uma data específica disponibilizados pelo Supremo Tribunal Federal (STF) em formato PDF.


## Instalação

Para executar o código, você precisará do Python 3 instalado em sua máquina, bem como das bibliotecas "requests" e "beautifulsoup4", que podem ser instaladas através dos comandos:

```bash
  pip install requests
  pip install beautifulsoup4
```
    
Após instalar as bibliotecas, basta salvar o código em um arquivo com extensão ".py" e executá-lo no terminal ou prompt de comando, passando a data desejada como argumento. Por exemplo, para obter os PDFs do DJe do dia 01/01/2022, execute o código da seguinte forma:

Obs: Este ano (2023), o STF migrou os DJe para outro site, portanto o script só pega os PDFs disponibilizados até Dezembro de 2022, pois qualquer data após isso ocorrerá em erro.

```bash
  python nome_do_arquivo.py "01-01-2022"
```

O código então irá acessar o portal do STF e extrair os links dos PDFs do DJe da data especificada, gerando o hashcode MD5 de cada arquivo PDF. Os resultados serão exibidos no terminal ou prompt de comando.



## Dificuldades

Durante o projeto, algumas dificuldades foram encontradas. A primeira delas foi o acesso ao site do STF através da lib "requests" que me retornava o seguinte erro:

"Seu acesso a este website foi bloqueado de forma preventiva. Por favor, tente novamente em alguns minutos. (FD) beatifulsoup"

Após pesquisas descobri que devemos definir um "user_agent" nas solicitações para evitar que o servidor bloqueie o acesso por motivos de segurança ou um bot mal-intencionado.

```bash
 user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

```
Outra dificuldade encontrada foi a maçante passagem entre várias páginas até chegar no PDF de fato, o que dificultou a criação de um algoritmo genérico para buscar os PDFs e extrair as informações necessárias. 

Por fim, o principal desafio nesse projeto foi realmente extrair os códigos Hash dos PDFs hospedados. Em alguns casos, o hash pode estar incluído no próprio nome do arquivo ou no próprio link do arquivo, o que não foi esse caso. 
Realizei diferentes abordagens, de modo genérico, tentando processar o HTML com o BeautifulSoup procurando pelo link original do PDF que é aberto a partir de alguma extensão, porém me retornava apenas o texto bruto do arquivo. 
Outra tentativa foi fazer uma requisição HTTP GET para o link do PDF e extrair o conteúdo do "header". Porém, sem sucesso, o hash md5 do arquivo também não era fornecido no header.

A única solução que encontrei foi obter o hash md5 do arquivo PDF através do seu conteúdo bruto, utilizando a biblioteca "hashlib" que permite calcular o hash md5 do conteúdo do arquivo PDF.


```bash
 response = requests.get(link_pdf, headers= conf)
 pdf_content = response.content
 md5_hash = hashlib.md5(pdf_content).hexdigest()
```


## Aprendizados

Com este projeto, aprendi sobre a importância dos hashes para verificar a integridade de arquivos e garantir que eles não foram modificados ou corrompidos. Aprendi também como usar os headers para simular o comportamento de um navegador web e evitar ser bloqueado por sites.

## Referência

 - [Data Science e Direito - Bloqueio de Acesso](https://dsd.arcos.org.br/biblioteca-requests/)
 - [Web Scraping com Python](https://medium.com/data-hackers/web-scraping-com-python-para-pregui%C3%A7osos-unindo-beautifulsoup-e-selenium-parte-1-9677fc5e2385)
 - [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
 - [Requests](https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request)

