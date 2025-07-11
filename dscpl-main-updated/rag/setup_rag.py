
from fetch_posts import fetch_socialverse_posts
from vector_store import create_vector_store

# Step 1: Fetch the posts from API
fetch_socialverse_posts()

# Step 2: Create FAISS vector store
create_vector_store()

print("✅ RAG setup complete.")
