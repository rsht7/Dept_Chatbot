
import os
from langchain_community.vectorstores import FAISS  
from langchain_openai import OpenAIEmbeddings        
from langchain.docstore.document import Document
from dotenv import load_dotenv


# Load API keys from .env file
load_dotenv()

# Initialize the OpenAI embedding model
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

# Path to your .txt files
txt_files = [
    "data/faculty_info_paragraphs.txt",
    "data/courses_data.txt",
    "data/about_dept.txt"
]

# This list will hold all the extracted documents (full paragraphs)
all_documents = []

# Load and split each .txt
for txt_path in txt_files:
    print(f"📄 Loading: {txt_path}")
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Split into paragraphs based on double newline
    paragraphs = text.strip().split('\n\n')
    
    for para in paragraphs:
        if para.strip():  # Skip empty paragraphs
            doc = Document(page_content=para.strip())
            all_documents.append(doc)

print(f"📚 Total documents loaded: {len(all_documents)}")

# NO need to split into smaller chunks since paragraph lengths are already small and manageable

#  Generate vector embeddings and store in FAISS
print("🔍 Creating FAISS vector store with OpenAI embeddings...")
vectorstore = FAISS.from_documents(all_documents, embeddings)

# Save FAISS index locally
vectorstore.save_local("faiss_index")
print("✅ FAISS index saved successfully at './faiss_index/'")
