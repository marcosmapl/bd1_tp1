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


def print_table_data(header, cols_size, data):
    for c, l in zip(header, cols_size):
        print(f'{c.ljust(l)}', end='')
    print('')
    for row in data:
        for c, l in zip(row, cols_size):
            print(f'{str(c).ljust(l)}', end='')
        print('')
    print('')


if __name__ == '__main__':
    op = 99
    while op:
        print('SELECIONE UMA DAS OPÇÕES:')
        print('[1] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[2] - LISTAR OS PRODUTOS SIMILARES COM MAIORES VENDAS')
        print('[3] - MOSTRAR EVOLUÇÃO DIÁRIA DAS AVALIAÇÕES')
        print('[4] - LISTAR OS 10 MAIS VENDIDOS EM CADA GRUPO DE PRODUTOS')
        print('[5] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
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
