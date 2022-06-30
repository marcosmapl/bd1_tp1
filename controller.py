# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# TRABALHO PRÁTICO I
import re
from typing import List

from psycopg2 import extras

from database import DatabaseManager
from model import Product, SimilarProducts, Category, Review, ProductCategory


class AmazonDatasetController:
    """ Classe reponsável pela anaálise e extração dos dados diretamente do arquivo dataset. """

    # regex para identificar e separar as informações da categorias de produto, como por exemplo "Book[12345]"
    __categoria_regex = re.compile(r'(.*)\[(\d+)\]')
    # regex para identificar e separar as infomações do produto relacionados com contadores de reviews
    __review_regex = re.compile(r'\s{2}reviews:\stotal:\s(\d+)\s{2}downloaded:\s(\d+)\s{2}avg\srating:\s(\d+)')
    # regex para identificar e separar as informações de uma review do produto
    __analise_regex = re.compile(r'\s{4}(\d{4}-\d{1,2}-\d{1,2})\s{2}cutomer:\s+([A-Z0-9]+)\s{2}rating:\s+(\d+)\s{2}votes:\s+(\d+)\s{2}helpful:\s+(\d+)')

    @staticmethod
    def extrair(path: str):
        """
        Função que faz a leitura do arquivo de metadados, identificando seções de produtos e passando para extração.

        :param path: Local onde se encontra o arquivo de metadados
        :return: São retornado 5 conjuntos de objetos. Primeiramente uma lista contendo todos os objetos `Products` encontrados no arquivo de metadados.
        O segundo conjunto retornado é um dicionário com todas os objetos `Category` encontradas, já dispostos em ordem hierarquica.
        O terceiro conjunto é uma lista de objetos `ProductCategory`, ou seja, produtos e suas respectivas categorias.
        O quarto conjunto de dados é um lista de objetos `SimilarProducts`, isto é, produtos e seus similares.
        Por fim, o último conjunto é uma lista de todas os objetos `Review` de produtos.
        """
        list_products = []
        dict_categories = dict()
        list_prod_cat = []
        list_similars = []
        list_reviews = []
        # abre o arquivo de metadados para leitura
        with open(path, 'r', encoding="utf8") as arquivo:
            # pula as linhas de cabeçalho do arquivo
            for i in range(3):
                _ = arquivo.readline()
            # lista que ira receber todas as linhas de metadados de um respectivo produto
            section = []
            # percorre todas as linhas do arquivo de metadados
            for line in arquivo:
                # se a linha atual for vazia, então chegamos ao fim da seção de metadados de um produto
                if not line.strip():
                    # extrai os objetos da seção do produto e salva nos conjuntos
                    p, c, pc, s, r = AmazonDatasetController.__extrair_itens(section)
                    list_products.append(p)
                    dict_categories.update(c)
                    list_prod_cat.extend(pc)
                    list_similars.extend(s)
                    list_reviews.extend(r)
                    # extraido os objetos, esvaziamos toda a seção e pulamos para a próxima linha do arquivo
                    section = []
                    continue
                # se a linha atual não for vazia, então ela contém metadados e deve ser adicionada a seção do produto
                section.append(line)
        return list_products, dict_categories, list_prod_cat, list_similars, list_reviews

    @staticmethod
    def __extrair_itens(section: List[str]):
        """
        Esta função recebe uma seção (lista de strings) de metadados de um produto e faz a extração dos objetos contidos.

        :param section: Seção de metadados do produto
        :return: Os conjuntos de dados com os objetos contidos na seção.
        """
        list_similars = []
        list_reviews = []
        list_prod_cat = []
        dict_categories = dict()
        # as primeiras duas linhas da seção são referentes ao ID e ASIN do produto, respectivamente.
        produto_obj = Product(int(section[0][3:].strip()), section[1][5:].strip())
        # uma vez extraídas podemos dispensa as duas primeiras linhas
        section = section[2:]
        # se restarem menos de 2 linhas de metadados na seção, então temos uma produto discontinuado, caso contrário devemos prosseguir com a extração
        if len(section) < 2:
            produto_obj.title = section[0].strip()
        else:
            # se tivermos mais de 2 linhas restantes de metadados, seguimos com a extração
            # as próximas linhas correspondem respectivamente ao `título`, `grupo do produto` e o `rank de vendas`
            produto_obj.title = section[0][8:].strip().upper()
            produto_obj.product_group = section[1][8:].strip().upper()
            produto_obj.salesrank = int(section[2][12:].strip())
            # em seguida, verificamos se na linha de produtos similares, a quantidade é maior que `zero`
            similares_data = section[3][11:-1].split('  ')
            if int(similares_data[0]):
                # caso afirmativo, extraímos os códigos ASIN de todos os produtos similares
                for pasin in similares_data[1:]:
                    list_similars.append(SimilarProducts(produto_obj.asin, pasin))
            # a próxima etapa é identificar se existem categorias
            n_categories = int(section[4][14:-1])
            # excluímos as linhas já processadas até aqui
            section = section[5:]
            if n_categories:
                # se existirem linhas de categorias prossegue com a extração
                for cat_line in section[:n_categories]:
                    # as categorias estão organizadas em níveis hierarquicos, logo, cada uma pode ou não ter uma categoria pai
                    # a primeira categoria de cada linha, é o nível mais alto e por isso não possui uma categoria pai
                    cat_father_code = None
                    categories_data = [AmazonDatasetController.__categoria_regex.search(x).groups() for x in cat_line[4:-1].split('|')]
                    for cat_data in categories_data:
                        cat_obj = Category(int(cat_data[1]), str(cat_data[0]).strip().upper(), cat_father_code)
                        dict_categories[cat_obj.category_id] = cat_obj
                        cat_father_code = cat_obj.category_id
                    list_prod_cat.append(ProductCategory(produto_obj.product_id, int(categories_data[-1][1])))
            # excluímos as linhas extraídas até aqui
            section = section[n_categories:]
            # extraímos os atributos relacionados com contadores de reviews
            review_data = AmazonDatasetController.__review_regex.search(section[0][:-1]).groups()
            produto_obj.review_total = int(review_data[0])
            produto_obj.review_downloaded = int(review_data[1])
            produto_obj.review_avg = float(review_data[2])
            # mais uma vez excluímos as linhas já extraídas
            section = section[1:]
            # por fim, se restarem linhas na seção, estas serão reviews
            for review_line in section:
                review_data = AmazonDatasetController.__analise_regex.search(review_line).groups()
                review_obj = Review(produto_obj.product_id, review_data[1], review_data[0])
                review_obj.rating = int(review_data[2])
                review_obj.votes = int(review_data[3])
                review_obj.helpful = int(review_data[4])
                list_reviews.append(review_obj)
        print(f'PRODUCT EXTRACTED ID: {produto_obj.product_id}')
        return produto_obj, dict_categories, list_prod_cat, list_similars, list_reviews


