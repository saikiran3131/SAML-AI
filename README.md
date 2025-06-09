# Custom Document ChatBot

A chatbot powered by LangChain and OpenAI that can answer questions based on your custom documents.

## Features

- Upload and process custom documents (PDF, DOCX, TXT, MD)
- Convert documents into embeddings for semantic search
- Chat with your documents using natural language
- Conversation memory for follow-up questions
- Source attribution for transparent answers

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone or download this repository
2. Install the required packages:

```powershell
py -m pip install -r requirements.txt
```

3. Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Adding Documents

Place your documents in the `documents` folder or use the ingestion script:

```powershell
py src/ingest.py
```

The ingestion script will help you add documents to the system and will guide you through the process.

Supported document types:
- PDF (.pdf)
- Microsoft Word (.docx)
- Text files (.txt)
- Markdown files (.md)

### Using the ChatBot

Start the chatbot:

```powershell
py src/chatbot.py
```

This will:
1. Load your documents and create embeddings if needed
2. Start an interactive chat session where you can ask questions
3. The chatbot will respond based on the content of your documents

Type `exit` to end the conversation.

## How It Works

1. **Document Loading**: Documents are loaded from the `documents` directory
2. **Text Processing**: Documents are split into chunks for processing
3. **Embedding Creation**: Document chunks are converted into vector embeddings
4. **Semantic Search**: When you ask a question, relevant chunks are retrieved
5. **Answer Generation**: OpenAI's model generates answers based on retrieved chunks

## Customization

You can customize the chatbot behavior by editing the parameters in `src/chatbot.py`:

- Change the OpenAI model (default: gpt-3.5-turbo)
- Adjust chunk size and overlap for document processing
- Modify the number of relevant chunks retrieved for each question

## Troubleshooting

- **API Key Issues**: Make sure your OpenAI API key is correctly set in the `.env` file
- **Document Processing Errors**: Check if your documents are in the supported formats
- **Out of Context Responses**: Try rephrasing your question or adding more relevant documents

## License

This project is provided for educational purposes only. Use at your own risk.


## pip install python-docx
## pip install unstructured

