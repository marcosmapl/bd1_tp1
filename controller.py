# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# TRABALHO PRÁTICO I
import re
from typing import List

from psycopg2 import extras

from database import DatabaseManager
from model import Product, SimilarProducts, Category, Review, ProductCategory


class AmazonDatasetController:
    """ Classe reponsável pela anaálise e extração dos dados diretamente do arquivo dataset. """


    __categoria_regex = re.compile(r'(.*)\[(\d+)\]')
    __review_regex = re.compile(r'\s{2}reviews:\stotal:\s(\d+)\s{2}downloaded:\s(\d+)\s{2}avg\srating:\s(\d+)')
    __analise_regex = re.compile(r'\s{4}(\d{4}-\d{1,2}-\d{1,2})\s{2}cutomer:\s+([A-Z0-9]+)\s{2}rating:\s+(\d+)\s{2}votes:\s+(\d+)\s{2}helpful:\s+(\d+)')

    @staticmethod
    def extrair(path: str):
        list_products = []
        dict_categories = dict()
        list_prod_cat = []
        list_similars = []
        list_reviews = []
        with open(path, 'r', encoding="utf8") as arquivo:
            for i in range(3):
                _ = arquivo.readline()
            metadados = []
            for line in arquivo:
                if not line.strip():
                    p, c, pc, s, r = AmazonDatasetController.__extrair_itens(metadados)
                    list_products.append(p)
                    dict_categories.update(c)
                    list_prod_cat.extend(pc)
                    list_similars.extend(s)
                    list_reviews.extend(r)
                    metadados = []
                    continue
                metadados.append(line)
        return list_products, dict_categories, list_prod_cat, list_similars, list_reviews

    @staticmethod
    def __extrair_itens(metadados):
        list_similars = []
        list_reviews = []
        list_prod_cat = []
        dict_categories = dict()
        produto_obj = Product(int(metadados[0][3:].strip()), metadados[1][5:].strip())
        # if produto_obj.product_id == 49:
        #     print('achou')
        metadados = metadados[2:]
        if len(metadados) < 2:
            produto_obj.title = metadados[0].strip()
        else:
            produto_obj.title = metadados[0][8:].strip().upper()
            produto_obj.product_group = metadados[1][8:].strip().upper()
            produto_obj.salesrank = int(metadados[2][12:].strip())

            similares_data = metadados[3][11:-1].split('  ')
            if int(similares_data[0]):
                for pasin in similares_data[1:]:
                    list_similars.append(SimilarProducts(produto_obj.asin, pasin))

            n_categories = int(metadados[4][14:-1])
            metadados = metadados[5:]
            if n_categories:
                for cat_line in metadados[:n_categories]:
                    cat_father_code = None
                    categories_data = [AmazonDatasetController.__categoria_regex.search(x).groups() for x in cat_line[4:-1].split('|')]
                    for cat_data in categories_data:
                        cat_obj = Category(int(cat_data[1]), str(cat_data[0]).strip().upper(), cat_father_code)
                        dict_categories[cat_obj.category_id] = cat_obj
                        cat_father_code = cat_obj.category_id
                    list_prod_cat.append(ProductCategory(produto_obj.product_id, int(categories_data[-1][1])))

            metadados = metadados[n_categories:]
            review_data = AmazonDatasetController.__review_regex.search(metadados[0][:-1]).groups()
            produto_obj.review_total = int(review_data[0])
            produto_obj.review_downloaded = int(review_data[1])
            produto_obj.review_avg = float(review_data[2])
            metadados = metadados[1:]
            for review_line in metadados:
                review_data = AmazonDatasetController.__analise_regex.search(review_line).groups()
                review_obj = Review(produto_obj.product_id, review_data[1], review_data[0])
                review_obj.rating = int(review_data[2])
                review_obj.votes = int(review_data[3])
                review_obj.helpful = int(review_data[4])
                list_reviews.append(review_obj)
        print(f'PRODUCT EXTRACTED ID: {produto_obj.product_id}')
        return produto_obj, dict_categories, list_prod_cat, list_similars, list_reviews


