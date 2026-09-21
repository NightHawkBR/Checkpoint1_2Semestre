"""Configuracao e helpers de conexao compartilhados pelos exercicios do CP1.

Centraliza aqui a conexao para que cada exercicio trate erro de conexao
sem repetir codigo (criterio de correcao: "tratamento de erros de conexao").

As credenciais podem ser sobrescritas por variaveis de ambiente, ex.:
    $env:MYSQL_PASSWORD = "senha123"   # PowerShell
"""

import os
import sys

import mysql.connector
from mysql.connector import Error as MySQLError
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# ---------------------------------------------------------------- MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "cp1_seguranca")

# ------------------------------------------------------------------ MySQL
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
}
MYSQL_DB = os.getenv("MYSQL_DB", "cp1_seguranca")


def get_mongo_db():
    """Devolve o database do MongoDB, encerrando com mensagem clara se cair."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")  # forca a conexao agora, nao na 1a query
        return client[MONGO_DB]
    except PyMongoError as erro:
        sys.exit(f"[ERRO] Falha ao conectar no MongoDB ({MONGO_URI}): {erro}")


def get_mysql_connection():
    """Devolve uma conexao MySQL, criando o database do CP se ainda nao existir."""
    try:
        servidor = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = servidor.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
        cursor.close()
        servidor.close()
        return mysql.connector.connect(database=MYSQL_DB, **MYSQL_CONFIG)
    except MySQLError as erro:
        alvo = f"{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}"
        sys.exit(f"[ERRO] Falha ao conectar no MySQL ({alvo}): {erro}")


def titulo(texto):
    """Cabecalho padrao para a saida dos exercicios."""
    print("=" * 60)
    print(texto)
    print("=" * 60)
