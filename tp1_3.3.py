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
    asin = input()
    params = (asin, asin)
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
    cursor = conn.cursor()
    cursor.execute(
        f'((SELECT product.product_id, product.asin, review.customer_id, review.review_date, review.rating, review.helpful FROM product, review WHERE product.product_id=%s ORDER BY rating DESC, helpful DESC LIMIT 5) UNION ALL (SELECT product.product_id, product.asin, review.customer_id, review.review_date, review.rating, review.helpful FROM product, review WHERE product.product_id=%s ORDER BY rating ASC, helpful DESC LIMIT 5));',
        tuple(params)
    )
    rows = cursor.fetchall()
    cols_names = ['ID', 'ASIN', 'CUSTOMER ID', 'REVIEW DATE', 'RATING', 'HELPFUL']
    print('\t\t\t\t'.join(cols_names))
    for row in rows:
        print('\t\t\t\t'.join([str(x) for x in row]))
    print('')


def listar_similares():
    pass


if __name__ == '__main__':
    op = 99
    while op:
        print('SELECIONE UMA DAS OPÇÕES:')
        print('[1] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[2] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[3] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[4] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[5] - LISTAR OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MAIOR AVALIAÇÃO E OS 5 COMENTÁRIOS MAIS ÚTEIS E COM MENOR AVALIAÇÃO')
        print('[0] - SAIR')
        op = int(input().strip())
        if op == 1:
            listar_5()
        elif op == 2:
            listar_similares()
