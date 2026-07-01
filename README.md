# SHL Hiring Assistant

An AI-powered hiring assistant that helps recruiters identify the most suitable SHL assessments by conducting a natural language conversation.

The assistant asks follow-up questions to understand the hiring requirements, extracts structured hiring criteria using an LLM, searches an embedding-based assessment catalog, and recommends the most relevant SHL assessments.

---

## Features

- Conversational hiring assistant
- Multi-turn conversation support
- Automatic requirement gathering
- Structured information extraction using an LLM
- Semantic search using a Vector Database
- Returns the Top-K SHL assessment recommendations
- FastAPI REST API
- Simple terminal chat client

---

## Project Architecture

```
                User
                  │
                  ▼
           FastAPI (/chat)
                  │
                  ▼
             AI Agent
                  │
                  ▼
          LLM Conversation
                  │
                  ▼
 Structured Hiring Requirements
                  │
                  ▼
        Vector Database Search
                  │
                  ▼
      SHL Assessment Catalog
                  │
                  ▼
     Top Assessment Recommendations
```

---

## Project Structure

```
.
├── app.py                 # FastAPI server
├── agent.py               # Agent orchestration
├── base_nodes.py          # PocketFlow workflow engine
├── react_nodes.py         # Conversation node(s)
├── llm.py                 # LLM wrapper
├── vector_db.py           # ChromaDB interface
├── chat.py                # CLI client
├── catalog_data.json      # SHL assessment catalog
├── requirements.txt
└── README.md
```

---

## Workflow

### Step 1

The recruiter starts a conversation.

Example:

```
I need to hire a Java backend developer.
```

---

### Step 2

The assistant gathers missing information.

Example:

- Experience level
- Required competencies
- Assessment types

---

### Step 3

Once enough information has been collected, the LLM returns structured JSON.

Example:

```json
{
    "role": "Java Developer",
    "competencies": [
        "Java",
        "Problem Solving"
    ],
    "job_level": [
        "Mid-Professional"
    ],
    "test_type_keys": [
        "Knowledge & Skills",
        "Simulations"
    ]
}
```

---

### Step 4

The application builds a semantic search query.

Example

```
Java Developer
Java
Problem Solving
Mid-Professional
Knowledge & Skills
Simulations
```

---

### Step 5

The query is searched against the SHL assessment catalog using a vector database.

Top matching assessments are returned.

---

## API

### Health Check

```
GET /health
```

Response

```json
{
    "status": "ok"
}
```

---

### Chat Endpoint

```
POST /chat
```

Request

```json
{
    "messages": [
        {
            "role": "user",
            "content": "Hiring a Java developer."
        }
    ]
}
```

---

Response (Conversation Continues)

```json
{
    "reply": "What experience level are you hiring for?",
    "recommendations": null,
    "end_of_conversation": false
}
```

---

Response (Recommendations)

```json
{
    "reply": "Based on your requirements, here are the best assessments.",
    "recommendations": [
        {
            "name": "Java Assessment",
            "url": "...",
            "description": "..."
        }
    ],
    "end_of_conversation": true
}
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd shl-hiring-assistant
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Server

```bash
uvicorn app:app --reload
```

Server runs at

```
http://127.0.0.1:8000
```

---

## Running the CLI Client

Open another terminal

```bash
python chat.py
```

Example

```
You: Hiring a Java developer.

Assistant:
What experience level are you hiring for?
```

---

## Technologies Used

- Python
- FastAPI
- Pydantic
- Google Gemini API
- ChromaDB
- PocketFlow (workflow orchestration)
- Vector Embeddings

---

## Conversation State

The agent maintains conversation history and shared state including:

- Conversation messages
- Current iteration count
- Maximum conversation iterations
- Last reasoning step

This enables coherent multi-turn conversations before recommendations are generated.

---

## Recommendation Pipeline

```
Recruiter
      │
      ▼
Conversation
      │
      ▼
LLM extracts hiring requirements
      │
      ▼
Structured JSON
      │
      ▼
Embedding Query
      │
      ▼
Vector Search
      │
      ▼
Top SHL Assessments
      │
      ▼
API Response
```

---

## Future Improvements

- Web frontend
- Streaming responses
- Better reranking of assessments
- Conversation memory
- Authentication
- Docker deployment
- Unit tests
- Evaluation framework
- Support for multiple assessment providers

---

## License

This project is intended for educational and research purposes.
