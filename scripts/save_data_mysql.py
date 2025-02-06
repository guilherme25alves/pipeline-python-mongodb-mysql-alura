import mysql.connector
import pandas as pd


def connect_mysql(host_name, user_name, pw):
    cnx = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=pw,
    )
    print(cnx)
    return cnx


def create_cursor(cnx):
    return cnx.cursor()


def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    print(f"\nBase de dados {db_name} criada")


def show_databases(cursor):
    cursor.execute("SHOW DATABASES;")
    for db in cursor:
        print(db)


def create_product_table(cursor, db_name, tb_name):
    cursor.execute(f""" 
        CREATE TABLE IF NOT EXISTS {db_name}.{tb_name} (
            id VARCHAR(100),
            Produto VARCHAR(100),
            Categoria_Produto VARCHAR(100),
            Preco FLOAT(10,2),
            Frete FLOAT(10,2),
            Data_Compra DATE,
            Vendedor VARCHAR(100),
            Local_Compra VARCHAR(100),
            Avaliacao_Compra INT,
            Tipo_Pagamento VARCHAR(100),
            Qntd_Parcelas INT,
            Latitude FLOAT(10,2),
            Longitude FLOAT(10,2),
            
            PRIMARY KEY (id)
        );               
    """)
    print(f"\nTabela {tb_name} criada")


def show_tables(cursor, db_name):
    cursor.execute(f"USE {db_name};")
    cursor.execute("SHOW TABLES;")
    for table in cursor:
        print(table)


def read_csv(path):
    return pd.read_csv(path)


def add_product_data(cnx, cursor, df, db_name, tb_name):
    lista_dados = [tuple(row) for _, row in df.iterrows()]
    sql = f"INSERT INTO {db_name}.{tb_name} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.executemany(sql, lista_dados)
    print(cursor.rowcount, "registros inseridos")
    cnx.commit()


if __name__ == "__main__":
    # realizando a conexão com mysql
    cnx = connect_mysql("localhost", "millenagena", "12345")
    cursor = create_cursor(cnx)

    # criando a base de dados
    create_database(cursor, "db_produtos_teste")
    show_databases(cursor)

    # criando tabela
    create_product_table(cursor, "db_produtos_teste", "tb_livros")
    show_tables(cursor, "db_produtos_teste")

    # lendo e adicionando os dados
    df = read_csv("../data_teste/tbl_livros.csv")
    add_product_data(cnx, cursor, df, "db_produtos_teste", "tb_livros")