class ModelEntityController:

    @classmethod
    def _insert_one(cls, element, table_name: str, attr_list):
        fields = ', '.join(attr_list)
        params = ', '.join(['%s' for _ in attr_list])
        query = f"INSERT INTO {table_name} ({fields}) VALUES ({params})"
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        cursor = connection.cursor()
        cursor.execute(query, element)
        connection.commit()
        return cursor.rowcount

    @classmethod
    def _insert_many(cls, elements, table_name: str, attr_list):
        attr_names = ','.join(attr_list)
        sql_query = f'INSERT INTO {table_name} ({attr_names}) VALUES %s'
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        cursor = connection.cursor()
        extras.execute_values(cursor, sql_query, elements)
        connection.commit()
        return cursor.rowcount

    @classmethod
    def _update(cls, elements, table_name: str, attr_list, search_field: str):
        #TODO add attr_list and new_values list as params
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        for element in elements:
            fields = '=%s, '.join(attr_list)
            query = f'UPDATE {table_name} SET {fields}=%s WHERE {search_field}=%s'
            connection.execute(query, element)
        connection.commit()
        return True

    @classmethod
    def _fetch_all(cls, table_name: str):
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        return cursor.fetch_all()

    @classmethod
    def _fetch_by_text_field(cls, table_name: str, field_value: str, field_name: str, exact=True, limit=None):
        params = [field_value]
        if limit:
            params.append(limit)
        return DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB).query(
            f'SELECT * FROM {table_name} WHERE {field_name} {"LIKE %s" if not exact else "= %s"}{"" if not limit else " LIMIT %s"}',
            tuple(params)
        )

    @classmethod
    def _fetch_by_numerical_field(cls, table_name: str, field_value: int, field_name: str, limit=None):
        params = [field_value]
        if limit:
            params.append(limit)
        return DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB).query(
            f'SELECT * FROM {table_name}{f" WHERE {field_name}=%s"}{"" if not limit else " LIMIT %s"}',
            tuple(params)
        )


class ProductController(ModelEntityController):
    __TABLE_NAME = 'product'

    @classmethod
    def insert_one(cls, element: Product):
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, Product.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[Product]):
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, Product.attr_list())

    @classmethod
    def update(cls, elements: List[Product]):
        return ModelEntityController._update([x.to_tuple()+(x.product_id,) for x in elements], cls.__TABLE_NAME, Product.attr_list(), Product.attr_list()[0])

    @classmethod
    def fetch_all(cls):
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)


class CategoryController(ModelEntityController):
    __TABLE_NAME = 'category'

    @classmethod
    def insert_one(cls, element: Category):
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, Category.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[Category]):
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, Category.attr_list())

    @classmethod
    def update(cls, elements: List[Category]):
        return ModelEntityController._update([x.to_tuple()+(x.category_id,) for x in elements], cls.__TABLE_NAME, Category.attr_list(), Category.attr_list()[0])

    @classmethod
    def fetch_all(cls):
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)


class ProductCategoryController(ModelEntityController):
    __TABLE_NAME = 'product_category'

    @classmethod
    def insert_one(cls, element: ProductCategory):
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, ProductCategory.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[ProductCategory]):
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, ProductCategory.attr_list())

    @classmethod
    def update(cls, elements: List[ProductCategory]):
        return ModelEntityController._update([x.to_tuple()+(x.product_id,) for x in elements], cls.__TABLE_NAME, ProductCategory.attr_list(), ProductCategory.attr_list()[0])

    @classmethod
    def fetch_all(cls):
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)


class SimilarProductsController(ModelEntityController):
    __TABLE_NAME = 'similar_products'

    @classmethod
    def insert_one(cls, element: SimilarProducts):
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, SimilarProducts.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[SimilarProducts]):
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, SimilarProducts.attr_list())

    @classmethod
    def update(cls, elements: List[SimilarProducts]):
        return ModelEntityController._update([x.to_tuple()+(x.product_asin,) for x in elements], cls.__TABLE_NAME, SimilarProducts.attr_list(), SimilarProducts.attr_list()[0])

    @classmethod
    def fetch_all(cls):
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)


class ReviewController(ModelEntityController):
    __TABLE_NAME = 'review'

    @classmethod
    def insert_one(cls, element: Review):
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, Review.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[Review]):
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, Review.attr_list())

    @classmethod
    def update(cls, elements: List[Review]):
        return ModelEntityController._update([x.to_tuple()+(x.product_id,) for x in elements], cls.__TABLE_NAME, Review.attr_list(), Review.attr_list()[0])

    @classmethod
    def fetch_all(cls):
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)
