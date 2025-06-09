import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Load your OpenAI key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 1. Load document
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sample_path = os.path.join(project_root, "documents", "SAML_Configuration_SiteBuild_Guide.docx")

print(f"Loading document from: {sample_path}")

# Check if file exists before loading
if not os.path.exists(sample_path):
    print(f"Error: File not found at {sample_path}")
    exit(1)

try:
    loader = UnstructuredFileLoader(sample_path)
    documents = loader.load()
    print(f"Successfully loaded document with {len(documents)} pages")
except Exception as e:
    print(f"Error loading document: {str(e)}")
    # Try using a different loader for markdown files
    from langchain_community.document_loaders import TextLoader
    print("Trying TextLoader instead...")
    loader = TextLoader(sample_path)
    documents = loader.load()
    print(f"Successfully loaded document with TextLoader: {len(documents)} pages")

# 2. Split document into chunks
print("Splitting document into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
print(f"Document split into {len(docs)} chunks")

# 3. Embed documents
print("Creating embeddings... This may take a moment.")
try:
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    db = FAISS.from_documents(docs, embeddings)
    print("Embeddings created successfully")
except Exception as e:
    print(f"Error creating embeddings: {str(e)}")
    exit(1)

# 4. Build chatbot (retriever + LLM)
retriever = db.as_retriever()
print("Setting up the language model...")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=openai_api_key)  # We're using gpt-3.5-turbo as default

try:
    print("Creating QA chain...")
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    print("QA chain created successfully")
except Exception as e:
    print(f"Error creating QA chain: {str(e)}")
    exit(1)

# 5. Ask questions
print("\n" + "="*50)
print("Custom Document ChatBot initialized!")
print("Type 'exit' to end the conversation")
print("="*50 + "\n")

while True:
    query = input("\nAsk a question (or type 'exit'): ")
    if query.lower() == "exit":
        break

    try:
        print("Processing your question...")
        result = qa.invoke(query)
        print("\nAnswer:", result["result"])
        
        # Uncomment to see source documents
        # print("\nSources:")
        # for i, doc in enumerate(result["source_documents"]):
        #     print(f"Source {i+1}: {doc.page_content[:150]}...\n")
    except Exception as e:
        print(f"Error generating answer: {str(e)}")

print("Goodbye!")
