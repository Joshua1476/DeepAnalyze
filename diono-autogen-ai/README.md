# DionoAutogen AI

**Autonomous Software Architect & Data-Science Engineering Platform**

DionoAutogen AI is a fully autonomous coding platform that translates plain-English requests into complete software solutions. Built entirely with open-source tools and models.

## 🌟 Features

- **Autonomous Planning**: Translates natural language into concrete build plans
- **Multi-Language Support**: Python, JavaScript, Java, Go, Rust, TypeScript, Ruby, PHP
- **Secure Sandbox Execution**: Docker-based isolated code execution with thread pool
- **Cloud Integration**: Google Drive, Dropbox, OneDrive support
- **Media Processing**: 
  - **Image OCR**: Extract text from images (PNG, JPG, GIF, BMP, TIFF, WEBP, SVG)
  - **Video Transcription**: Speech-to-text from videos (MP4, AVI, MOV, MKV, etc.)
  - **URL Support**: Process media from URLs or local files
- **Real-Time Updates**: WebSocket-based progress tracking
- **Open Source**: 100% free and open-source stack

## 🚀 Quick Start

### Local Installation

```bash
# Clone and start
git clone https://github.com/Joshua1476/DeepAnalyze.git
cd DeepAnalyze/diono-autogen-ai
./start.sh
```

Visit `http://localhost:3000` and login with `demo`/`demo`.

### 📚 Comprehensive Guides

- **[Installation Guide](INSTALLATION_GUIDE.md)** - Complete setup for macOS, Windows, and Linux
- **[Free Hosting Guide](FREE_HOSTING_GUIDE.md)** - Deploy to Railway, Render, Fly.io, and more
- **[Setup Guide](SETUP.md)** - Detailed configuration and usage
- **[Media Processing](MEDIA_PROCESSING.md)** - Image OCR and video transcription guide

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
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py              # Main API
│   │   ├── sandbox_runner.py    # Code execution (non-blocking)
│   │   ├── media_processor.py   # Image/Video processing
│   │   ├── llm_wrapper.py       # LLM integration
│   │   └── ...
│   └── requirements.txt
├── frontend/                     # React frontend
├── scripts/                      # Execution scripts
├── INSTALLATION_GUIDE.md         # Cross-platform installation (NEW!)
├── FREE_HOSTING_GUIDE.md         # Free hosting platforms (NEW!)
├── MEDIA_PROCESSING.md           # Media processing guide
├── SETUP.md                      # Detailed setup guide
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

**Core Features:**
- `POST /api/plan` - Generate build plan from description
- `POST /api/run` - Execute code in sandbox (non-blocking)
- `POST /api/deploy` - Deploy application
- `POST /api/upload` - Upload files (auto-processes media)
- `POST /api/process-media` - Process image/video for transcription
- `GET /api/projects` - List all projects
- `GET /api/projects/{name}` - Get project details
- `WS /ws/{session_id}` - WebSocket for real-time updates

**Media Processing:**
```bash
# Process image from URL
curl -X POST http://localhost:8000/api/process-media \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://example.com/image.png",
    "project_name": "my-project"
  }'

# Process local video
curl -X POST http://localhost:8000/api/process-media \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "video.mp4",
    "project_name": "my-project"
  }'
```

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

## 🌐 Deployment Options

### Local Development
- ✅ Works on macOS (Intel & Apple Silicon), Windows, Linux
- ✅ Optimized for 16GB RAM / 500GB SSD
- ✅ See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

### Free Hosting Platforms
- **Railway** - Easiest for beginners
- **Render** - Generous free tier
- **Fly.io** - Docker-native, multiple regions
- **See [FREE_HOSTING_GUIDE.md](FREE_HOSTING_GUIDE.md)** for step-by-step instructions

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
