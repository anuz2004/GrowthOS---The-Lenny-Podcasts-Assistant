# 🚀 GrowthOS

> An AI-powered workspace for intelligent conversations, Retrieval-Augmented Generation (RAG), artifact generation, and multi-provider Large Language Models.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

GrowthOS is an AI workspace that combines conversational AI with Retrieval-Augmented Generation (RAG), enabling users to interact with a curated knowledge base while generating code, documents, and rich artifacts.

The application supports multiple LLM providers, workspace organization, chat history, streaming responses, and artifact previews in a clean terminal-inspired interface.

---

# ✨ Features

### 💬 AI Chat
- Multi-turn conversations
- Streaming responses
- Automatic chat title generation
- Persistent chat history

### 📂 Workspaces
- Create multiple workspaces
- Organize conversations by project
- Workspace-specific chat sessions

### 🧠 Retrieval-Augmented Generation (RAG)
- Semantic search over indexed transcripts
- Vector similarity search using pgvector
- Context-aware AI responses
- Episode citation support

### 📄 Artifact Generation
Generate and preview:

- HTML
- Markdown
- Source Code
- SQL
- Documentation

Features include:

- Live Preview
- Syntax Highlighting
- Copy to Clipboard
- Download Generated Files

### 🤖 Multi-Provider LLM Support

Supports multiple AI providers including:

- Ollama (Local)
- Groq
- OpenAI
- Anthropic Claude
- xAI Grok

Provider selection is configurable per chat session.

### 📚 Knowledge Base

GrowthOS includes a transcript ingestion pipeline that:

- Parses podcast transcripts
- Chunks long documents
- Generates embeddings
- Stores vectors in PostgreSQL
- Retrieves relevant context using semantic search

---

# 🏗️ Architecture

```
                 +-------------------+
                 |     React UI      |
                 +---------+---------+
                           |
                           |
                     REST + Streaming
                           |
                           ▼
                +----------------------+
                |    FastAPI Backend   |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          ▼                                 ▼
    LLM Providers                     RAG Pipeline
 (Groq/OpenAI/Ollama)          Retrieval + Embeddings
          |                                 |
          +---------------+-----------------+
                          |
                          ▼
                  PostgreSQL + pgvector
                        (Supabase)
```

---

# 🛠️ Tech Stack

## Frontend

- React
- TypeScript
- Vite
- Axios
- React Markdown
- Tailwind CSS

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- Alembic
- AsyncIO

## AI

- Ollama
- Groq
- OpenAI
- Anthropic Claude
- xAI Grok

## Database

- PostgreSQL
- Supabase

---

# 📁 Project Structure

```
GrowthOS
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── database
│   │   ├── ingest
│   │   ├── llm
│   │   ├── models
│   │   ├── rag
│   │   ├── services
│   │   └── main.py
│   │
│   ├── data
│   ├── scripts
│   ├── requirements.txt
│   └── .env
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/GrowthOS.git

cd GrowthOS
```

---

# Backend Setup

Create a virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
APP_NAME=GrowthOS
APP_VERSION=1.0.0

DATABASE_URL=YOUR_DATABASE_URL

OPENAI_API_KEY=YOUR_KEY
GROQ_API_KEY=YOUR_KEY
ANTHROPIC_API_KEY=YOUR_KEY
XAI_API_KEY=YOUR_KEY

OLLAMA_HOST=http://localhost:11434
```

---

# Database

Run migrations

```bash
alembic upgrade head
```

---

# Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs at

```
http://localhost:8000
```

---

# Frontend Setup

Navigate to frontend

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run development server

```bash
npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# Transcript Ingestion

To build the knowledge base:

```bash
python scripts/ingest.py
```

This process:

- Parses transcripts
- Splits into chunks
- Generates embeddings
- Stores vectors in PostgreSQL

---

# Using GrowthOS

## 1. Create a Workspace

Create a workspace for your project.

---

## 2. Create a Chat

Each workspace can contain multiple chat sessions.

---

## 3. Select an AI Provider

Choose from:

- Ollama
- Groq
- OpenAI
- Claude
- Grok

---

## 4. Ask Questions

Examples:

```
Tell me about Lenny's podcast with Jensen Huang.
```

```
Summarize the episode about startups.
```

```
Create a responsive landing page using HTML and CSS.
```

```
Generate SQL queries for an employee database.
```

---

## 5. View Artifacts

Generated artifacts can be:

- Previewed
- Copied
- Downloaded

---

# Screenshots

## Dashboard

> *(Add screenshot here)*

---

## Chat Interface

> *(Add screenshot here)*

---

## Artifact Viewer

> *(Add screenshot here)*

---

## Workspace Management

> *(Add screenshot here)*

---

# Future Improvements

- User Authentication
- File Upload Support
- PDF Knowledge Base
- Image Generation
- Multi-user Collaboration
- Agent Workflows
- Plugin System
- Cloud Vector Database Support

---

# License

This project is licensed under the MIT License.

---

# Author

**Anuz B K**

M.Sc. Software Systems

Coimbatore Institute of Technology

GitHub: https://github.com/anuz2004

---

⭐ If you found this project useful, consider giving it a star!
