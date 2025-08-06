from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Load text
with open("combined_books.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split text into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.create_documents([text])

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS vector database
faiss_db = FAISS.from_documents(docs, embeddings)

# Save FAISS DB locally
faiss_db.save_local("faiss_db")

print("✅ FAISS vector database created and saved as 'faiss_db'.")