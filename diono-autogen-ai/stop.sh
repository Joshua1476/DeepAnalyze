#!/bin/bash
# Stop DionoAutogen AI services

echo "Stopping DionoAutogen AI services..."
docker-compose down

echo ""
echo "✓ All services stopped"
echo ""
echo "To remove all data (including workspace):"
echo "  docker-compose down -v"
