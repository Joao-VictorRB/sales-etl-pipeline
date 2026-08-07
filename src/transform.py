import pandas as pd

def standardize_columns(df):

    df.columns = df.columns.str.replace(' ', '_').str.lower()
    return df
    

def treat_nulls(df):

    df = df.dropna(how='all',axis = 0)
    df = df.dropna(how='all',axis = 1)

    return df


def remove_duplicates(df):

    df = df.drop_duplicates()
    return df
     

def transform_clientes(df):

    df = standardize_columns(df)
    df = treat_nulls(df)
    df = remove_duplicates(df)

    if all(col in df.columns for col in ['nome', 'cidade', 'estado']):

        df = df.dropna(subset=['nome', 'cidade', 'estado'])

        df_columns = ['nome','cidade','estado']

        for col in df_columns:
            if col != 'estado':
                df[col] = df[col].str.title().str.strip()
            else:
                df[col] = df[col].str.upper().str.strip()

    return df


def transform_produtos(df):

    df = standardize_columns(df)
    df = treat_nulls(df)
    df = remove_duplicates(df)

    if all(col in df.columns for col in ['nome_produto', 'categoria', 'marca']):

        df = df.dropna(subset=['nome_produto', 'categoria', 'marca'])

        df_columns = ['nome_produto','categoria','marca']

        for col in df_columns:
            df[col] = df[col].str.title().str.strip()

    return df


def transform_vendas(df):

    df = standardize_columns(df)
    df = treat_nulls(df)
    df = remove_duplicates(df)

    #Date

    if 'data' in df.columns:

        today = pd.Timestamp.today()
        
        df['data'] = pd.to_datetime(df['data'], errors='coerce')

        if pd.api.types.is_datetime64_any_dtype(df['data']):

            df = df.dropna(subset=['data'])
            df = df[
                (df['data'] >= "2000-01-01") &
                (df['data'] <= today)
            ]

    #Qtd

    types = {
            'quantidade': int, 
            'valor_unitario': float
        }
    

    for col,dtype in types.items():

        if col in df.columns:

            df[col] = df[col].fillna(0)

            avg =  df.loc[df[col] >= 0, col].mean()
            df.loc[df[col] < 0, col] = avg

            df[col] = df[col].astype(dtype)

    df["valor_total"] = df["valor_unitario"] * df["quantidade"]

    return df
        


def transform(dfs):

    for name_file, df in dfs.items():

        if name_file == 'clientes.csv':
            dfs[name_file] =  transform_clientes(df)
        elif name_file == 'produtos.csv':
            dfs[name_file] = transform_produtos(df)
        elif name_file == 'vendas.csv':
            dfs[name_file] = transform_vendas(df)
        else:
            pass

    return dfs

    