# DionoAutogen AI - Setup Guide

Complete setup instructions for the DionoAutogen AI platform.

## Prerequisites

### Required Software

1. **Docker & Docker Compose**
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **jq (JSON processor)**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install jq
   
   # macOS
   brew install jq
   
   # Or download from: https://stedolan.github.io/jq/download/
   ```

2. **NVIDIA Docker (Optional, for GPU support)**
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-docker2
   sudo systemctl restart docker
   ```

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd diono-autogen-ai

# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Make scripts executable
chmod +x scripts/*.sh
```

### 2. Configure Environment

Edit `backend/.env`:
```bash
# LLM Configuration
LLM_MODEL=mistral-7b-instruct
LLM_API_URL=http://ollama:11434

# Security (IMPORTANT: Change in production!)
SECRET_KEY=your-super-secret-key-change-this

# Optional: Add API keys for external LLM services
# LLM_API_KEY=your-openai-api-key
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Initialize Data

```bash
# Prepare sample data and pull models
cd scripts
./prepare_data.sh
```

### 5. Access the Platform

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Default Login**: 
- Username: `demo`
- Password: `demo`

## Usage Examples

### Single Task Execution

```bash
cd scripts
./single.sh my-project "Create a REST API for user management"
```

### Multi-Project Cold Start

```bash
cd scripts
./multi_coldstart.sh
```

### Reinforcement Learning Mode

```bash
cd scripts
./multi_rl.sh my-rl-project 10
```

## Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## Configuration

### LLM Models

#### Using Ollama (Local, Recommended)

```bash
# Pull models
docker exec diono-ollama ollama pull mistral:7b-instruct
docker exec diono-ollama ollama pull codellama:7b

# List available models
docker exec diono-ollama ollama list
```

#### Using OpenAI API

Update `backend/.env`:
```bash
LLM_API_URL=https://api.openai.com/v1
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4
```

### Cloud Storage Integration

1. Navigate to **Providers** page in the web interface
2. Click **Connect** on your preferred provider
3. Enter credentials:
   - **Google Drive**: Client ID and Secret
   - **Dropbox**: Access Token
   - **OneDrive**: Client credentials

### API Keys Management

1. Navigate to **API Keys** page
2. Click **Add New Key**
3. Enter service details and API key
4. Keys are encrypted and stored securely

## Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose logs backend

# Restart service
docker-compose restart backend
```

### Ollama model not found

```bash
# Pull the model
docker exec diono-ollama ollama pull mistral:7b-instruct

# Verify
docker exec diono-ollama ollama list
```

### Permission errors

```bash
# Fix workspace permissions
sudo chown -R $USER:$USER workspace/
chmod -R 755 workspace/
```

### Port already in use

```bash
# Change ports in docker-compose.yml
# For example, change "3000:3000" to "3001:3000"
```

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` in backend/.env
- [ ] Use strong passwords
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Set up backup strategy
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Use environment-specific configs

### Recommended Setup

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Enable auto-restart
docker-compose -f docker-compose.prod.yml up -d --restart=always

# Set up reverse proxy (nginx)
# Configure SSL certificates
# Set up monitoring and logging
```

## Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Check all services
docker-compose ps
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

## Backup and Restore

### Backup

```bash
# Backup workspace
tar -czf backup-$(date +%Y%m%d).tar.gz workspace/

# Backup database
docker exec diono-backend cp /app/diono_autogen.db /workspace/backup.db
```

### Restore

```bash
# Restore workspace
tar -xzf backup-20240115.tar.gz

# Restore database
docker cp backup.db diono-backend:/app/diono_autogen.db
docker-compose restart backend
```

## Support

For issues and questions:
- Check the logs: `docker-compose logs`
- Review API docs: http://localhost:8000/docs
- Check GitHub issues
- Contact support

## License

MIT License - See LICENSE file for details
