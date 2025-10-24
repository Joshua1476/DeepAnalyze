#!/bin/bash
# Prepare data and environment for DionoAutogen AI

set -e

echo "=== DionoAutogen AI - Data Preparation ==="

# Create necessary directories
echo "Creating directories..."
mkdir -p ../workspace
mkdir -p ../backend/logs
mkdir -p ../data/uploads
mkdir -p ../data/models

# Download sample datasets (if needed)
echo "Preparing sample datasets..."
mkdir -p ../data/samples

# Create sample CSV
cat > ../data/samples/sample_data.csv << EOF
id,name,value,category
1,Item A,100,Category 1
2,Item B,200,Category 2
3,Item C,150,Category 1
4,Item D,300,Category 3
5,Item E,250,Category 2
EOF

# Create sample JSON
cat > ../data/samples/sample_config.json << EOF
{
  "project": "sample-project",
  "version": "1.0.0",
  "settings": {
    "debug": false,
    "max_workers": 4
  }
}
EOF

echo "✓ Sample datasets created"

# Pull Ollama models (if Ollama is running)
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Pulling Ollama models..."
    docker exec diono-ollama ollama pull mistral:7b-instruct || true
    echo "✓ Models pulled"
else
    echo "⚠ Ollama not running. Skipping model download."
fi

# Set permissions
echo "Setting permissions..."
chmod -R 755 ../workspace
chmod -R 755 ../data

echo ""
echo "Data preparation complete!"
echo "Sample data available in: data/samples/"
