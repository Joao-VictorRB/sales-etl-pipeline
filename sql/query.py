import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.connect.connection import con, closeDB
import pandas as pd

#----   BARRA LATERAL -------

def get_date_min_max(temp):
    connection = con()
    if connection is None or not connection.is_connected():
        raise RuntimeError("Falha ao conectar ao banco de dados")

    cur = connection.cursor()
    try:
        if temp == 'min':
            cur.execute("SELECT min(data) FROM fato_vendas;")
        else:
            cur.execute("SELECT max(data) FROM fato_vendas;")

        return cur.fetchone()[0]
    finally:
        closeDB(connection, cur)


def get_states():
    connection = con()
    if connection is None or not connection.is_connected():
        raise RuntimeError("Falha ao conectar ao banco de dados")

    cur = connection.cursor()
    try:
        cur.execute("SELECT DISTINCT estado FROM dim_clientes ORDER BY estado;")
        results = cur.fetchall()
        return [x[0] for x in results]
    finally:
        closeDB(connection, cur)


def get_category():
    connection = con()
    if connection is None or not connection.is_connected():
        raise RuntimeError("Falha ao conectar ao banco de dados")

    cur = connection.cursor()
    try:
        cur.execute("SELECT DISTINCT categoria FROM dim_produtos ORDER BY categoria;")
        results = cur.fetchall()
        return [x[0] for x in results]
    finally:
        closeDB(connection, cur)


def get_mark():
    connection = con()
    if connection is None or not connection.is_connected():
        raise RuntimeError("Falha ao conectar ao banco de dados")

    cur = connection.cursor()
    try:
        cur.execute("SELECT DISTINCT marca FROM dim_produtos ORDER BY marca;")
        results = cur.fetchall()
        return [x[0] for x in results]
    finally:
        closeDB(connection, cur)


def query_filtro(date,state,category,mark):

    connection = con()
    if connection is None or not connection.is_connected():
        raise RuntimeError("Falha ao conectar ao banco de dados")


    query = "SELECT * FROM v_sales_etl_pipiline WHERE 1 = 1 "
    params = []

    if len(date) == 1:

        dt_inicio = date[0].strftime("%Y-%m-%d")
        query += "AND data = %s "
        params.append(dt_inicio)

    elif len(date) == 2:

        dt_inicio = date[0].strftime("%Y-%m-%d")
        dt_fim = date[1].strftime("%Y-%m-%d")

        query += "AND data BETWEEN %s AND %s "

        params.append(dt_inicio)
        params.append(dt_fim)

    if state != 'Todos':
        query += "AND estado = %s "
        params.append(state)

    if category != 'Todos':
        query += "AND categoria = %s "
        params.append(category)

    if mark != 'Todos':
        query += "AND marca = %s "
        params.append(mark)

    cur = connection.cursor()
    try:
        cur.execute(query,params)

        results = cur.fetchall()
        columns = cur.column_names

        return pd.DataFrame(results,columns=columns)
    finally:
        closeDB(connection, cur)











