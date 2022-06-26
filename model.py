# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# TRABALHO PRÁTICO I

class ModelEntity:
    """Interface que especifica os métodos de uma Entidade do Modelo de dados necessita implementar"""

    def to_tuple(self):
        """Retorna os valores dos atributos (campos) da Entidade organizados numa tupla (row)"""
        pass

    @staticmethod
    def attr_list():
        """Retorna uma lista com o nome de todos os atributos da Entidade"""
        pass


class Product(ModelEntity):
    """Entidade que representa um Produto"""

    def __init__(self, product_id: int, asin: str):
        self.product_id = product_id
        self.asin = asin
        self.title = None
        self.product_group = None
        self.salesrank = None
        self.review_total = None
        self.review_downloaded = None
        self.review_avg = None
        # for name in ['title', 'product_group', 'salesrank', 'review_total', 'review_downloaded', 'review_avg']:
        #     setattr(self, name, None)

    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        return list(Product(-1, "").__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class SimilarProducts(ModelEntity):
    """Entidade que representa a relação Product-Product (produtos similares)"""

    def __init__(self, product_asin: str, similar_asin: str):
        self.product_asin = product_asin
        self.similar_asin = similar_asin

    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        return list(SimilarProducts("", "").__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class Category(ModelEntity):
    """Entidade que representa uma Categoria de Produtos"""

    def __init__(self, category_id: int, name: str, parent_id=None):
        self.category_id = category_id
        self.name = name
        self.parent_id = parent_id

    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        return list(Category(-1, "").__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class ProductCategory(ModelEntity):
    """Entidade que representa a relação Produto-Categoria."""

    def __init__(self, product_id: id, category_id: int):
        self.product_id = product_id
        self.category_id = category_id

    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        return list(ProductCategory(-1, -1).__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class Review(ModelEntity):
    """Entidade que representa uma Categoria de Produtos."""

    def __init__(self, product_id: id, customer_id: str, review_date: str):
        self.product_id = product_id
        self.customer_id = customer_id
        self.review_date = review_date
        self.rating = None
        self.votes = None
        self.helpful = None
        # for name in ['rating', 'votes', 'helpful']:
        #     setattr(self, name, None)

    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        return list(Review(-1, "", "").__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)
