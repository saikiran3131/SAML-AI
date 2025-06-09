import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import (
    UnstructuredFileLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    PyPDFLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="📄 SAML Document Q&A", layout="wide")
st.title("📄 LRN SAML Configuration portal")
st.markdown("This tool analyzes documents from the `documents/` folder. Supported formats: `.pdf`, `.txt`, `.docx`, `.xlsx`.")

# Setup session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define constants
#DOCUMENT_FOLDER = "documents"
DOCUMENT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../documents"))

SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".docx", ".xlsx"]

# Read and load documents
documents = []
if os.path.isdir(DOCUMENT_FOLDER):
    for filename in os.listdir(DOCUMENT_FOLDER):
        filepath = os.path.join(DOCUMENT_FOLDER, filename)
        ext = os.path.splitext(filename)[1].lower()

        loader = None  # Initialize outside

        if ext == ".pdf":
            try:
                loader = PyPDFLoader(filepath)
            except Exception as e:
                st.warning(f"Primary PDF load failed for `{filename}`: {e}")
                try:
                    loader = UnstructuredFileLoader(filepath)
                except Exception as e2:
                    st.error(f"Fallback PDF load also failed for `{filename}`: {e2}")
                    continue  # ❗ Skip to next file if both loaders fail

        elif ext == ".txt":
            loader = TextLoader(filepath)

        elif ext == ".docx":
            loader = Docx2txtLoader(filepath)

        elif ext == ".xlsx":
            loader = UnstructuredExcelLoader(filepath)

        else:
            st.info(f"⚠️ Skipped unsupported file type: `{filename}`")
            continue

        try:
            if loader:
                docs = loader.load()
                documents.extend(docs)
                st.success(f"✅ Loaded `{filename}` with {len(docs)} document chunks.")
        except Exception as e:
            st.warning(f"❌ Failed to load `{filename}`: {e}")

else:
    st.error(f"`{DOCUMENT_FOLDER}` folder not found.")
    st.stop()

if not documents:
    st.warning("No valid documents found in the `documents/` folder.")
    st.stop()

# Split documents
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(documents)

# Embeddings and vector store
embeddings = OpenAIEmbeddings(api_key=openai_api_key)
vectorstore = FAISS.from_documents(split_docs, embeddings)
retriever = vectorstore.as_retriever()

# Set up LLM and QA Chain (with memory for chat history)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=openai_api_key)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Chat interface
st.markdown("### 💬 Ask a question about the documents:")
user_input = st.chat_input("Ask your question here...")

# Display previous messages
for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        result = qa_chain.invoke({
            "question": user_input,
            "chat_history": st.session_state.chat_history
        })
        answer = result["answer"]

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.chat_history.append((user_input, answer))

    # Optional: show sources
    with st.expander("📚 Show Source Documents"):
        for i, doc in enumerate(result.get("source_documents", [])):
            st.markdown(f"**Source {i+1}**")
            st.write(doc.page_content[:500])
