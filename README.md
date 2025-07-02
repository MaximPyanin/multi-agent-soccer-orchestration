# langgraph-soccer-agent
**An agent-based FastAPI service orchestrated by LangGraph, combining live football data, web search and Azure OpenAI to deliver concise, context-aware answers about teams, fixtures, stats and more.**

## 🧰 Tech Stack

- **Language**: Python ≥3.11  
- **Framework**: FastAPI
- **Orchestration**: LangChain + LangGraph  
- **Data**: TheSportsDB API (soccer)  
- **Search**: Tavily (web)  
- **Containerization**: Docker & Docker Compose
---

## Core Components

- Supervisor Agent: Intelligent query routing and decision-making
- Football Data Agent: Specialized team data retrieval from TheSportsDB API
- Web Search Agent: Real-time web search capabilities via Tavily
- Conversation Response Agent: Natural language response generation

## 🚀 Features

- Multi-Agent Orchestration: LangGraph-based workflow management
- Intelligent Routing: Context-aware query classification and agent selection
- Real-time Data: Live football data from TheSportsDB API
- Web Search Integration: Enhanced information retrieval through Tavily Search
- Type Safety: Full Pydantic model validation

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Azure OpenAI API access
- Tavily API key

### Environment Setup
Create a .env file with your API credentials:
```bash
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_KEY=your_azure_key
TAVILY_API_KEY=your_tavily_key
```

### Running with Docker
```bash
# Build and start the service
docker-compose up --build

# Service will be available at http://localhost:8080
```

### Local Development
```bash
# Install dependencies with UV
uv sync

# Run the application
uv run -- uvicorn app.main:app --reload --port 8080
```

## API Usage

### Chat Endpoint
```bash
POST /api/v1/chat
Content-Type: application/json

{
  "question": "Tell me about Manchester United"
}
```
Response:
```json
{
  "data": {
    "answer": "Manchester United is an English professional football club..."
  }
}
```

## 📜 LICENSE
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
