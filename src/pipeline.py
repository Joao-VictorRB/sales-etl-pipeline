import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pathlib import Path
from src.extract import extract
from src.transform import transform
from src.load import load
from src.connect.connection import con, closeDB

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
