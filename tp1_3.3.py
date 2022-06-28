# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# TRABALHO PRÁTICO I
from database import DatabaseManager


def print_table_data(header, cols_size, data):
    for c, l in zip(header, cols_size):
        print(f'{c.ljust(l)}', end='')
    print('')
    for row in data:
        for c, l in zip(row, cols_size):
            print(f'{str(c).ljust(l)}', end='')
        print('')
    print('')


def listar_5():
    print('INFORME O ID DO PRODUTO:')
    id = input()
    params = (id, id)
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'((SELECT product.product_id, product.asin, review.customer_id, review.review_date, review.rating, review.helpful FROM product, review WHERE product.product_id=%s ORDER BY rating DESC, helpful DESC LIMIT 5) UNION ALL (SELECT product.product_id, product.asin, review.customer_id, review.review_date, review.rating, review.helpful FROM product, review WHERE product.product_id=%s ORDER BY rating ASC, helpful DESC LIMIT 5))',
        tuple(params)
    )
    rows = cursor.fetchall()
    print_table_data(['ID', 'ASIN', 'CUSTOMER ID', 'REVIEW DATE', 'RATING', 'HELPFUL'], [8, 11, 12, 10, 10, 5], rows)


def listar_similares():
    print('INFORME O ID DO PRODUTO:')
    id = input()
    params = (id,)
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT product.title, product.salesrank, psimilar.title, psimilar.salesrank FROM product JOIN similar_products ON product.asin=similar_products.product_asin JOIN product as psimilar ON psimilar.asin=similar_products.similar_asin WHERE product.product_id=%s AND psimilar.salesrank>product.salesrank',
        tuple(params)
    )
    rows = cursor.fetchall()
    print_table_data(['TITULO PRODUTO', 'SALESRANK', 'TITULO SIMILAR', 'SALESRANK'], [80, 12, 80, 12], rows)


def listar_evolucao():
    print('INFORME O ID DO PRODUTO:')
    id = input()
    params = (id,)
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT product.title, review.review_date, round(avg(review.rating), 2) FROM product INNER JOIN review ON product.product_id=review.product_id WHERE product.product_id=%s GROUP BY product.title, review.review_date ORDER BY review_date ASC',
        tuple(params)
    )
    rows = cursor.fetchall()
    print_table_data(['TITULO', 'DATA', 'MÉDIA DE AVALIAÇÕES'], [150, 14, 10], rows)


def listar_mvendidos():
    print('\t\t\t\tPRODUTOS MAIS VENDIDOS POR GRUPO')
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT title, salesrank, product_group FROM (SELECT title, salesrank, product_group, Rank() over (Partition BY product_group ORDER BY salesrank DESC ) AS Rank FROM product WHERE salesrank > 0) rs WHERE Rank <= 10'
    )
    rows = cursor.fetchall()
    print_table_data(['TITULO', 'RANK VENDAS', 'GRUPO'], [150, 15, 13], rows)


def listar_comentarios():
    print('\t\t\t\tCLIENTES COM MAIS COMENTÁRIOS POR GRUPO DE PRODUTO')
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT customer_id, n_reviews, review_rank, product_group FROM (SELECT customer_id, n_reviews, product_group, ROW_NUMBER() OVER (PARTITION BY t1.product_group ORDER BY t1.n_reviews DESC) AS review_rank FROM (SELECT customer_id, count(customer_id) AS n_reviews, product_group FROM product INNER JOIN review ON product.product_id=review.product_id GROUP BY (product_group, customer_id)) AS t1 ORDER BY t1.product_group ASC, t1.n_reviews DESC) AS t2 WHERE review_rank <= 10'
    )
    rows = cursor.fetchall()
    print_table_data(['ID CLIENTE', 'N COMENTARIOS', 'RANK', 'GRUPO'], [16, 10, 5, 15], rows)


def listar_avaliacoes_produtos():
    print('\t\t\t\tPRODUTOS COM MAIOR MÉDIA DE AVALIAÇÕES ÚTEIS POSITIVAS POR PRODUTO   ')
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT t2.product_id, t2.title, t2.product_group, t2.avg_helpful, t2.n_rank FROM (SELECT product.product_id, product.title, product.product_group, t1.avg_helpful, ROW_NUMBER() OVER (PARTITION BY product.product_group ORDER BY t1.avg_helpful DESC) AS n_rank FROM product JOIN (SELECT review.product_id, round(avg(review.helpful), 2) AS avg_helpful FROM review WHERE review.helpful > 0 GROUP BY review.product_id) t1 ON t1.product_id=product.product_id) as t2 WHERE n_rank <= 10'
    )
    rows = cursor.fetchall()
    print_table_data(['ID PRODUTO', 'TITULO', 'GRUPO', 'MEDIA AV', 'RANK'], [12, 150, 15, 12, 5], rows)


def listar_avaliacoes_categorias():
    print('\t\t\t\tCATEGORIAS COM MAIOR MÉDIA DE AVALIAÇÕES ÚTEIS POSITIVAS POR PRODUTO   ')
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'select category.name, round(t_avg.avg, 2) from category inner join (select product_category.category_id, avg(qtd_pos.count) from product_category inner join (select review.product_id, count(*) from review where review.helpful > 0 group by review.product_id) qtd_pos on qtd_pos.product_id = 	product_category.product_id group by product_category.category_id having  avg(qtd_pos.count) > 0 order by avg desc limit 5) t_avg on category.category_id  =  t_avg.category_id;'
    )
    rows = cursor.fetchall()
    print_table_data(['NOME CATEGORIA', 'MEDIA AV'], [50, 12], rows)


if __name__ == '__main__':
    op = 99
    while op:
        print('SELECIONE UMA DAS OPÇÕES:')
        print('[1] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[2] - LISTAR OS PRODUTOS SIMILARES COM MAIORES VENDAS')
        print('[3] - MOSTRAR EVOLUÇÃO DIÁRIA DAS AVALIAÇÕES')
        print('[4] - LISTAR OS 10 MAIS VENDIDOS EM CADA GRUPO DE PRODUTOS')
        print('[5] - LISTAR OS 10 PRODUTOS COM A MAIOR MÉDIA DE AVALIAÇÕES ÚTEIS POSITIVAS POR PRODUTO')
        print('[6] - LISTAR OS 10 PRODUTOS COM A MAIOR MÉDIA DE AVALIAÇÕES ÚTEIS POSITIVAS POR PRODUTO')
        print('[7] - LISTAR OS 10 CLIENTES QUE MAIS FIZERAM COMENTÁRIOS POR GRUPO DE PRODUTO')
        print('[0] - SAIR')
        op = int(input().strip())
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
            listar_comentarios()
