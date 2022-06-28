# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# TRABALHO PRÁTICO I
from typing import Iterable, Any
from database import DatabaseManager

LISTAR_5_SQL = "((SELECT product.product_id, product.asin, review.customer_id, review.review_date, review.rating, review.helpful FROM product, review WHERE product.product_id=%s ORDER BY rating DESC, helpful DESC LIMIT 5) UNION ALL (SELECT product.product_id, product.asin, review.customer_id, review.review_date, review.rating, review.helpful FROM product, review WHERE product.product_id=%s ORDER BY rating ASC, helpful DESC LIMIT 5))"
LISTAR_SIMILARES_SQL = "SELECT product.title, product.salesrank, psimilar.title, psimilar.salesrank FROM product JOIN similar_products ON product.asin=similar_products.product_asin JOIN product as psimilar ON psimilar.asin=similar_products.similar_asin WHERE product.product_id=%s AND psimilar.salesrank>product.salesrank"
LISTAR_EVOLUCAO_SQL = "SELECT product.title, review.review_date, round(avg(review.rating), 2) FROM product INNER JOIN review ON product.product_id=review.product_id WHERE product.product_id=%s GROUP BY product.title, review.review_date ORDER BY review_date ASC"
LISTAR_MAIS_VENDIDOS_SQL = "SELECT title, salesrank, product_group FROM (SELECT title, salesrank, product_group, Rank() over (Partition BY product_group ORDER BY salesrank DESC ) AS Rank FROM product WHERE salesrank > 0) rs WHERE Rank <= 10"
LISTAR_PRODUTOS_SQL =  "SELECT t2.product_id, t2.title, t2.product_group, t2.avg_helpful, t2.n_rank FROM (SELECT product.product_id, product.title, product.product_group, t1.avg_helpful, ROW_NUMBER() OVER (PARTITION BY product.product_group ORDER BY t1.avg_helpful DESC) AS n_rank FROM product JOIN (SELECT review.product_id, round(avg(review.helpful), 2) AS avg_helpful FROM review WHERE review.helpful > 0 GROUP BY review.product_id) t1 ON t1.product_id=product.product_id) as t2 WHERE n_rank <= 10"
LISTAR_CATEGORIAS_SQL = "select category.name, round(t_avg.avg, 2) from category inner join (select product_category.category_id, avg(qtd_pos.count) from product_category inner join (select review.product_id, count(*) from review where review.helpful > 0 group by review.product_id) qtd_pos on qtd_pos.product_id = 	product_category.product_id group by product_category.category_id having  avg(qtd_pos.count) > 0 order by avg desc limit 5) t_avg on category.category_id  =  t_avg.category_id"
LISTAR_CLIENTES_SQL = "SELECT customer_id, n_reviews, review_rank, product_group FROM (SELECT customer_id, n_reviews, product_group, ROW_NUMBER() OVER (PARTITION BY t1.product_group ORDER BY t1.n_reviews DESC) AS review_rank FROM (SELECT customer_id, count(customer_id) AS n_reviews, product_group FROM product INNER JOIN review ON product.product_id=review.product_id GROUP BY (product_group, customer_id)) AS t1 ORDER BY t1.product_group ASC, t1.n_reviews DESC) AS t2 WHERE review_rank <= 10"


def print_table_data(header: Iterable[str], cols_size: Iterable[int], data: Iterable[Iterable[Any]]):
    """Essa função recebe um conjuto de dados (tuplas) e imprime no console num formato tabular

    Args:
        header (Iterable[str]): Nome das colunas da tabela (linha de cabeçalho).
        cols_size (Iterable[int]): Tamanho de caracteres em cada coluna da tabela. Utilizado para formatação.
        data (Iterable[Iterable[Any]]): Conjunto de dados num formato tabular a serem impressos no console.

    """
    # imprime o cabeçalho (nome das colunas) da tabela
    print('-' * sum(cols_size))
    for col_name, col_size in zip(header, cols_size):
        print(f'{col_name.ljust(col_size)}', end='')
    print('\n' + '-' * sum(cols_size))
    # imprime o conjunto de dados
    for row in data:
        for value, col_size in zip(row, cols_size):
            print(f'{str(value).ljust(col_size)}', end='')
        print('')
    print('-' * sum(cols_size))
    print('')