class ModelEntityController:
    """Classe controller que implementa as funções de CRUD de objetos no banco de dados"""

    @classmethod
    def _insert_one(cls, row, table_name: str, attr_list):
        """
        Esta função recebe um registro (tupla) e o insere na respectiva tabela do banco de dados.

        :param row: Uma tupla de valores (registro) a serem inseridos na tabela
        :param table_name: Nome da tabela
        :param attr_list: Uma lista com os nomes dos respectivos atributos (campos da tabela) cujos valores estão no registro.
        :return:
        """
        # constroi o comando SQL para inserção do registro na tabela
        fields = ', '.join(attr_list)
        params = ', '.join(['%s' for _ in attr_list])
        query = f"INSERT INTO {table_name} ({fields}) VALUES ({params})"
        # recupera a conexão com o sgbd
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        cursor = connection.cursor()
        # executa o comando SQL
        cursor.execute(query, row)
        connection.commit()
        return cursor.rowcount

    @classmethod
    def _insert_many(cls, rows, table_name: str, attr_list):
        """
        Esta função recebe registros (tuplas) e os insere na respectiva tabela do banco de dados.

        :param rows: As tuplas de valores (registros) a serem inseridos na tabela
        :param table_name: Nome da tabela
        :param attr_list: Uma lista com os nomes dos respectivos atributos (campos da tabela) cujos valores estão no registro.
        :return:
        """
        # constroi o comando SQL para inserção do registro na tabela
        attr_names = ','.join(attr_list)
        sql_query = f'INSERT INTO {table_name} ({attr_names}) VALUES %s'
        # recupera a conexão com o sgbd
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        cursor = connection.cursor()
        # executa o comando SQL
        extras.execute_values(cursor, sql_query, rows)
        connection.commit()
        return cursor.rowcount

    @classmethod
    def _fetch_all(cls, table_name: str):
        """
        Esta função recupera todos os registros de uma dada tabela do banco de dados.

        :param table_name: Nome da tabela do banco de dados.
        :return: Os registros (tuplas) encontrados na tabela.
        """
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        return cursor.fetch_all()

    @classmethod
    def _fetch_by_text_field(cls, table_name: str, field_value: str, field_name: str, exact=True, limit=None):
        """
        Esta função recupera registros (tuplas) de uma tabela do banco de dados por meio de uma busca pelo valor textual de um compo informado.

        :param table_name: Nome da tabela do banco de dados.
        :param field_value: Valor do campo a ser utilizado na busca.
        :param field_name: Nome do compo da tabela.
        :param exact: Booleano que indica se a busca deve ser pelo valor exato ou não.
        :param limit: Limite de registros a serem retornados. Caso seja "None", todos os registros encontrados serão retornados.
        :return: Os registros (tuplas) encontrados pela busca.
        """
        params = [field_value]
        if limit:
            params.append(limit)
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        rows = connection.query(
            f'SELECT * FROM {table_name} WHERE {field_name} {"LIKE %s" if not exact else "= %s"}{"" if not limit else " LIMIT %s"}',
            tuple(params)
        )
        return rows

    @classmethod
    def _fetch_by_numerical_field(cls, table_name: str, field_value: int, field_name: str, limit=None):
        """
         Esta função recupera registros (tuplas) de uma tabela do banco de dados por meio de uma busca pelo valor inteiro de um compo informado.

        :param table_name: Nome da tabela do banco de dados.
        :param field_value: Valor do campo a ser utilizado na busca.
        :param field_name: Nome do compo da tabela.
        :param limit: Limite de registros a serem retornados. Caso seja "None", todos os registros encontrados serão retornados.
        :return: Os registros (tuplas) encontrados pela busca.
        """
        params = [field_value]
        if limit:
            params.append(limit)
        return DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB).query(
            f'SELECT * FROM {table_name}{f" WHERE {field_name}=%s"}{"" if not limit else " LIMIT %s"}',
            tuple(params)
        )


