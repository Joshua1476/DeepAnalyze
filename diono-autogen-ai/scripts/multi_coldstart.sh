#!/bin/bash
# Multi-ability cold start - Initialize multiple projects

set -e

echo "=== DionoAutogen AI - Multi-Project Cold Start ==="

# Array of sample projects
declare -a PROJECTS=(
    "todo-api:Create a REST API for a todo application with user authentication"
    "data-dashboard:Build a data visualization dashboard with charts and graphs"
    "ml-pipeline:Create a machine learning pipeline for data preprocessing and model training"
)

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "Error: Backend is not running. Please start it first with 'docker-compose up'"
    exit 1
fi

# Get authentication token
echo "Authenticating..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=demo&password=demo")

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "Error: Failed to authenticate"
    exit 1
fi

echo "Initializing ${#PROJECTS[@]} projects..."
echo ""

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

for project in "${PROJECTS[@]}"; do
    IFS=':' read -r name description <<< "$project"
    
    echo "=== Project: $name ==="
    echo "Description: $description"
    
    # Create workspace
    mkdir -p "$PROJECT_ROOT/workspace/$name"
    
    # Generate plan (using jq for proper JSON escaping)
    echo "Generating build plan..."
    curl -s -X POST http://localhost:8000/api/plan \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d "$(jq -n \
            --arg desc "$description" \
            --arg project "$name" \
            '{description: $desc, project_name: $project, requirements: [], tech_stack: []}')" \
        > "$PROJECT_ROOT/workspace/$name/build_plan.json"
    
    echo "✓ Plan generated for $name"
    echo ""
done

echo "All projects initialized!"
echo "Access the web interface at http://localhost:3000 to continue development"
