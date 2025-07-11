from langchain_huggingface import HuggingFaceEmbeddings  # ✅ Updated to use new package
from langchain_community.vectorstores import FAISS

def get_rag_context(query):
    index_path = "rag/faiss_index"

    # Use modern HuggingFaceEmbeddings (no deprecation warning)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Load the FAISS vector store
    vector_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    # Create a retriever and use .invoke() instead of deprecated get_relevant_documents()
    retriever = vector_db.as_retriever()
    docs = retriever.invoke(query)

    # Join the page contents into a context block
    context = "\n\n".join([doc.page_content for doc in docs])
    return context