class ProductController(ModelEntityController):
    """Classe que implementa as funções de CRUD para objetos `Product`."""
    __TABLE_NAME = 'product'

    @classmethod
    def insert_one(cls, element: Product):
        """
        Esta função insere um novo registro na tabela `product` com o valores provenientes de um objeto `Product`.

        :param element: O objeto `Product` cujos valores deverão ser inseridos.
        :return: Um inteiro maior que `zero` se registro foi inserido com sucesso.
        """
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, Product.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[Product]):
        """
        Esta função insere novos registros na tabela `Product` com os valores provenientes de uma lista de objetos `Product`.

        :param elements: A lista com os objetos `Product` cujos valores deverão ser inseridos como novos registros da tabela.
        :return: Um inteiro maior que `zero` se registros foram inseridos com sucesso.
        """
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, Product.attr_list())

    @classmethod
    def fetch_all(cls):
        """
        Esta função recupera todos os registros da tabela `Product` mapeados para uma lista de objetos `Product`.

        :return: Uma lista contendo os registros da tabela, mapeados para objetos `Product`.
        """
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `product` por meio de uma busca por um parametro textual num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `Product`.

        :param field_value: O valor textual do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param exact: Booleano que indica se a busca textual deve ser exata ou não.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `Product`
        """
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `product` por meio de uma busca por um parametro inteiro num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `Product`.

        :param field_value: O valor inteiro do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `Product`
        """
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)


