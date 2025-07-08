# llm/knowledge_base/build_kb.py
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
# Define paths
DOCS_DIR = "llm/knowledge_base/docs"
DB_DIR = "llm/knowledge_base/db"

print("Starting knowledge base creation...")

# 1. Load Documents
documents = []
for file in os.listdir(DOCS_DIR):
    if file.endswith(".txt"):
        loader = TextLoader(os.path.join(DOCS_DIR, file), encoding='utf-8')
        documents.extend(loader.load())

if not documents:
    print("No documents found. Please add documentation to the 'llm/knowledge_base/docs' directory.")
    exit()

print(f"Loaded {len(documents)} document(s).")

# 2. Chunk Documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunked_docs = text_splitter.split_documents(documents)
print(f"Split documents into {len(chunked_docs)} chunks.")

# 3. Create Embeddings
# Using a local, lightweight embedding model.
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
print("Embedding model loaded.")

# 4. Store in ChromaDB
# This will create the DB directory if it doesn't exist and save the embeddings.
# It's persistent, so you only need to run this once or when docs change.
vectorstore = Chroma.from_documents(
    documents=chunked_docs,
    embedding=embedding_function,
    persist_directory=DB_DIR
)

print("\n---------------------------------")
print("✅ Knowledge base created successfully!")
print(f"Vector store persisted at: {DB_DIR}")
print("---------------------------------")