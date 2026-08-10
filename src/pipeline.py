from pathlib import Path
from extract import extract
from transform import transform
from load import load
from connect.connection import con, closeDB

try:
    path_root = Path(__file__).resolve().parent.parent
except NameError:
    path_root = Path.cwd()

def pipeline():

    conn = con()

    try:
        
        dfs,errors = extract(path_root)
        dfs = transform(dfs)
        load(dfs, conn)

    finally:
        closeDB(conn)
        print('Finalized ETL')


if __name__ == "__main__":
    pipeline()