class CategoryController(ModelEntityController):
    """Classe que implementa as funções de CRUD para objetos `Category`."""
    __TABLE_NAME = 'category'

    @classmethod
    def insert_one(cls, element: Category):
        """
        Esta função insere um novo registro na tabela `category` com o valores provenientes de um objeto `Category`.

        :param element: O objeto `Category` cujos valores deverão ser inseridos.
        :return: Um inteiro maior que `zero` se registro foi inserido com sucesso.
        """
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, Category.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[Category]):
        """
         Esta função insere novos registros na tabela `category` com os valores provenientes de uma lista de objetos `Category`.

         :param elements: A lista com os objetos `Category` cujos valores deverão ser inseridos como novos registros da tabela.
         :return: Um inteiro maior que `zero` se registros foram inseridos com sucesso.
         """
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, Category.attr_list())

    @classmethod
    def fetch_all(cls):
        """
        Esta função recupera todos os registros da tabela `category` mapeados para uma lista de objetos `Category`.

        :return: Uma lista contendo os registros da tabela, mapeados para objetos `Category`.
        """
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `category` por meio de uma busca por um parametro textual num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `Category`.

        :param field_value: O valor textual do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param exact: Booleano que indica se a busca textual deve ser exata ou não.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `Category`
        """
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `category` por meio de uma busca por um parametro inteiro num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `Category`.

        :param field_value: O valor inteiro do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `Category`
        """
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)


class ProductCategoryController(ModelEntityController):
    """Classe que implementa as funções de CRUD para objetos `ProductCategory`."""
    __TABLE_NAME = 'product_category'

    @classmethod
    def insert_one(cls, element: ProductCategory):
        """
        Esta função insere um novo registro na tabela `product_category` com o valores provenientes de um objeto `ProductCategory`.

        :param element: O objeto `ProductCategory` cujos valores deverão ser inseridos.
        :return: Um inteiro maior que `zero` se registro foi inserido com sucesso.
        """
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, ProductCategory.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[ProductCategory]):
        """
         Esta função insere novos registros na tabela `product_category` com os valores provenientes de uma lista de objetos `ProductCategory`.

         :param elements: A lista com os objetos `ProductCategory` cujos valores deverão ser inseridos como novos registros da tabela.
         :return: Um inteiro maior que `zero` se registros foram inseridos com sucesso.
         """
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, ProductCategory.attr_list())

    @classmethod
    def fetch_all(cls):
        """
        Esta função recupera todos os registros da tabela `product_category` mapeados para uma lista de objetos `ProductCategory`.

        :return: Uma lista contendo os registros da tabela, mapeados para objetos `ProductCategory`.
        """
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `product_category` por meio de uma busca por um parametro textual num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `ProductCategory`.

        :param field_value: O valor textual do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param exact: Booleano que indica se a busca textual deve ser exata ou não.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `ProductCategory`
        """
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `product_category` por meio de uma busca por um parametro inteiro num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `ProductCategory`.

        :param field_value: O valor inteiro do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `ProductCategory`
        """
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)


