# -*- coding: utf-8 -*-
# UNIVERSIDADE FEDERAL DO AMAZONAS
# INSTITUTO DE COMPUTAÇÃO
# BANCO DE DADOS I - 2020/02 (2021)
# PROFESSOR: ALTIGRAN SOARES DA SILVA
# ALUNOS: DANIEL
# ALUNOS: JELIEL
# ALUNOS: MARCOS AVNER PIMENTA DE LIMA
# TRABALHO PRÁTICO I
import psycopg2

from configparser import ConfigParser


class DatabaseManager:

    POSTGRESQL_DB = 'postgresql'
    MYSQL_DB = 'mysql'
    DATABASE_NAME = 'amazon'
    __db_config_file = 'database.ini'
    __connection = None

    @classmethod
    def __get_connection_params(cls, sgbd_name: str):
            parser = ConfigParser()
            parser.read(DatabaseManager.__db_config_file)
            db = {}
            if parser.has_section(sgbd_name):
                params = parser.items(sgbd_name)
                for param in params:
                    db[param[0]] = param[1]
            else:
                raise Exception('Section {0} not found in the {1} file'.format(sgbd_name, DatabaseManager.__db_config_file))
            return db

    @classmethod
    def get_connection(cls, sgbd_name: str):
        if not DatabaseManager.__connection or DatabaseManager.__connection.closed:
            DatabaseManager.__connection = psycopg2.connect(**DatabaseManager.__get_connection_params(sgbd_name))
        return DatabaseManager.__connection

    @classmethod
    def close_connection(cls):
        if DatabaseManager.__connection and not DatabaseManager.__connection.closed:
            DatabaseManager.__connection.close()

    @classmethod
    def create_tables(cls, sgbd_name: str):
        with open('db_create.sql', 'r') as db_file:
            sql = ''.join(db_file.readlines())
            conn = DatabaseManager.get_connection(sgbd_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()
            conn.commit()
            conn.close()
