# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
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
    """
    Entidade que representa um Produto.

    Attributes
        product_id : int
            Número identificado do produto dentro da base da amazon.
        asin : str
            Número de identificação padronizada da Amazon.
        title : str
            Título do produto.
        product_group : str
            Grupo ao qual o produto pertence (BABY PRODUCT | BOOK | CE | DVD | MUSIC | SOFTWARE | SPORTS | TOY | VIDEO | VIDEO GAMES).
        salesrank : int
            Posição do produto no rank de vendas.
        review_total : int
            Total de reviews atribuídas ao produto.
        review_downloaded : int
            Total de reviews disponibilizadas no arquivo de metadados.
        review_avg : int
            Valor médio das reviews atribuídas ao produto.

    Methods
        to_tuple():
            Retorna o produto num formato de tupla.
        attr_list():
            Retorna uma lista com os nomes dos atributos (campos) do objeto produto.
    """

    def __init__(self, product_id: int, asin: str, title: str = None, product_group: str = None, salesrank: int = None, review_total: int = None, review_downloaded: int = None, review_avg: float = None):
        """
        Método construtor da classe `Product`.

        :param product_id: Identificador único do produto.
        :param asin: ASIN do produto.
        :param title: Título do produto.
        :param product_group: Grupo ao qual o produto pertence.
        :param salesrank: Posição do produto no rank de vendas.
        :param review_total: Total de reviews atribuídas ao produto.
        :param review_downloaded: Total de reviews disponíveis no arquivo de metadados.
        :param review_avg: Média das notas de reviews do produto.
        """
        self.product_id = product_id
        self.asin = asin
        self.title = title
        self.product_group = product_group
        self.salesrank = salesrank
        self.review_total = review_total
        self.review_downloaded = review_downloaded
        self.review_avg = review_avg
        # for name in ['title', 'product_group', 'salesrank', 'review_total', 'review_downloaded', 'review_avg']:
        #     setattr(self, name, None)

    def to_tuple(self):
        """Retorna o produto num formato de tupla."""
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        """Retorna uma lista com os nomes dos atributos (campos) do objeto produto."""
        return list(Product(-1, "").__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class SimilarProducts(ModelEntity):
    """
    Entidade que representa uma relação de Produto (n) x Produto (n) indicando que são similares.

    Attributes
        product_asin : str
            ASIN do produto.
        similar_asin : str
            ASIN do produto similar.

    Methods
        to_tuple():
            Retorna os valores do objeto similaridade numa tupla.
        attr_list():
            Retorna uma lista com os nomes dos atributos (campos) do objeto similaridade.
    """

    def __init__(self, product_asin: str, similar_asin: str):
        """
        Método construtor da classe `SimilarProducts`.

        :param product_asin: ASIN do produto.
        :param similar_asin: ASIN do produto similar.
        """
        self.product_asin = product_asin
        self.similar_asin = similar_asin

    def to_tuple(self):
        """Retorna os valores do objeto similaridade numa tupla."""
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        """Retorna uma lista com os nomes dos atributos (campos) do objeto similaridade."""
        return list(SimilarProducts("", "").__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class Category(ModelEntity):
    """
    Entidade que representa um Categoria de produtos.

    Attributes
        category_id : int
            Número identificador único da categoria.
        name : str
            Descrição da categoria.
        parent_id : int
            Número identificador da categoria hierarquicamente superior, assume o valor "None" caso não exista.

    Methods
        to_tuple():
            Retorna os valores do objeto categoria numa tupla.
        attr_list():
            Retorna uma lista com os nomes dos atributos (campos) do objeto categoria.
    """

    def __init__(self, category_id: int, name: str, parent_id: int = None):
        """
        Método construtor da classe `Category`.

        :param category_id: Idnetificador único da categoria.
        :param name: Descrição da categoria.
        :param parent_id: Identificador único da categoria hierarquicamente superior, ou `None` caso não exista.
        """
        self.category_id = category_id
        self.name = name
        self.parent_id = parent_id

    def to_tuple(self):
        """Retorna os valores do objeto categoria numa tupla."""
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        """Retorna uma lista com os nomes dos atributos (campos) do objeto categoria."""
        return list(Category(-1, "").__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class ProductCategory(ModelEntity):
    """
    Entidade que representa uma relação Category x `Product` (N x N).

    Attributes
        product_id : int
            Número identificador único do produto.
        category_id : int
            Número identificador único da categoria.

    Methods
        to_tuple():
            Retorna os valores do objeto numa tupla.
        attr_list():
            Retorna uma lista com os nomes dos atributos (campos) do objeto.
    """

    def __init__(self, product_id: id, category_id: int):
        """
        Método construtor da classe `ProductCategory`.

        :param product_id: Número identificador único de um `Product`.
        :param category_id: Número identificador único de uma `Category`.
        """
        self.product_id = product_id
        self.category_id = category_id

    def to_tuple(self):
        """Retorna os valores do objeto numa tupla."""
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        """Retorna uma lista com os nomes dos atributos (campos) do objeto."""
        return list(ProductCategory(-1, -1).__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class Review(ModelEntity):
    """
    Entidade que representa uma review de um dado Produto, feita por um Cliente.

    Attributes
        product_id : int
            Número identificador único do produto.
        customer_id : int
            Número identificador único do cliente.
        review_date : str
            Data em que a review foi submetida (YYYY-MM-DD).
        rating: int
            Nota atribuída ao produto (1-5).
        votes: int
            Número de votos recebidos pela review.
        helpul: int
            Número de clientes que consideram a review útil.

    Methods
        to_tuple():
            Retorna os valores do objeto review numa tupla.
        attr_list():
            Retorna uma lista com os nomes dos atributos (campos) do objeto review.
    """

    def __init__(self, product_id: int, customer_id: str, review_date: str, rating=None, votes=None, helpful=None):
        """
        Método construtor da classe Review.

        :param product_id: Idenctificador único da review.
        :param customer_id: Código do cliente que fez a review.
        :param review_date: Data de publicação da review.
        :param rating: Nota atribuída ao produto (1-5).
        :param votes: Número de votos recebidos pela review.
        :param helpful: Número de clientes que consideram a review útil.
        """
        self.product_id = product_id
        self.customer_id = customer_id
        self.review_date = review_date
        self.rating = rating
        self.votes = votes
        self.helpful = helpful
        # for name in ['rating', 'votes', 'helpful']:
        #     setattr(self, name, None)

    def to_tuple(self):
        """Retorna os valores do objeto review numa tupla."""
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    @staticmethod
    def attr_list():
        """Retorna uma lista com os nomes dos atributos (campos) do objeto review."""
        return list(Review(-1, "", "").__dict__)[:]

    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)
