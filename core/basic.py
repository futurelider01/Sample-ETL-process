from core.functions import *
import time
# import all necessary funtions

@timer_info
def ingest_files(source_folder_or_specific_files: str|list, chunk_size: int = None):
    """Main ingest function.
    Ingest every csv files in source folder
    : source_folder - str if you want to give a source folder
    : source_folder - list if you want to specify certain files
    : chunk_size - int get certain row from file if file is larger than 5MB
    """
    
    if isinstance(source_folder_or_specific_files, str):
        # get all csv files
        csv_files = [file for file in os.listdir(source_folder_or_specific_files) if file.endswith('.csv')]
    elif isinstance(source_folder_or_specific_files, list):
        csv_files = source_folder_or_specific_files
    
    for file in csv_files:
        # generate file_path
        file_path = os.path.join(source_folder_or_specific_files, file)
        
        #check size
        if size(file_path)>5: # in MB
            # It is large file
            chunk_ingest(file_path, chunk_size=chunk_size if chunk_size is not None else 200)
        else:
            # It is small file
            just_ingest(file_path)
