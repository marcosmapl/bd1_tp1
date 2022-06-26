# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# TRABALHO PRÁTICO I
from controller import AmazonDatasetController, ProductController, CategoryController, ProductCategoryController, SimilarProductsController, ReviewController
from database import DatabaseManager
from datetime import datetime

AMAZON_DATASET_FILEPATH = 'amazon-meta.txt'

if __name__ == '__main__':
    start_time = datetime.now()
    DatabaseManager.create_tables(DatabaseManager.POSTGRESQL_DB)
    products, categories, prod_cats, similars, reviews = AmazonDatasetController().extrair(AMAZON_DATASET_FILEPATH)

    ProductController.insert_batch(products)
    print(f'{len(products)} PRODUCTS INSERTED INTO DATABASE')
    CategoryController.insert_batch(categories.values())
    print(f'{len(categories.values())} CATEGORIES INSERTED INTO DATABASE')
    ProductCategoryController.insert_batch(prod_cats)
    print(f'{len(prod_cats)} PRODUCT CATEGORIES INSERTED INTO DATABASE')
    SimilarProductsController.insert_batch(similars)
    print(f'{len(similars)} SIMILARS PRODUCTS INSERTED INTO DATABASE')
    ReviewController.insert_batch(reviews)
    print(f'{len(reviews)} PRODUCT REVIEWS INSERTED INTO DATABASE')
    # for item in items:
    #     produto = item[0]
    #     print(produto)
    #     rows = ProductController.insert_one(produto)
    DatabaseManager.close_connection()
    print(f'TIME ELAPSED: {datetime.now() - start_time}')
