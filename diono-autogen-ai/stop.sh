#!/bin/bash
# Stop DionoAutogen AI services

echo "Stopping DionoAutogen AI services..."

# Try Docker Compose v2 first, fall back to v1
if docker compose version > /dev/null 2>&1; then
    docker compose down
elif docker-compose version > /dev/null 2>&1; then
    docker-compose down
else
    echo "❌ Docker Compose not found"
    exit 1
fi

echo ""
echo "✓ All services stopped"
echo ""
echo "To remove all data (including workspace):"
echo "  docker-compose down -v"