class SimilarProductsController(ModelEntityController):
    """Classe que implementa as funções de CRUD para objetos `SimilarProducts`."""
    __TABLE_NAME = 'similar_products'

    @classmethod
    def insert_one(cls, element: SimilarProducts):
        """
        Esta função insere um novo registro na tabela `similar_products` com o valores provenientes de um objeto `SimilarProducts`.

        :param element: O objeto `SimilarProducts` cujos valores deverão ser inseridos.
        :return: Um inteiro maior que `zero` se registro foi inserido com sucesso.
        """
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, SimilarProducts.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[SimilarProducts]):
        """
         Esta função insere novos registros na tabela `similar_products` com os valores provenientes de uma lista de objetos `SimilarProducts`.

         :param elements: A lista com os objetos `SimilarProducts` cujos valores deverão ser inseridos como novos registros da tabela.
         :return: Um inteiro maior que `zero` se registros foram inseridos com sucesso.
         """
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, SimilarProducts.attr_list())

    @classmethod
    def fetch_all(cls):
        """
        Esta função recupera todos os registros da tabela `similar_products` mapeados para uma lista de objetos `SimilarProducts`.

        :return: Uma lista contendo os registros da tabela, mapeados para objetos `SimilarProducts`.
        """
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `similar_products` por meio de uma busca por um parametro textual num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `SimilarProducts`.

        :param field_value: O valor textual do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param exact: Booleano que indica se a busca textual deve ser exata ou não.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `SimilarProducts`
        """
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `similar_products` por meio de uma busca por um parametro inteiro num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `SimilarProducts`.

        :param field_value: O valor inteiro do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `SimilarProducts`
        """
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)


class ReviewController(ModelEntityController):
    """Classe que implementa as funções de CRUD para objetos `Review`."""
    __TABLE_NAME = 'review'

    @classmethod
    def insert_one(cls, element: Review):
        """
        Esta função insere um novo registro na tabela `review` com o valores provenientes de um objeto `Review`.

        :param element: O objeto `Review` cujos valores deverão ser inseridos.
        :return: Um inteiro maior que `zero` se registro foi inserido com sucesso.
        """
        return ModelEntityController._insert_one(element.to_tuple(), cls.__TABLE_NAME, Review.attr_list())

    @classmethod
    def insert_batch(cls, elements: List[Review]):
        """
         Esta função insere novos registros na tabela `review` com os valores provenientes de uma lista de objetos `Review`.

         :param elements: A lista com os objetos `Review` cujos valores deverão ser inseridos como novos registros da tabela.
         :return: Um inteiro maior que `zero` se registros foram inseridos com sucesso.
         """
        return ModelEntityController._insert_many([x.to_tuple() for x in elements], cls.__TABLE_NAME, Review.attr_list())

    @classmethod
    def fetch_all(cls):
        """
        Esta função recupera todos os registros da tabela `review` mapeados para uma lista de objetos `Review`.

        :return: Uma lista contendo os registros da tabela, mapeados para objetos `Review`.
        """
        return ModelEntityController._fetch_all(cls.__TABLE_NAME)

    @classmethod
    def fetch_by_text_field(cls, field_value: str, field_name: str, exact=True, limit=None):
        """
        Esta função recupera uma seleção de registros da tabela `review` por meio de uma busca por um parametro textual num dos campos da tabela.
        Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `Review`.

        :param field_value: O valor textual do campos no registros desejados.
        :param field_name: O nome do campo a ser utilizado na busca.
        :param exact: Booleano que indica se a busca textual deve ser exata ou não.
        :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
        :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `Review`
        """
        return ModelEntityController._fetch_by_text_field(cls.__TABLE_NAME, field_value, field_name, exact, limit)

    @classmethod
    def fetch_by_numerical_field(cls, field_value: int, field_name: str, limit=None):
        """
         Esta função recupera uma seleção de registros da tabela `review` por meio de uma busca por um parametro inteiro num dos campos da tabela.
         Os registros que satisfizerem o critério de busca serão mapeados e retornados numa lista de objetos `Review`.

         :param field_value: O valor inteiro do campos no registros desejados.
         :param field_name: O nome do campo a ser utilizado na busca.
         :param limit: Inteiro que especifica o número máximo (limite) de registros a serem retornados, caso seja "None" todos os registros encontrados serão retornados.
         :return: Os registros, que satisfizerem o critério de buscar, mapeados num lista de objetos `Review`
         """
        return ModelEntityController._fetch_by_numerical_field(cls.__TABLE_NAME, field_value, field_name, limit)
