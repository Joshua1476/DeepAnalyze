#!/bin/bash
# Single execution mode - Run a single task

set -e

echo "=== DionoAutogen AI - Single Task Execution ==="

# Check if project name is provided
if [ -z "$1" ]; then
    echo "Usage: ./single.sh <project_name> <task_description>"
    exit 1
fi

PROJECT_NAME=$1
TASK_DESCRIPTION=$2

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "Error: Backend is not running. Please start it first with 'docker-compose up'"
    exit 1
fi

# Create project workspace
mkdir -p ../workspace/$PROJECT_NAME

echo "Project: $PROJECT_NAME"
echo "Task: $TASK_DESCRIPTION"
echo ""

# Generate build plan
echo "Generating build plan..."
PLAN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/plan \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer demo-token" \
    -d "{
        \"description\": \"$TASK_DESCRIPTION\",
        \"project_name\": \"$PROJECT_NAME\",
        \"requirements\": [],
        \"tech_stack\": []
    }")

echo "Build plan generated!"
echo "$PLAN_RESPONSE" | jq '.'

# Save plan to file
echo "$PLAN_RESPONSE" > ../workspace/$PROJECT_NAME/build_plan.json

echo ""
echo "Build plan saved to workspace/$PROJECT_NAME/build_plan.json"
echo "You can now implement the plan using the web interface at http://localhost:3000"
