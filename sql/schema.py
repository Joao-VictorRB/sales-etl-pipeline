from connect.connection import con, closeDB

con = con()
cur =  con.cursor()

cur.execute(""" 
    CREATE TABLE IF NOT EXISTS dim_clientes(
        idCliente INT PRIMARY KEY,
        nomeCliente VARCHAR(255) NOT NULL,
        cidade VARCHAR(50) NOT NULL,
        estado CHAR(2) NOT NULL
    );
 """)

cur.execute(""" 
    CREATE TABLE IF NOT EXISTS dim_produtos(
        idProduto INT PRIMARY KEY,
        nomeProduto VARCHAR(100) NOT NULL,
        categoria VARCHAR(100) NOT NULL,
        marca VARCHAR(100) NOT NULL
    );
 """)

cur.execute(""" 
    CREATE TABLE IF NOT EXISTS fato_vendas(
        idVenda INT PRIMARY KEY,
        id_Cliente INT NOT NULL,
        id_Produto INT NOT NULL,
        data DATE NOT NULL,
        quantidade INT NOT NULL,
        valor_unitario DECIMAL(10,2) NOT NULL,
        valor_total DECIMAL(10,2) NOT NULL,

        FOREIGN KEY (id_Cliente) REFERENCES dim_clientes(idCliente),
        FOREIGN KEY (id_Produto) REFERENCES dim_produtos(idProdutos)
    );
 """)

closeDB(con,cur)
