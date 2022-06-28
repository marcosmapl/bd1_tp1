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
    cols_names = ['ID', 'ASIN', 'CUSTOMER ID', 'REVIEW DATE', 'RATING', 'HELPFUL']
    print('\t\t\t\t'.join(cols_names))
    for row in rows:
        print('\t\t\t\t'.join([str(x) for x in row]))
    print('')


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
    cols_names = ['TITULO PRODUTO', 'SALESRANK', 'TITULO SIMILAR', 'SALESRANK']
    print('\t\t\t'.join(cols_names))
    for row in rows:
        print('\t\t\t'.join([str(x) for x in row]))
    print('')


def listar_evolucao():
    print('INFORME O ID DO PRODUTO:')
    id = input()
    params = (id,)
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT product.title, review.review_date, avg(review.rating) FROM product INNER JOIN review ON product.product_id=review.product_id WHERE product.product_id=%s GROUP BY product.title, review.review_date ORDER BY review_date ASC',
        tuple(params)
    )
    rows = cursor.fetchall()
    cols_names = ['TITULO', 'DATA', 'MÉDIA DE AVALIAÇÕES']
    print('\t\t'.join(cols_names))
    for row in rows:
        print('\t'.join([str(x) for x in row]))
    print('')


if __name__ == '__main__':
    op = 99
    while op:
        print('SELECIONE UMA DAS OPÇÕES:')
        print('[1] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[2] - LISTAR OS PRODUTOS SIMILARES COM MAIORES VENDAS')
        print('[3] - MOSTRAR EVOLUÇÃO DIÁRIA DAS AVALIAÇÕES')
        print('[4] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[5] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[0] - SAIR')
        op = int(input().strip())
        if op == 1:
            listar_5()
        elif op == 2:
            listar_similares()
        elif op == 3:
            listar_evolucao()
