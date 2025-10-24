#!/bin/bash
# Quick start script for DionoAutogen AI

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║              DionoAutogen AI - Quick Start                 ║"
echo "║        Autonomous Software Development Platform            ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✓ Docker is installed"

# Detect Docker Compose version and set command
COMPOSE_CMD=""
if docker compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
    echo "✓ Docker Compose v2 detected"
elif docker-compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
    echo "✓ Docker Compose v1 detected"
else
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo ""

# Create environment files if they don't exist
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "✓ Backend environment file created"
fi

if [ ! -f frontend/.env ]; then
    echo "Creating frontend/.env from template..."
    cp frontend/.env.example frontend/.env
    echo "✓ Frontend environment file created"
fi

echo ""
echo "Starting services..."
echo ""

# Set HOST_WORKSPACE_PATH for Docker-in-Docker volume mounting
export HOST_WORKSPACE_PATH="$(pwd)/workspace"
echo "Workspace path: $HOST_WORKSPACE_PATH"

# Ensure workspace directory exists and is writable
mkdir -p "$HOST_WORKSPACE_PATH"
# Give permissive permissions for quick local development. Adjust as needed for production.
chmod 0777 "$HOST_WORKSPACE_PATH"

# Start services using detected compose command
$COMPOSE_CMD up -d

echo ""
echo "Waiting for services to be ready..."
sleep 5

# Check if services are running
if $COMPOSE_CMD ps | grep -q "Up"; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗[...]"
    echo "║                   🎉 Success!                              ║"
    echo "╚════════════════════════════════════════════════════════════╝[...]"
    echo ""
    echo "Services are running:"
    echo ""
    echo "  🌐 Frontend:  http://localhost:3000"
    echo "  🔧 Backend:   http://localhost:8000"
    echo "  📚 API Docs:  http://localhost:8000/docs"
    echo ""
    echo "Default login credentials:"
    echo "  Username: demo"
    echo "  Password: demo"
    echo ""
    echo "Useful commands:"
    echo "  View logs:     $COMPOSE_CMD logs -f"
    echo "  Stop services: $COMPOSE_CMD down"
    echo "  Restart:       $COMPOSE_CMD restart"
    echo ""
    echo "For more information, see SETUP.md"
    echo ""
else
    echo ""
    echo "❌ Some services failed to start. Check logs with:"
    echo "   $COMPOSE_CMD logs"
    exit 1
fi
