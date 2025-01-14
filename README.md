# DocMind

An intelligent document management system with advanced natural language processing capabilities for seamless document interaction and querying.

## Overview

DocMind is a full-stack application that revolutionizes how users interact with their documents. It combines state-of-the-art document processing with powerful RAG (Retrieval-Augmented Generation) capabilities, allowing users to upload various document types and query them using natural language.

## Features

- **Document Management**

  - Support for multiple document formats (PDF, PPT, CSV, etc.)
  - Secure document storage and retrieval
  - Advanced document parsing using unstructured.io
  - Full-text search capabilities

- **Intelligent Document Querying**

  - Natural language processing powered by LangChain/LlamaIndex
  - RAG Agents for context-aware document interaction
  - Efficient caching for improved response times

- **User Management**
  - Secure session-based authentication
  - Role-based access control
  - User profile management

## Architecture

DocMind follows a microservices architecture with the following components:

- **Frontend**: React.js-based user interface
- **API Gateway**: Central entry point for all client requests
- **Auth Service**: Handles user authentication and authorization
- **Document Service**: Manages document operations and storage
- **RAG Service**: Processes natural language queries and generates responses

## Tech Stack

### Backend

- FastAPI for microservices
- PostgreSQL for primary database
- Redis for caching
- Elasticsearch for document indexing and search
- AWS S3 for document storage

### Frontend

- React.js
- Modern UI libraries
- Responsive design

### NLP & Document Processing

- LangChain/LlamaIndex for NLP
- Autogen/Crewai for RAG agents
- unstructured.io for document parsing

### Infrastructure

- Docker for containerization
- Kubernetes for orchestration
- AWS/Cloud infrastructure

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Node.js 16+
- AWS Account (for S3)
- Elasticsearch instance

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/docmind.git
cd docmind
```

2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services

```bash
docker-compose up -d
```

4. Initialize the database

```bash
docker-compose exec api python init_db.py
```

### Development Setup

1. Backend services

```bash
cd services
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. Frontend

```bash
cd frontend
npm install
npm start
```

## API Documentation

API documentation is available at `/docs` when running the API service. The documentation is automatically generated using FastAPI's built-in Swagger UI.
