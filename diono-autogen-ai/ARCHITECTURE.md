# DionoAutogen AI - Architecture Documentation

## System Overview

DionoAutogen AI is an autonomous software development platform that translates natural language descriptions into complete software solutions. The system uses a microservices architecture with the following key components:

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (React Frontend)                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
┌────────────────────────┴────────────────────────────────────┐
│                     API Gateway                              │
│                   (FastAPI Backend)                          │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ LLM Wrapper  │  │   Sandbox    │  │  Ingestion   │      │
│  │              │  │   Runner     │  │   Module     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Auth      │  │    Cloud     │  │    Crypto    │      │
│  │              │  │   Drives     │  │    Utils     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐
│   Ollama     │  │    Redis    │  │  Workspace │
│   (LLM)      │  │   (Cache)   │  │  (Storage) │
└──────────────┘  └─────────────┘  └────────────┘
```

## Core Components

### 1. Frontend (React)

**Technology Stack:**
- React 18
- Vite (Build tool)
- TailwindCSS (Styling)
- Monaco Editor (Code editing)
- Zustand (State management)
- Axios (HTTP client)

**Key Features:**
- Real-time WebSocket communication
- Code editor with syntax highlighting
- Markdown rendering for AI responses
- Authentication and session management
- Cloud provider integration UI
- API key management

**File Structure:**
```
frontend/
├── src/
│   ├── pages/
│   │   ├── Login.jsx          # Authentication
│   │   ├── Dashboard.jsx      # Main interface
│   │   ├── Providers.jsx      # Cloud storage
│   │   └── Keys.jsx           # API keys
│   ├── store/
│   │   └── authStore.js       # Auth state
│   ├── api/
│   │   └── client.js          # API client
│   └── App.jsx                # Main app
└── package.json
```

### 2. Backend (FastAPI)

**Technology Stack:**
- FastAPI (Web framework)
- Uvicorn (ASGI server)
- Pydantic (Data validation)
- Docker SDK (Sandbox execution)
- SQLAlchemy (Database ORM)
- Redis (Caching)

**Key Modules:**

#### a. Main Application (`main.py`)
- API endpoints
- WebSocket handling
- Request routing
- Middleware configuration

#### b. LLM Wrapper (`llm_wrapper.py`)
- Abstraction layer for LLM APIs
- Support for multiple providers (Ollama, OpenAI, etc.)
- Streaming response handling
- Plan generation
- Code generation

#### c. Sandbox Runner (`sandbox_runner.py`)
- Secure code execution in Docker containers
- Multi-language support
- Resource limits (CPU, memory, timeout)
- Output capture and error handling

#### d. Document Ingestion (`ingestion.py`)
- File type detection
- Data parsing (CSV, JSON, Excel, etc.)
- Content extraction
- Metadata generation

#### e. Cloud Drives (`cloud_drives.py`)
- Google Drive integration
- Dropbox integration
- OneDrive support (extensible)
- File listing and download

#### f. Authentication (`auth.py`)
- JWT token generation
- Token verification
- User authentication
- Password hashing

#### g. Crypto Utils (`crypto_utils.py`)
- Data encryption/decryption
- Password hashing
- Secure credential storage

### 3. Infrastructure

#### Docker Compose Services

**Backend Service:**
- FastAPI application
- Mounts workspace volume
- Connects to Docker socket for sandbox execution
- Environment-based configuration

**Frontend Service:**
- React application
- Nginx for serving static files
- Proxies API requests to backend

**Redis Service:**
- Session storage
- Caching layer
- Task queue (future)

**Ollama Service:**
- Local LLM inference
- GPU support (optional)
- Model management

## Data Flow

### 1. Build Plan Generation

```
User Input → Frontend → Backend API
                          ↓
                    LLM Wrapper
                          ↓
                    Ollama/OpenAI
                          ↓
                    Parse Response
                          ↓
                    Save to Workspace
                          ↓
                    Return to User
```

### 2. Code Execution

```
Code Input → Backend API
                ↓
          Sandbox Runner
                ↓
          Create Docker Container
                ↓
          Execute Code
                ↓
          Capture Output
                ↓
          Return Results
```

### 3. Real-time Updates

```
User Action → WebSocket Message
                    ↓
              Backend Handler
                    ↓
              Process Action
                    ↓
              Broadcast Update
                    ↓
              All Connected Clients
