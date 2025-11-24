import os
import sys
from dotenv import load_dotenv
import re 
import json 

# --- LangChain Imports (Modularized) ---
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

# Define common paths
current_dir = os.path.dirname(os.path.abspath(__file__))
book_dir = os.path.join(current_dir, "books")
persistent_dir = os.path.join(current_dir, "db", "epa_chroma_db")

# Define fixed instructions/templates
LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/text-embedding-004"
SCORE_THRESHOLD = 0.1 # Using a lower threshold for better retrieval success

# The query is general and topic-focused for retrieval
TOPIC_QUERY = "Key information about the provided source document content."

# The instruction tells the LLM the final format (Note: JSON braces are escaped for the prompt)
QUESTION_GENERATION_TEMPLATE = """
Generate 12 multiple-choice questions based ONLY on the provided context related to the topic of the source document. Adhere strictly to the specified JSON schema.

The JSON must adhere strictly to this format:
[
  {{{{
    "question": "the question based on the context", 
    "options": ["choice 1", "choice 2", "choice 3", "choice 4"], 
    "answer": 0 
  }}}}
]
The 'answer' index (0-3) must be the correct option in the list. Do not include any text outside the JSON block.

CONTEXT:
{context}
"""
PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert curriculum developer that creates strict, challenging multiple-choice questions based on provided text, adhering to the specified JSON schema. Output ONLY the JSON."),
    ("user", QUESTION_GENERATION_TEMPLATE),
])

# --- 1. Database Initialization Function (Unchanged) ---
def initialize_vector_store():
    """Initializes the Chroma vector store if it does not exist."""
    print("persistent directory does not exist. Initializing the vector store...")
    
    if not os.path.exists(book_dir): 
        raise FileNotFoundError(f"The path to {book_dir} does not exist, please add the right path.")
    
    book_files = [book for book in os.listdir(book_dir) if book.endswith(".txt")]
    documents = []
    for book in book_files:
        file_path = os.path.join(book_dir, book)
        loader = TextLoader(file_path, encoding="utf-8")
        book_doc = loader.load()
        for doc in book_doc: 
            doc.metadata = {"source" : book} 
            documents.append(doc)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(f"\n----------------Document Chunk Information-------------------\nNumber of document chunks is {len(docs)}")

    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=API_KEY)
    
    print("\n--------------Creating persistent vector store--------------------")
    db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_dir)
    print("---------------Finished Creating Vector Database-------------------\n")
    return db

def clean_llm_output(text):
    # Remove docstrings
    text = re.sub(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')', "", text)
    # Remove code fences
    text = text.replace("```json", "").replace("```", "")
    return text.strip()

def save_json_responses(responses, title):
    # Split only if a dot exists
    base = title.split(".")[0] if "." in title else title
    
    filename = f"{base}.json"
    with open(filename, "w") as file:
        file.write(responses)

# --- 2. Main RAG Logic (Accepts Dynamic Input) ---
def run_rag_chain(source_file_name: str, final_llm_instruction: str):
    """
    Loads the database and runs the RAG chain for a specific source file.
    :param source_file_name: The name of the document to filter by (e.g., 'Event Layout and Equipment Management.txt').
    :param final_llm_instruction: The instruction to pass to the LLM (e.g., 'Generate 12 questions').
    """
    # --- Check/Initialize the DB ---
    if not os.path.exists(persistent_dir): 
        db = initialize_vector_store()
    else: 
        print("Vector store already exists, loading from persistent storage.")
        embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=API_KEY)
        db = Chroma(persist_directory=persistent_dir, embedding_function=embeddings)
        print("---------------Finished Loading Vector Database-------------------\n")

    # --- Setup Retriever (Dynamically Filtered) ---
    print(f"Setting up retriever filter for: {source_file_name}")
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",    
        search_kwargs={
            "k": 10, 
            "score_threshold": SCORE_THRESHOLD,  
            "filter": {
                "source": source_file_name
            }
        }
    )

    # --- Setup LLM and Chain ---
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=API_KEY)

    # 1. Retrieval Step: Pass the TOPIC_QUERY to the retriever
    retrieval_step = RunnablePassthrough.assign(
        context=lambda x: retriever.invoke(TOPIC_QUERY) 
    )

    # 2. Formatting Step: Combine retrieved documents and pass along the LLM instruction
    formatting_step = RunnablePassthrough.assign(
        context=lambda x: "\n\n---\n\n".join([doc.page_content for doc in x["context"]])
    )

    # 3. Final Chain: Format the prompt, send to LLM, parse output
    rag_chain = (
        retrieval_step 
        | formatting_step
        # Input to Prompt is {'context': '...', 'input': 'instruction'}
        | {"context": lambda x: x["context"], "input": lambda x: final_llm_instruction} 
        | PROMPT
        | llm
        | StrOutputParser() 
    )

    # --- Invoke the Chain ---
    print("\n------------------Invoking RAG Chain-------------------------")
    
    # We pass an input dictionary containing the instruction text.
    json_questions = rag_chain.invoke({"input": final_llm_instruction})
    
    print("\n------------------Generated Questions (JSON)-----------------")
    responses = clean_llm_output(json_questions)
    return responses


if __name__ == "__main__":
    # --- Example of Dynamic Call (as if from an API) ---
    # To run this script directly, we'll take the file name from the command line arguments.
    # To simulate an endpoint:
    # 1. Run the script without arguments for an example.
    # 2. Run the script with arguments: python api_ready_generator.py "Guest and Client Relations.txt"

    if len(sys.argv) > 1:
        # User passed a file name (e.g., from an API call or CLI)
        source_file = sys.argv[1]
    else:
        # Default file name if run without arguments
        print("Using default source file. Pass a file name as a command-line argument to change it.")
        source_file = "Event Layout and Equipment Management.txt" 
    
    # The instruction can also be dynamic but is fixed here for simplicity
    instruction = "Generate 12 multiple-choice questions for an exam."
    
    try:
        output_json = run_rag_chain(source_file, instruction)
        print(output_json)
    except Exception as e:
        print(f"\nAn error occurred during RAG chain execution: {e}")
        # Optionally, check if the error is due to no documents found:
        if "CRITICAL: No relevant documents retrieved" in str(e):
             print("\nSuggestion: Check the spelling of the source file name and verify that the database exists.")
             
# --- End of api_ready_generator.py ---