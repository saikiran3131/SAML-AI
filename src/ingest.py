import os
import sys
import shutil
from datetime import datetime

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print("=" * 50)
    print(" Document Ingestion Tool for Custom ChatBot")
    print("=" * 50)
    print()

def ingest_document(source_path, documents_dir):
    """Copy a document to the documents directory."""
    if not os.path.exists(source_path):
        return False, f"File not found: {source_path}"
    
    try:
        # Get the filename without path
        filename = os.path.basename(source_path)
        
        # Create a timestamped version to avoid overwriting
        name, ext = os.path.splitext(filename)
        timestamped_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        
        # Destination path
        dest_path = os.path.join(documents_dir, timestamped_name)
        
        # Copy the file
        shutil.copy2(source_path, dest_path)
        
        return True, f"Document added: {timestamped_name}"
    except Exception as e:
        return False, f"Error adding document: {str(e)}"

def main():
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    documents_dir = os.path.join(project_root, "documents")
    
    # Ensure documents directory exists
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)
    
    clear_screen()
    print_header()
    
    # Show current documents
    print("Current documents:")
    
    docs = [f for f in os.listdir(documents_dir) if os.path.isfile(os.path.join(documents_dir, f))]
    if docs:
        for i, doc in enumerate(docs, 1):
            print(f"  {i}. {doc}")
    else:
        print("  No documents found.")
    
    print("\nAccepted file types: .pdf, .txt, .md, .docx")
    print("\nTo add a document, enter the full path to the file.")
    print("To exit, type 'exit'.")
    
    while True:
        print()
        file_path = input("Enter file path: ").strip()
        
        if file_path.lower() == 'exit':
            break
        
        success, message = ingest_document(file_path, documents_dir)
        print(message)
        
        if success:
            print("Document added successfully. After adding all documents, run the chatbot to rebuild the knowledge base.")
    
    print("\nExiting document ingestion tool.")

if __name__ == "__main__":
    main()