def execute_query(sql_query: str, params: Iterable = None) -> Iterable:
    """Função que recebe uma query SQL e seus parametros, executa a query e retorna os registros obtidos.

    Args:
        sql_query (str): A query SQL a ser executada. Os parametros são identificados como "placeholders" dentro da query.
        params (Iterable): Conjunto de parametros da query.

    Returns:
        Iterable: Conjunto de dados obtidos com a execução da query.

    """
    # estabelece uma conexão com o sgbd
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    # obtem o objeto para executar consultas
    cursor = conn.cursor()
    # executa a consulta fornecida junto com seus parametros
    cursor.execute(sql_query, params)
    # retorna os dados encontrados (tuplas)
    return cursor.fetchall()


def listar_5():
    """Esta função exibe os 5 comentários mais úteis e com maior avaliação, e também os 5 mais úteis com menor avaliação, de um dado produto."""
    id = input('POR GENTILEZA, INFORME O ID DO PRODUTO: ')
    rows = execute_query(LISTAR_5_SQL, (id, id))
    print_table_data(['ID', 'ASIN', 'CUSTOMER ID', 'REVIEW DATE', 'RATING', 'HELPFUL'], [8, 15, 18, 13, 10, 5], rows)


def listar_similares():
    """Esta função exibe os 5 comentários mais úteis e com maior avaliação, e também os 5 mais úteis com menor avaliação, de um dado produto."""
    id = input('POR GENTILEZA, INFORME O ID DO PRODUTO: ')
    rows = execute_query(LISTAR_SIMILARES_SQL, (id, ))
    print_table_data(['TITULO PRODUTO', 'SALESRANK', 'TITULO SIMILAR', 'SALESRANK'], [80, 12, 80, 12], rows)


def listar_evolucao():
    """Esta função exibe a evolução diária das médias de avaliação de um produto."""
    id = input('POR GENTILEZA, INFORME O ID DO PRODUTO: ')
    rows = execute_query(LISTAR_EVOLUCAO_SQL, (id, ))
    print_table_data(['TITULO', 'DATA', 'MÉDIA DE AVALIAÇÕES'], [150, 14, 10], rows)


def listar_mvendidos():
    """Esta função exibe uma tabela no console com os 10 produtos mais vendidos (líderes) de cada grupo de produtos."""
    rows = execute_query(LISTAR_MAIS_VENDIDOS_SQL)
    print_table_data(['TITULO', 'RANK VENDAS', 'GRUPO'], [150, 15, 13], rows)


def listar_avaliacoes_produtos():
    """Esta função exibe uma tabela no console com os 10 produtos com a maior média de avaliações úteis positivas por grupo."""
    rows = execute_query(LISTAR_PRODUTOS_SQL)
    print_table_data(['ID PRODUTO', 'TITULO', 'GRUPO', 'MEDIA AV', 'RANK'], [12, 150, 15, 12, 5], rows)


def listar_avaliacoes_categorias():
    """Esta função exibe uma tabela no console com as 5 categorias mais bem avaliadas."""
    rows = execute_query(LISTAR_CATEGORIAS_SQL)
    print_table_data(['NOME CATEGORIA', 'MEDIA AV'], [50, 12], rows)


def listar_clientes():
    """Esta função exibe uma tabela no console com os 10 clientes que mais fizeram comentários por grupo de produto."""
    rows = execute_query(LISTAR_CLIENTES_SQL)
    print_table_data(['ID CLIENTE', 'N COMENTARIOS', 'RANK', 'GRUPO'], [16, 18, 10, 15], rows)


if __name__ == '__main__':
    op = 99
    while op:
        print('[1] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[2] - LISTAR OS PRODUTOS SIMILARES COM MAIORES VENDAS')
        print('[3] - MOSTRAR EVOLUÇÃO DIÁRIA DAS AVALIAÇÕES')
        print('[4] - LISTAR OS 10 MAIS VENDIDOS EM CADA GRUPO DE PRODUTOS')
        print('[5] - LISTAR OS 10 PRODUTOS COM A MAIOR MÉDIA DE AVALIAÇÕES ÚTEIS POSITIVAS POR PRODUTO')
        print('[6] - LISTAR AS 5 CATEGORIAS DE PRODUTO COM A MAIOR MÉDIA DE AVALIAÇÕES ÚTEIS POSITIVAS')
        print('[7] - LISTAR OS 10 CLIENTES QUE MAIS FIZERAM COMENTÁRIOS POR GRUPO DE PRODUTO')
        print('[0] - SAIR')
        op = int(input('SELECIONE UMA DAS OPÇÕES: ').strip())
        if op == 1:
            listar_5()
        elif op == 2:
            listar_similares()
        elif op == 3:
            listar_evolucao()
        elif op == 4:
            listar_mvendidos()
        elif op == 5:
            listar_avaliacoes_produtos()
        elif op == 6:
            listar_avaliacoes_categorias()
        elif op == 7:
            listar_clientes()
