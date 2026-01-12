# Regulatory Compliance AI Assistant

An intelligent AI-powered assistant designed to help users navigate complex data protection laws and privacy regulations, with a specialized focus on the **Nigerian Data Protection Act (NDPA)**. This tool leverages state-of-the-art NLP models and vector databases to provide accurate, context-aware legal guidance.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Components](#project-components)
- [API Documentation](#api-documentation)
- [License](#license)

## 🎯 Overview

The Regulatory Compliance AI Assistant is designed to assist legal professionals, businesses, and individuals in understanding and complying with data protection regulations. The system provides intelligent responses to questions about privacy laws, summarizes legal documents, analyzes privacy policies, and identifies potential violations of user rights under the Nigerian Data Protection Act.

### Key Capabilities:
- **Legal Question Answering**: Get accurate answers to questions about data protection laws and regulations
- **Document Summarization**: Automatically summarize sections of the NDPA and other legal documents
- **Privacy Policy Analysis**: Analyze privacy policies and identify violations of user rights
- **Compliance Assistance**: Receive guidance on compliance with the Nigerian Data Protection Act

## ✨ Features

### Core Features:
1. **Intelligent Query Processing**
   - Natural language understanding powered by advanced NLP models
   - Context-aware responses based on indexed legal documents
   - Multi-turn conversation support

2. **Vector-Based Search**
   - Semantic search using embeddings for accurate document retrieval
   - Pinecone-powered indexing for fast and scalable search
   - Support for complex legal document queries

3. **Legal Document Processing**
   - Automatic conversion of text documents to structured JSON format
   - Embedding generation for semantic understanding
   - Support for multiple document types

4. **Web Interface**
   - User-friendly chat interface for easy interaction
   - Session management for maintaining conversation history
   - Real-time response streaming

5. **Multi-Tool Integration**
   - Cohere API for advanced NLP capabilities
   - SentenceTransformers for document embeddings
   - Gradio for model inference

## 🛠️ Technology Stack

### Backend:
- **Python 3.8+**: Core programming language
- **Flask**: Web framework for application server
- **Pinecone**: Vector database for semantic search and indexing
- **Cohere**: API for advanced NLP and text generation
- **SentenceTransformers**: Pre-trained models for generating embeddings
- **Gradio Client**: For interfacing with AI models

### Frontend:
- **HTML5**: Markup structure
- **CSS3**: Styling and layout
- **JavaScript**: Client-side interactivity

### Infrastructure:
- **Flask Session**: For managing user sessions and conversation history

## 📁 Project Structure

```
Regulatory_Compliance_AI_Assistant/
├── README.md                          # Project documentation (this file)
├── LICENSE                            # Project license
├── bash.sh                            # Shell script for running the application
├── chatweb.html                       # Standalone chat interface HTML
├── documents/                         # Directory containing legal documents
│   ├── content_section_embeddings.json # Embeddings of document content
│   ├── ndpa.json                      # Nigerian Data Protection Act in JSON format
│   ├── ndpa.txt                       # Nigerian Data Protection Act in text format
│   └── output.json                    # Processed output data
├── flask_session/                     # Flask session storage
│   └── [session files...]             # Individual session files
├── src/                               # Source code directory
│   ├── __init__.py                    # Package initialization
│   ├── agent.py                       # Main AI agent logic and prompt templates
│   ├── create_embeddings.py           # Script to generate embeddings from JSON data
│   ├── create_json.py                 # Utility to convert text files to JSON
│   ├── indexing.py                    # Pinecone indexing and configuration
│   ├── test_retrieval.py              # Testing script for retrieval functionality
│   └── create_json.py                 # JSON conversion utilities
└── webapp/                            # Flask web application
    ├── __init__.py                    # Package initialization
    ├── app.py                         # Main Flask application
    ├── static/                        # Static assets
    │   ├── css/
    │   │   └── style.css              # Application styling
    │   └── js/
    │       └── chat.js                # Client-side chat logic
    └── templates/                     # HTML templates
        └── chat.html                  # Chat interface template
```

## 🚀 Installation

### Prerequisites:
- Python 3.8 or higher
- pip (Python package manager)
- API keys for:
  - Pinecone (vector database)
  - Cohere (NLP API)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Regulatory_Compliance_AI_Assistant
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `flask==2.3.0`
- `flask-session==0.5.0`
- `pinecone-client==2.2.0`
- `sentence-transformers==2.2.0`
- `cohere==4.0.0`
- `gradio-client==0.2.0`
- `python-dotenv==1.0.0`

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root:
```
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
COHERE_API_KEY=your_cohere_api_key
FLASK_SECRET_KEY=your_secret_key
```

## ⚙️ Configuration

### Pinecone Setup:
1. Create a Pinecone account at https://www.pinecone.io
2. Create a serverless index named `regulatoryai`
3. Add your API key to the `.env` file

### Cohere Setup:
1. Create a Cohere account at https://cohere.com
2. Generate an API key
3. Add your API key to the `.env` file

### Model Configuration:
The project uses `all-MiniLM-L6-v2` as the default SentenceTransformer model for generating embeddings. To use a different model, modify the `model_name` parameter in relevant files.

## 📖 Usage

### Running the Application:

#### Option 1: Using Flask Development Server
```bash
cd webapp
python app.py
```
The application will start at `http://localhost:5000`

#### Option 2: Using the Bash Script
```bash
bash bash.sh
```

### Using the Chat Interface:
1. Open your web browser and navigate to `http://localhost:5000`
2. Type your question about data protection laws or regulations
3. The AI assistant will provide a comprehensive response
4. Your conversation history is automatically maintained

### Command Line Usage:

#### Generate Embeddings:
```bash
python src/create_embeddings.py
```

#### Convert Documents to JSON:
```bash
python src/create_json.py
```

#### Index Documents:
```bash
python src/indexing.py
```

#### Test Retrieval:
```bash
python src/test_retrieval.py
```

## 🔧 Project Components

### 1. **agent.py**
- **Purpose**: Core AI agent logic and prompt templates
- **Key Functions**: 
  - Initializes Cohere API client
  - Defines the system prompt for the AI assistant
  - Handles conversation flow
- **Configuration**: Contains the expert legal assistant prompt template

### 2. **create_embeddings.py**
- **Purpose**: Generates vector embeddings for document content
- **Key Functions**: 
  - `generate_embeddings(json_file, output_file, model_name)`: Creates embeddings from text data
- **Output**: JSON file containing document content with embeddings

### 3. **create_json.py**
- **Purpose**: Converts text documents to structured JSON format
- **Key Functions**: 
  - `convert_txt_to_json(input_file, output_file)`: Transforms .txt files to JSON
- **Usage**: Preprocessing legal documents before embedding generation

### 4. **indexing.py**
- **Purpose**: Manages Pinecone vector database indexing
- **Key Functions**:
  - Initializes Pinecone client
  - Creates serverless index
  - Loads and indexes documents
- **Configuration**: Handles cloud provider and region settings

### 5. **test_retrieval.py**
- **Purpose**: Tests the retrieval system with queries
- **Key Functions**: 
  - Initializes SentenceTransformer model
  - Configures Pinecone client
  - Tests query-to-embedding conversion and retrieval
- **Usage**: Validates the indexing and retrieval pipeline

### 6. **app.py** (Flask Application)
- **Purpose**: Main web application server
- **Key Routes**:
  - `/`: Renders the chat interface
  - `/chat`: Handles user messages and returns AI responses
- **Session Management**: Maintains conversation history per user

## 🔌 API Documentation

### Chat Endpoint

**Endpoint**: `POST /chat`

**Request Body**:
```json
{
  "message": "What are my rights under the NDPA?",
  "conversation_id": "optional_id"
}
```

**Response**:
```json
{
  "response": "According to the Nigerian Data Protection Act (NDPA)...",
  "conversation_history": [...],
  "status": "success"
}
```

**Status Codes**:
- `200`: Successful response
- `400`: Invalid request
- `500`: Server error

## 📝 Document Format

### Supported Input Formats:
- **Text Files (.txt)**: Plain text documents with sections separated by headers
- **JSON Files (.json)**: Structured JSON with sections and content

### Document Structure:
```json
{
  "sections": [
    {
      "title": "Section Title",
      "content": "Section content and details",
      "questions": ["Question 1", "Question 2"]
    }
  ]
}
```

## 🔍 Troubleshooting

### Common Issues:

1. **Pinecone Connection Error**
   - Verify API key in `.env` file
   - Check internet connection
   - Ensure index exists in Pinecone account

2. **Model Loading Error**
   - Ensure SentenceTransformers is properly installed
   - First run may take time to download model
   - Check available disk space

3. **Session Not Persisting**
   - Verify `flask_session` directory exists
   - Check Flask session configuration in `app.py`

4. **Embedding Generation Issues**
   - Ensure input JSON file exists in `documents/` directory
   - Verify JSON format is correct

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support & Contact

For questions or support, please open an issue on the GitHub repository or contact the development team.

---

**Last Updated**: January 12, 2026

**Version**: 1.0.0