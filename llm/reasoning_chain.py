# llm/reasoning_chain.py
import os
from llama_cpp import Llama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from llm.prompts import SYSTEM_PROMPT

# --- 1. CONFIGURATION ---
MODEL_PATH = os.path.join("models", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")
DB_DIR = "llm/knowledge_base/db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- 2. INITIALIZE COMPONENTS ---

# Load LLM
print("Loading LLM model...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=-1,
    verbose=False
)

# Load RAG retriever
print("Loading RAG knowledge base...")
embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embedding_function)
retriever = vectorstore.as_retriever(search_kwargs={'k': 3}) # Retrieve top 3 most relevant chunks

print("✅ Initialization complete.")

# --- 3. REASONING FUNCTION ---
def generate_workflow(user_query: str, data_manifest: dict):
    """
    Generates a geospatial workflow using RAG and CoT.
    
    Args:
        user_query (str): The user's natural language request.
        data_manifest (dict): A dictionary mapping data names to file paths.
                                e.g., {'rivers': 'data/input/rivers.shp'}
    """
    print(f"\n>> Received Query: {user_query}")

    # 1. RAG: Retrieve relevant tool documentation
    retrieved_docs = retriever.get_relevant_documents(user_query)
    rag_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    print(f"\n>> Retrieved Context:\n{rag_context}")

    # 2. Create data context string
    data_context_str = "\n".join([f"- {name}: {path}" for name, path in data_manifest.items()])

    # 3. Format the prompt
    formatted_prompt = SYSTEM_PROMPT.format(
        user_query=user_query,
        rag_context=rag_context,
        data_context=data_context_str
    )

    # Add Mistral instruction format
    final_prompt = f"<s>[INST] {formatted_prompt} [/INST]"
    
    # 4. LLM: Generate the response
    print("\n>> Generating workflow with LLM...")
    output = llm(
        final_prompt,
        max_tokens=1024,
        stop=["</s>"],
        echo=False
    )
    
    response_text = output['choices'][0]['text']
    return response_text

# --- 4. EXAMPLE USAGE ---
if __name__ == '__main__':
    # This is a test run to see if the chain works.
    test_query = "Find all areas within 500 meters of the main rivers."
    
    # In the real app, this will come from the user's uploads.
    test_data_manifest = {
        'rivers': 'data/input/rivers.shp',
        'land_use': 'data/input/land_use.tif'
    }

    generated_text = generate_workflow(test_query, test_data_manifest)
    
    print("\n--- LLM FULL RESPONSE ---")
    print(generated_text)
    print("------------------------")