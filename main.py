from core import config
from core.basic import ingest_files

# Source folder from config file
source_folder = config.SOURCE_FOLDER

# Calling main ingest function
# source_folder=['source/people', 'source/organizations']
ingest_files(source_folder, chunk_size=50000)
