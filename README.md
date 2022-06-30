# Trabalho Prático 01 - ICC200 Banco de Dados I - UFAM - 2022

> Este trabalho prático tem como objetivo implementar uma ferramenta para minerar dados do dataset `Amazon product co-purchasing network metadata` e construir uma banco de dados a partir dos dados coletados.

> Keywords: `amazon`, `dataset`, `miner-tool`, `database`, `dashboard`, `sql`, `python`

<!-- TABLE OF CONTENTS -->
## Sumário

- [Objetivo](#objetivo)
- [Ambiente de desenvolvimento](#ambiente-de-desenvolvimento)
- [Arquivo de entrada](#arquivo-de-entrada)
  - [Formato dos dados](#formato-dos-dados)
  - [Estatísticas do dataset](#estatsticas-do-dataset)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Tecnologias e módulos utilizados](#tecnologias-e-módulos-utilizados)
- [Contato](#contato)
- [License](#license)

## Objetivo

Objetivo deste trabalho prático é projetar e implementar um banco de dados sobre produtos vendidos em uma loja de comércio eletrônico,
incluindo avaliações e comentários de usuários sobre estes produtos. O trabalho consiste na criação de um Banco de Dados Relacional
contendo dados sobre compras de produtos e elaboração de um Dashboard, um painel para monitoramento dos dados de compra, gerando
uma série de relatórios. Os dados para o banco de dados serão fornecidos de um arquivo de entrada que será indicado aos alunos.

## Ambiente de desenvolvimento

Os códigos fontes devem ser desenvolvidos em linguagem Python e o SGBD relacional usado deverá ser o PostgreSQL. Os scripts Python
devem fazer acesso direto ao SGDB usando comandos SQL, sem camadas de software intermediário.

## Arquivo de entrada

O [arquivo de entrada](https://snap.stanford.edu/data/bigdata/amazon/amazon-meta.txt.gz) de onde serão extraídos os dados de entrada será o [“Amazon product co-purchasing network metadata”](https://snap.stanford.edu/data/amazon-meta.html) que faz
parte do Stanford Network Analysis Project (SNAP). Os dados foram coletados em 2006 do site Amazon.com e contém informações sobre
produtos e comentários de clientes sobre 548.552 produtos diferentes (livros, CDs de música, DVDs e fitas de vídeo VHS). Para cada
produto, a seguinte informação está disponível:

- Título
- Posição no ranking de vendas (salesrank)
- Lista de produtos `similares` (que foram adquiridos junto com o produto)
- Informação de categorização do produto - Categorias e subcategorias ao qual o produto pertence
- Comentários sobre os produtos

### Formato dos dados

```
Id:   15
ASIN: 1559362022
  title: Wake Up and Smell the Coffee
  group: Book
  salesrank: 518927
  similar: 5  1559360968  1559361247  1559360828  1559361018  0743214552
  categories: 3
   |Books[283155]|Subjects[1000]|Literature & Fiction[17]|Drama[2159]|United States[2160]
   |Books[283155]|Subjects[1000]|Arts & Photography[1]|Performing Arts[521000]|Theater[2154]|General[2218]
   |Books[283155]|Subjects[1000]|Literature & Fiction[17]|Authors, A-Z[70021]|( B )[70023]|Bogosian, Eric[70116]
  reviews: total: 8  downloaded: 8  avg rating: 4
    2002-5-13  cutomer: A2IGOA66Y6O8TQ  rating: 5  votes:   3  helpful:   2
    2002-6-17  cutomer: A2OIN4AUH84KNE  rating: 5  votes:   2  helpful:   1
    2003-1-2  cutomer: A2HN382JNT1CIU  rating: 1  votes:   6  helpful:   1
    2003-6-7  cutomer: A2FDJ79LDU4O18  rating: 4  votes:   1  helpful:   1
    2003-6-27  cutomer: A39QMV9ZKRJXO5  rating: 4  votes:   1  helpful:   1
    2004-2-17  cutomer:  AUUVMSTQ1TXDI  rating: 1  votes:   2  helpful:   0
    2004-2-24  cutomer: A2C5K0QTLL9UAT  rating: 5  votes:   2  helpful:   2
    2004-10-13  cutomer:  A5XYF0Z3UH4HB  rating: 5  votes:   1  helpful:   1
```

### Estatísticas do dataset

<table>
<tr>
<td>Products</td>
<td>548,552</td>
</tr>
<tr>
<td>Product-Project Edges</td><td>1,788,725</td>
</tr>
<tr>
<td>Reviews</td><td>7,781,990</td>
</tr>
<tr>
<td>Product category memberships</td><td>2,509,699</td>
</tr>
<tr>
<td>Books</td><td>393561</td>
</tr>
<tr>
<td>Music CDs</td><td>103144</td>
</tr>
<tr>
<td>Videos</td><td>26132</td>
</tr>
</table>

## Estrutura do projeto

O projeto está organizado segundo a estrutura abaixo:

```
bd1_tp1
└─── controller.py
└─── database.ini
└─── database.py
└─── db_create.sql
└─── model.py
└─── README.md
└─── TP1-BD-2021-02 [2022].md
└─── tp1_3.1.pdf
└─── tp1_3.2.py
└─── tp1_3.3.py
```

- `controller.py`: neste script estão contidos todos os códigos de extração e operações que manipulam os dados.
- `database.ini`: arquivo com os parâmetros para conexão com o SGBD.
- `db_create.sql`: arquivo com os comandos SQL para criação das tabelas no SGBD.
- `model.py`: arquivo de classes do modelo de dados (ORM).
- `TP1-BD-2021-02 [2022].pdf`: arquivo PDF com a especificação do trabalho prático.
- `tp1_3.1.pdf`: arquivo PDF com a descrição do banco de dados (diagrama e dicionário de dados).
- `tp1_3.2.py`: este script é responsável pela extração dos dados contidos no arquivo de metadados, conexão com o SGBD, criação das tabelas do banco de dados e inserção dos dados.
- `tp1_3.3.py`: neste script implementa um DashBoard no console permitindo algumas consultas e relatórios com base nos dados recuperados do banco de dados.

## Tecnologias e módulos utilizados

- Python3: como linguagem de programação `Python 3.8.8`.
  - `os`: Este módulo foi utilizado para acesso às rotinas do sistema operacional na leitura do arquivo de metadados. 
  - `psycopg2`: Este módulo foi utilizado para conexão e comunidação com o SGBD `PostgreSQL`
  - `re`: Este módulo foi utilizado para construção de `Expressões Regulares` para extração de dados do arquivo de metadados.

## Contato

Marcos A. P. de Lima  – marcos.lima@icomp.ufam.edu.br
[![LinkedIn][linkedin-shield]][linkedin-url]

## License

- **[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)** [![GNU GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
- Copyright 2022 © [marcosmapl](https://github.com/marcosmapl).

<!-- Markdown link & img dfn's -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/marcosmapl