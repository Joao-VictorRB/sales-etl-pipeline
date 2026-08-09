from src.connect.connection import con, closeDB

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

cur.execute(""" 
    CREATE VIEW IF NOT EXISTS v_sales_etl_pipiline AS
       SELECT
            f_v.idVenda,d_c.idCliente,d_p.idProduto,
            d_c.nomeCliente,d_c.cidade,d_c.estado,
            d_p.nomeProduto,d_p.categoria,d_p.marca,
            f_v.data,f_v.quantidade,f_v.valor_unitario,f_v.valor_total
        FROM fato_vendas AS f_v
        INNER JOIN dim_clientes AS d_c
            ON f_v.id_Cliente = d_c.idCliente
        INNER JOIN dim_produtos AS d_p
            ON f_v.id_Produto = d_p.idProduto;
 """)

closeDB(con,cur)
