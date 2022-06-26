# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# TRABALHO PRÁTICO I
from controller import AmazonDatasetController, ProductController
from database import DatabaseManager

AMAZON_DATASET_FILEPATH = 'amazon-meta.txt'

if __name__ == '__main__':
    # DatabaseManager.create_tables(DatabaseManager.POSTGRESQL_DB)
    items = AmazonDatasetController().extrair(AMAZON_DATASET_FILEPATH)
    for item in items:
        produto = item[0]
        print(produto)
        rows = ProductController.insert_one(produto)
        print(f'Inserted {rows} rows\n')
    DatabaseManager.close_connection()
