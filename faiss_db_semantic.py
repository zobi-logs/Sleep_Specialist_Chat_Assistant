from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load your original source
with open("combined_books.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Simulate semantic chunking with sentence-like chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.create_documents([text])

# Create and save the FAISS DB
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_db_semantic")

print("✅ Semantic FAISS DB created and saved as 'faiss_db_semantic'")