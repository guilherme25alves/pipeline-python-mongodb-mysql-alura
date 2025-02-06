# EXEMPLO CARREGANDO VARIÁVEIS DE AMBIENTE DO ARQUIVO .ENV
# import os
# from dotenv import load_dotenv
# import mysql
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests

# # Carraga as variáveis de ambiente do arquivo .env no ambiente de trabalho
# load_dotenv()

# # Exemplo de utilização
# host = os.getenv("DB_HOST")
# user = os.getenv("DB_USERNAME")
# password = os.getenv("DB_PASSWORD")

# cnx = mysql.connector.connect(host=host, user=user, password=password)

# print(cnx)


def connect_mongo(uri):
    client = MongoClient(uri, server_api=ServerApi("1"))

    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client


def create_connect_db(client, db_name):
    db = client[db_name]
    print(f'Connected to the "{db_name}" database')
    return db


def create_connect_collection(db, collection_name):
    collection = db[collection_name]
    print(f'Connected to the "{collection_name}" collection')
    return collection


def extract_api_data(url):
    return requests.get(url).json()


def insert_data(col, data):
    result = col.insert_many(data)
    numero_docs_inseridos = len(result.inserted_ids)
    return numero_docs_inseridos


if __name__ == "__main__":
    client = connect_mongo(
        "mongodb+srv://admin:admin@cluster-alura-pipeline.qp97c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-alura-pipeline"
    )
    db = create_connect_db(client, "db_produtos_desafio")
    col = create_connect_collection(db, "produtos")

    data = extract_api_data("https://labdados.com/produtos")
    print(f"\nQuantidade de dados extraídos: {len(data)}")

    numero_documentos_inseridos = insert_data(col, data)
    print(f"\nQuantidade de documentos inseridos: {numero_documentos_inseridos}")

    client.close()
    print("\nConexão fechada.")
