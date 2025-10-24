# DionoAutogen AI

**Autonomous Software Architect & Data-Science Engineering Platform**

DionoAutogen AI is a fully autonomous coding platform that translates plain-English requests into complete software solutions. Built entirely with open-source tools and models.

## 🌟 Features

- **Autonomous Planning**: Translates natural language into concrete build plans
- **Multi-Language Support**: Python, JavaScript, Java, Go, Rust, and more
- **Secure Sandbox Execution**: Docker-based isolated code execution
- **Cloud Integration**: Google Drive, Dropbox, OneDrive support
- **Real-Time Updates**: WebSocket-based progress tracking
- **Open Source**: 100% free and open-source stack

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.10+ (for local backend development)

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd diono-autogen-ai

# Start all services
docker-compose up -d

# Access the platform
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### Manual Setup

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
diono-autogen-ai/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── scripts/          # Execution scripts
└── docker-compose.yml
```

## 🔧 Configuration

### Environment Variables

Create `.env` files in backend and frontend directories:

**Backend `.env`:**
```
LLM_MODEL=mistral-7b-instruct
LLM_API_URL=http://localhost:11434
WORKSPACE_DIR=/workspace
MAX_EXECUTION_TIME=300
```

**Frontend `.env`:**
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

## 📚 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

- `POST /api/plan` - Generate build plan from description
- `POST /api/run` - Execute code in sandbox
- `POST /api/deploy` - Deploy application
- `WS /ws/{session_id}` - WebSocket for real-time updates

## 🛠️ Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style

```bash
# Backend
black app/
flake8 app/

# Frontend
npm run lint
npm run format
```

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- FastAPI
- React
- Docker
- Open-source LLM models (Llama, Mistral, etc.)
