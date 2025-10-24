#!/bin/bash
# Multi-ability reinforcement learning mode

set -e

echo "=== DionoAutogen AI - Reinforcement Learning Mode ==="

# This script demonstrates iterative improvement through RL
# It executes code, evaluates results, and refines the approach

PROJECT_NAME=${1:-"rl-experiment"}
ITERATIONS=${2:-5}

echo "Project: $PROJECT_NAME"
echo "Iterations: $ITERATIONS"
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "Error: Backend is not running. Please start it first with 'docker-compose up'"
    exit 1
fi

# Create workspace
mkdir -p ../workspace/$PROJECT_NAME

for i in $(seq 1 $ITERATIONS); do
    echo "=== Iteration $i/$ITERATIONS ==="
    
    # Generate code
    echo "Generating code..."
    CODE="print('Hello from iteration $i')\nprint('Testing RL mode')"
    
    # Execute code
    echo "Executing code..."
    RESULT=$(curl -s -X POST http://localhost:8000/api/run \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer demo-token" \
        -d "{
            \"code\": \"$CODE\",
            \"language\": \"python\",
            \"project_name\": \"$PROJECT_NAME\",
            \"timeout\": 60
        }")
    
    echo "Result:"
    echo "$RESULT" | jq '.'
    
    # Save iteration results
    echo "$RESULT" > ../workspace/$PROJECT_NAME/iteration_$i.json
    
    echo ""
    sleep 2
done

echo "RL training complete!"
echo "Results saved to workspace/$PROJECT_NAME/"
