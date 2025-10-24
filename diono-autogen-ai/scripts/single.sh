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

# Create project workspace (relative to project root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
mkdir -p "$PROJECT_ROOT/workspace/$PROJECT_NAME"

echo "Project: $PROJECT_NAME"
echo "Task: $TASK_DESCRIPTION"
echo ""

# Generate build plan (using jq for proper JSON escaping)
echo "Generating build plan..."
PLAN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/plan \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "$(jq -n \
        --arg desc "$TASK_DESCRIPTION" \
        --arg project "$PROJECT_NAME" \
        '{description: $desc, project_name: $project, requirements: [], tech_stack: []}')")

echo "Build plan generated!"
echo "$PLAN_RESPONSE" | jq '.'

# Save plan to file
echo "$PLAN_RESPONSE" > "$PROJECT_ROOT/workspace/$PROJECT_NAME/build_plan.json"

echo ""
echo "Build plan saved to workspace/$PROJECT_NAME/build_plan.json"
echo "You can now implement the plan using the web interface at http://localhost:3000"
