
from collections import Counter
import pandas as pd
import os

def list_files(root,folder):

    files = list()

    full_path = os.path.join(root,'data',folder)
    for file in os.listdir(full_path):
        files.append(file)

    return files


def new_files(root):

    file_raw = list_files(root,'raw')
    file_staging = list_files(root,'staging')
    not_in_staging = list((Counter(file_raw) - Counter(file_staging)).elements())

    return not_in_staging


def read_files(root, name_file_list):

    dfs = dict()
    errors = []

    for file in name_file_list:

        path = os.path.join(root,'data/raw',file)

        try:
            df = pd.read_csv(path)
            dfs[file] = df

        except Exception as e:
            #print(f"Erro ao ler {file}: {e}")
            errors.append(file)

    return dfs, errors


def extract(root):

    files = new_files(root)

    dfs,errors = read_files(root,files)
    return dfs,errors
