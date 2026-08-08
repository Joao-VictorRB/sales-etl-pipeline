def load_clientes(dataframe,cur):

    query = """ INSERT INTO 
                    dim_clientes (idCliente, nomeCliente, cidade, estado) 
                VALUES (%s, %s, %s, %s) 
            """ 

    for row in dataframe.itertuples(index=False):
        cur.execute(query,row)
    
    
def load_produtos(dataframe,cur):

    query = """ INSERT INTO 
                    dim_produtos (idProduto, nomeProduto, categoria, marca) 
                VALUES (%s, %s, %s, %s) 
            """ 

    for row in dataframe.itertuples(index=False):
        cur.execute(query,row)


def load_vendas(dataframe,cur):
    
    query = """ INSERT INTO 
                    fato_vendas (idVenda, data, id_Cliente, id_Produto, quantidade, valor_unitario, valor_total) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
            """ 

    for row in dataframe.itertuples(index=False):
        cur.execute(query,row)


def load (dfs, con):

    cur = con.cursor()

    try:

        load_clientes(dfs['clientes.csv'],cur)
        load_produtos(dfs['produtos.csv'],cur)
        load_vendas(dfs['vendas.csv'],cur)
        con.commit() 

    except:
        con.rollback()
        raise
