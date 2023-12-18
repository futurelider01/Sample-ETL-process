from core import config
import os, pandas as pd, time
from sqlalchemy import create_engine, inspect
from datetime import datetime

connection_string = f"mssql+pyodbc://{config.USERNAME}:{config.PASSWORD}@{config.SERVER}/{config.DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(connection_string)

# Check if the table exists in SQL Server
inspector = inspect(engine)
all_tables = inspector.get_table_names()

# log func for logging in case of errors and loadings
def logging(tableName,status='Fail',row_count=0,error_text='No',date=datetime.now()):
    """Logs any action with ETL process when it is called"""
    row = ','.join([tableName,status,str(row_count),error_text,str(date)])+'\n'
    with open('logs.csv','a') as f:
        f.write(row)

# ingesting small files 
def just_ingest(file_path):
    """"
    Ingests given path to sql server at once
    :file_path - str
    """
    table_name = os.path.splitext(os.path.basename(file_path))[0]
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
            
    if table_name in all_tables:
        # Table exists, check for column mismatch
        if not chech_columns_eq(table_name, df.columns):
            # Columns mismath error
            text=f"Column mismatch in table {table_name}."
            logging(table_name, error_text=text)
            return
        
    # Insert into table, append data
    print(f"Loading file {os.path.basename(file_path)} to table {table_name}...")
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print(f"Successfully LOADED {len(df)} rows.\nDone\n")
    # log it
    logging(table_name, "Success", len(df))             
    
    

# ingesting big files
def chunk_ingest(file_path, chunk_size=200):
    """"
    Ingests given path to sql server with given chunk size
    : file_path - str
    : chunk_size - int (default 200)
    """
    # getting base name of file as tbl name
    table_name = os.path.splitext(os.path.basename(file_path))[0]
    # getting columns of csv
    df = list(pd.read_csv(file_path, chunksize=chunk_size))
    df_cols = df[0].columns
    rows = len(df)
    # checking whether exists in sql server
    if table_name in all_tables:
        # Table exists, check for column mismatch
        if not chech_columns_eq(table_name, df_cols):
            # Columns mismath error
            text=f"Column mismatch in table {table_name}."
            logging(table_name, error_text=text)
            return # Don't need to iterate again if columns mismatch
    rows=0            
    for chunk in df: # gets default every 200 rows
        rows+=len(chunk)
        print(f"Loading file {os.path.basename(file_path)} to table {table_name}...")
        chunk.to_sql(table_name, engine, index=False, if_exists='append')
        print(f"Successfully LOADED {len(chunk)} rows.\n\n")
    print(f"Successfully LOADED file {os.path.basename(file_path)} to table {table_name}\n"\
          f"Transferred {rows} rows.\nDone\n")
            
    # log it
    logging(table_name,'Success',rows) 
        
            


def chech_columns_eq(table_name, df_columns):
    """"Returns True if all columns of dataFram exists in table
         Otherwise False"""
    sql_columns = [column['name'] for column in inspector.get_columns(table_name)]
    if not all(column in sql_columns for column in df_columns):
        return False
    return True

def size(file_path):

    mb_size = os.path.getsize(file_path)//1024**2 # MB
    return mb_size


def timer_info(func):
    def wrapper(*args, **kwargs):
        print(f"\n\nFunction \"{func.__name__}\" started...\n\n".center(50))
    
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function \"{func.__name__}\" took {elapsed_time:.4f} seconds to run.\n\n\n")
        
        return result
    
    return wrapper
