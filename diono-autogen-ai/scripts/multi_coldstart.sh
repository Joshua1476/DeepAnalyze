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

echo "Initializing ${#PROJECTS[@]} projects..."
echo ""

for project in "${PROJECTS[@]}"; do
    IFS=':' read -r name description <<< "$project"
    
    echo "=== Project: $name ==="
    echo "Description: $description"
    
    # Create workspace
    mkdir -p ../workspace/$name
    
    # Generate plan
    echo "Generating build plan..."
    curl -s -X POST http://localhost:8000/api/plan \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer demo-token" \
        -d "{
            \"description\": \"$description\",
            \"project_name\": \"$name\",
            \"requirements\": [],
            \"tech_stack\": []
        }" > ../workspace/$name/build_plan.json
    
    echo "✓ Plan generated for $name"
    echo ""
done

echo "All projects initialized!"
echo "Access the web interface at http://localhost:3000 to continue development"