```

## Security Architecture

### Authentication Flow

1. User submits credentials
2. Backend validates against database
3. JWT token generated with expiration
4. Token stored in frontend (localStorage)
5. Token included in all API requests
6. Backend validates token on each request

### Sandbox Security

1. **Isolation**: Each execution in separate Docker container
2. **Resource Limits**: CPU, memory, and time constraints
3. **Network Control**: Configurable network access
4. **File System**: Isolated workspace per project
5. **Cleanup**: Automatic container removal after execution

### Data Security

1. **Encryption**: Sensitive data encrypted at rest
2. **HTTPS**: All communication over TLS (production)
3. **CORS**: Restricted origins
4. **Rate Limiting**: API request throttling
5. **Input Validation**: Pydantic models for all inputs

## Scalability Considerations

### Horizontal Scaling

**Backend:**
- Stateless design allows multiple instances
- Load balancer distributes requests
- Shared Redis for session management

**Frontend:**
- Static files served via CDN
- Multiple frontend instances behind load balancer

**Sandbox:**
- Docker Swarm or Kubernetes for container orchestration
- Distributed execution across nodes

### Vertical Scaling

**LLM Inference:**
- GPU acceleration for Ollama
- Larger models for better results
- Model quantization for efficiency

**Database:**
- PostgreSQL for production (vs SQLite)
- Read replicas for queries
- Connection pooling

## Monitoring and Observability

### Logging

- **Structured Logging**: JSON format with loguru
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Aggregation**: Centralized logging (ELK stack)

### Metrics

- **API Metrics**: Request count, latency, errors
- **System Metrics**: CPU, memory, disk usage
- **Business Metrics**: Projects created, code executions

### Health Checks

- `/health` endpoint for service status
- Docker health checks
- Automated alerting on failures

## Deployment Strategies

### Development

```bash
docker-compose up -d
```

### Staging

```bash
docker-compose -f docker-compose.staging.yml up -d
```

### Production

```bash
# Use Kubernetes or Docker Swarm
kubectl apply -f k8s/
```

## Extension Points

### Adding New LLM Providers

1. Extend `LLMWrapper` class
2. Implement provider-specific API calls
3. Add configuration in `config.py`
4. Update frontend provider selection

### Adding New Languages

1. Add language to `sandbox_runner.py`
2. Define Docker image
3. Specify execution command
4. Update frontend language selector

### Adding New Cloud Providers

1. Create provider class in `cloud_drives.py`
2. Implement `list_files()` and `download()`
3. Add provider to `CloudProvider` enum
4. Update frontend provider UI

## Performance Optimization

### Caching Strategy

- **Redis**: API responses, session data
- **Browser**: Static assets, API responses
- **CDN**: Frontend assets in production

### Database Optimization

- **Indexes**: On frequently queried fields
- **Connection Pooling**: Reuse connections
- **Query Optimization**: Use joins, avoid N+1

### Code Execution

- **Container Reuse**: Keep warm containers
- **Image Caching**: Pre-pull common images
- **Parallel Execution**: Multiple containers

## Future Enhancements

1. **Multi-user Collaboration**: Real-time code editing
2. **Version Control**: Git integration
3. **CI/CD Pipeline**: Automated testing and deployment
4. **Plugin System**: Extensible architecture
5. **Advanced Analytics**: Usage patterns, success metrics
6. **Mobile App**: iOS and Android clients
7. **Voice Interface**: Speech-to-code
8. **AI Pair Programming**: Continuous assistance

## Technology Decisions

### Why FastAPI?

- Modern, fast Python framework
- Automatic API documentation
- Built-in WebSocket support
- Type hints and validation
- Async/await support

### Why React?

- Component-based architecture
- Large ecosystem
- Excellent developer experience
- Strong community support

### Why Docker?

- Consistent environments
- Easy deployment
- Isolation and security
- Scalability

### Why Ollama?

- Local LLM inference
- No API costs
- Privacy-focused
- Easy model management
- GPU acceleration

## Conclusion

DionoAutogen AI is designed as a modular, scalable, and secure platform for autonomous software development. The architecture supports both local and cloud deployments, with clear extension points for future enhancements.
