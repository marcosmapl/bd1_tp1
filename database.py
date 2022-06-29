# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# TRABALHO PRÁTICO I
from configparser import ConfigParser

import psycopg2
import os


class DatabaseManager:
    """
    Classe responsável pela criação do banco de dados e gerenciamento das conexões com o SGBD.

    As conexões com o SGBD seguem o pattern Singleton.

    Constants:
        - POSTGRESQL_DB (str): String constante com o nome do SGBD postgresql, para uso na requisição de uma conexão.
        - DATABASE_NAME (str): String constante com o nome do banco de dados utilizado nesta aplicação.

    """

    POSTGRESQL_DB = 'postgresql'
    DATABASE_NAME = 'amazon'
    __db_config_filename = 'database.ini' # nome do arquivo de configurações da conexão com o sgbd
    __connection = None # objeto singleton de conexão com o sgbd

    @classmethod
    def __get_connection_params(cls, sgbd_name: str):
        """
        Esta função carrega os parametros de conexão do arquivo de configurações e coloca-os num dicionário.

        Args:
            sgbd_name (str): Nome do SGDB a ser utilizado (POSTGRESQL_DB).

        Raises:
            FileNotFoundError: Caso o arquivo de configurações não seja encontrado na pasta atual.
            Exception: Caso a seção para o SGBD escolhido não sejam encontradas no arquivo de configurações.
        """
        # verifica se o arquivo de configurações existe
        if os.path.exists(DatabaseManager.__db_config_filename):
            # criar um objeto parser e carrega o arquivo de configurações
            parser = ConfigParser()
            parser.read(DatabaseManager.__db_config_filename)
            # se a seção escolhida (sgbd) estiver presente no arquivo, carrega os parametros para um dicionário
            if parser.has_section(sgbd_name):
                params = parser.items(sgbd_name)
                db = dict(params)
                return db
            else:
                raise Exception(f'Section {sgbd_name} not found in the {DatabaseManager.__db_config_filename} file')
        else:
            raise FileNotFoundError(f'O arquivo {DatabaseManager.__db_config_filename} de configurações para o sgbd {sgbd_name} não foi encontrado!')

    @classmethod
    def get_connection(cls, sgbd_name: str):
        """
        Esta função é responsável por fonecer o objeto Singleton de conexão com o SGBD.

        Caso o objeto de conexão não exista ou a conexão estiver fechada, abre uma nova conexão num novo objeto.

        Args:
            sgbd_name (str): Nome do SGDB a ser utilizado (POSTGRESQL_DB | MYSQL_DB).
        """
        if not DatabaseManager.__connection or DatabaseManager.__connection.closed:
            DatabaseManager.__connection = psycopg2.connect(**DatabaseManager.__get_connection_params(sgbd_name))
        return DatabaseManager.__connection

    @classmethod
    def close_connection(cls):
        """
        Esta função é responsável por fechar a conexão ativa com o SGBD.

        Caso o objeto de conexão não exista ou a conexão estiver fechada, abre uma nova conexão num novo objeto.

        Args:
            sgbd_name (str): Nome do SGDB a ser utilizado (POSTGRESQL_DB | MYSQL_DB).
        """
        if DatabaseManager.__connection and not DatabaseManager.__connection.closed:
            DatabaseManager.__connection.close()

    @classmethod
    def create_database(cls, sgbd_name: str):
        """
        Esta função é responsável por estabelecer a primeira conexão com o SGBD, criar o schema do banco de dados, tabelas e relacionamentos.

        A primeira conexão feita é para criar o schema do banco de dados, por isso conectamos diretamente no banco de dados padrão do sgbd.

        Args:
            sgbd_name (str): Nome do SGDB a ser utilizado (POSTGRESQL_DB | MYSQL_DB).
        """
        db_params = DatabaseManager.__get_connection_params(sgbd_name)
        db_params['database'] = 'postgres'
        conn = psycopg2.connect(db_params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {sgbd_name}")
        conn.close()
        # lê e executa o script de criação das tabelas do banco de dados
        with open('db_create.sql', 'r') as db_file:
            sql = ''.join(db_file.readlines())
            conn = DatabaseManager.get_connection(sgbd_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()
            conn.commit()
            conn.close()
