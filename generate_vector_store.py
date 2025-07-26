from src.components.data_prepocessing import ProcessData
from src.components.vector_database import Vector
from src.utils.helper import save_data



pre_process = ProcessData()
vector_process = Vector()

# raw data extract
raw_data = pre_process.extract_raw_data()
save_data(raw_data)


# Normalize text
normalized_text = pre_process.normalize_text(raw_data)

# make document object
documents = pre_process.convert_document_object(normalized_text)

# Generate chunks
documents_chunks = pre_process.convert_into_chunk(documents)

# load embedding model
embedding_model = vector_process.load_embedding_model()

# create vector store database and save locally
vector_process.create_vector_store(
    chunks=documents_chunks,
    embedding_model=embedding_model
)



