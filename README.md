# 📊 Sales ETL Pipeline

Projeto de Engenharia de Dados desenvolvido para praticar a construção de um pipeline ETL completo utilizando **Python, Pandas, MySQL e Streamlit**.

O projeto simula um cenário de vendas em que dados provenientes de arquivos CSV passam por processos de **extração, transformação e carregamento (ETL)** até serem disponibilizados em um banco de dados MySQL e apresentados em um dashboard interativo.

## 🌐 Projeto Online

🚀 **Dashboard:** [salespipeline2026.streamlit.app](https://salespipeline2026.streamlit.app/)  
☁️ **Banco de dados:** MySQL hospedado em ambiente cloud ([Aiven](https://aiven.io/)).

O dashboard e o banco de dados estão disponíveis online, permitindo que a aplicação seja acessada sem depender do ambiente local.

---

## 🚀 Arquitetura

```text
               Arquivos CSV
                    │
                    ▼
                 EXTRACT
                    │
                    ▼
                TRANSFORM
                    │
                    ▼
                  LOAD
                    │
                    ▼
                 MySQL ☁️
                    │
                    ▼
           Streamlit Cloud ☁️
                    │
                    ▼
                Dashboard
```

# 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Manipulação de Dados:** Pandas
* **Banco de Dados:** MySQL / MySQL Connector
* **Visualização & Dashboard:** Streamlit, Plotly
* **Controle de Versão:** Git / GitHub

# 🔄 ETL

## 1. Extract

A etapa de extração é responsável por identificar e carregar os arquivos disponíveis na pasta `raw/`.

### O processo:

* Verifica os arquivos existentes;
* Identifica arquivos novos;
* Compara os arquivos entre `raw/` e `staging/`;
* Realiza a leitura dos CSVs utilizando Pandas;
* Identifica arquivos que não puderam ser lidos;
* Retorna os DataFrames para a etapa de transformação.

Os DataFrames são armazenados em um dicionário para facilitar o processamento:

{
    "clientes.csv": DataFrame,
    "produtos.csv": DataFrame,
    "vendas.csv": DataFrame
}

## 2. Transform

A etapa de transformação realiza a limpeza e padronização dos dados.

### Tratamentos implementados:

* Padronização dos nomes das colunas;
* Tratamento de valores nulos;
* Remoção de registros duplicados;
* Padronização de strings (remoção de espaços extras, caixa baixa/alta);
* Conversão de tipos de dados;
* Validação e padronização de datas;
* Tratamento de valores inválidos ou inconsistentes;
* Aplicação de regras de negócio específicas para clientes, produtos e vendas.

As transformações são divididas entre funções genéricas e funções específicas para cada conjunto de dados.

---

## 3. Load

Após o tratamento, os dados são carregados no banco de dados MySQL.

O banco utiliza uma modelagem dimensional baseada em **Star Schema**, otimizada para consultas analíticas sobre os dados de vendas.

# 🗄️ Modelagem do Banco (Star Schema)

                    ┌─────────────────┐
                    │  dim_clientes   │
                    ├─────────────────┤
                    │ id_cliente      │
                    │ nome_cliente    │
                    │ cidade          │
                    │ estado          │
                    └────────┬────────┘
                             │
                             │
                        ┌────▼───────┐
                        │ fato_vendas│
                        ├────────────┤
                        │ id_venda   │
                        │ id_cliente │
                        │ id_produto │
                        │ data       │
                        │ quantidade │
                        │ valor_unit │
                        │ valor_total│
                        └────┬───────┘
                             │
                             │
                    ┌────────▼────────┐
                    │  dim_produtos   │
                    ├─────────────────┤
                    │ id_produto      │
                    │ nome_produto    │
                    │ categoria       │
                    │ marca           │
                    └─────────────────┘

## 🗄️ Modelagem de Dados

### Tabelas

* **`dim_clientes`:** `id_cliente`, `nome_cliente`, `cidade`, `estado`
* **`dim_produtos`:** `id_produto`, `nome_produto`, `categoria`, `marca`
* **`fato_vendas`:** `id_venda`, `id_cliente`, `id_produto`, `data`, `quantidade`, `valor_unitario`, `valor_total`

### Relacionamentos (Chaves Estrangeiras)

* `fato_vendas.id_cliente` ➔ `dim_clientes.id_cliente`
* `fato_vendas.id_produto` ➔ `dim_produtos.id_produto`

---

## 📈 Dashboard

O dashboard foi desenvolvido utilizando **Streamlit** e **Plotly**, realizando consultas diretamente no banco de dados MySQL.

### Principais Indicadores e Visualizações:

* 💰 **Faturamento total**
* 🛒 **Quantidade de vendas**
* 📦 **Produtos vendidos**
* 👥 **Total de clientes**
* 📈 **Evolução do faturamento**
* 🏷️ **Faturamento por categoria**
* 🥇 **Produtos mais vendidos**
* 🌎 **Vendas por estado**

O dashboard conta com filtros dinâmicos para facilitar a análise interativa dos dados.

---

## 🧪 Tratamento de Inconsistências

Os arquivos brutos do projeto contêm inconsistências propositais para simular cenários reais de engenharia de dados, tais como:

* **Formatos de data distintos:** `05/01/2026`, `2026/01/06`, `07-01-2026`, `2026-01-08`
* **Formatos monetários variados:** `150`, `150,00`, `R$ 800`
* **Inconsistências gerais:** Valores nulos, duplicidades, espaços extras e IDs inválidos.

Todas essas inconsistências são tratadas programmaticamente na fase de **Transform**.

---

## ⚙️ Instalação e Execução Local

1. **Clone o repositório:**

```bash
git clone https://github.com/SEU-USUARIO/sales-etl-pipeline.git
cd sales-etl-pipeline
```

2. **Crie e ative o ambiente virtual:**

* **Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

* **Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configuração de Variáveis de Ambiente:**

Crie um arquivo `.env` na raiz do projeto (com base no `.env.example`) e insira suas credenciais:

```env
DB_HOST=seu_host
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_DATABASE=seu_banco
```

5. **Execução:**

* **Rodar o pipeline ETL:**
```bash
python src/pipeline.py
```

* **Rodar o Dashboard Streamlit:**
```bash
streamlit run dashboard/app.py
```

## ☁️ Deploy

A arquitetura em nuvem é estruturada da seguinte forma:

```plaintext
MySQL Cloud (Aiven) ◄─── Streamlit Cloud ◄─── GitHub
```

O dashboard em nuvem se conecta com o MySQL hospedado via **Secrets Management** do Streamlit Cloud.

---

## 🎯 Objetivos do Projeto

Este projeto abrange os seguintes conceitos essenciais da Engenharia de Dados:

* Arquitetura e construção de pipelines ETL
* Manipulação e limpeza de dados com Pandas
* Modelagem Dimensional (Star Schema)
* Integração Python com bancos relacionais (MySQL)
* Consultas analíticas em SQL
* Visualização de dados interativa
* Gestão de variáveis de ambiente e Deploy em Nuvem

---

## 👨‍💻 Autor

**João Victor**  
Estudante de Ciência da Computação com foco em Engenharia de Dados.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joaobatista7/)
