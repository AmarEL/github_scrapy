# Github Crawler  
Um crawler em python e scrapy para crawlear repositorios do github!  
## Python Version:
Python3.6  
## Crawler installation
**Algumas bibliotecas de sistema são necessárias**

    $[sudo] apt-get install build-essential python3.6-dev
**Clone o repositório**

    $ git clone https://github.com/AmarEL/github_scrapy.git
    $ cd github_scrapy/

**Intale os pacotes da aplicação**

    $ pip install -r requirements.txt


## Crawler Execution  
1. Mova o arquivo de entrada 'repositories.txt' para a raiz do projeto  
2. Na raiz do projeto, execute o crawler com o comando:  
    $ python github_crawler.py repositories.txt 

Os resultados podem ser visualizados no diretório "repositories", em que cada corresponde a um repositório.  
Ex: frontpressorg_frontpress.txt == frontpressorg/frontpress



