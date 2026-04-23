from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os

# Load model via Ollama
llm = Ollama(model="llama3")
print ("llm=", llm)

# Embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print ("embeddings=", embeddings)

DB_DIR = "db"

def load_docs():
    print ("load_docs")
    docs = []
    for file in os.listdir("cobol_docs"):
        if file.endswith(".cbl") or file.endswith(".txt"):
            loader = TextLoader(os.path.join("cobol_docs", file))
            docs.extend(loader.load())
    return docs

def create_db():
    print ("create_db")
    docs = load_docs()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunks = splitter.split_documents(docs)

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_DIR
    )
    
    db.persist()
    return db

def get_db():
    print ("get_db")
    if not os.path.exists(DB_DIR):
        return create_db()
    return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

def answer(query):
    print ("answer=", answer)
    db = get_db()
    retriever = db.as_retriever(search_kwargs={"k": 3})

    docs = retriever.get_relevant_documents(query)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a COBOL expert.

Use the context below to answer the question.

Context:
{context}

Question:
{query}
"""

    return llm.invoke(prompt)