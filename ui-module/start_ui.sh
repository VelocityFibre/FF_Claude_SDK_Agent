#!/bin/bash
# Quick start script for Unified Convex Agent UI

echo "=========================================="
echo "🚀 Starting Unified Convex Agent UI"
echo "=========================================="
echo ""
echo "📊 Agent: Unified ConvexAgent"
echo "🔧 Tools: 17 (contractors, projects, tasks)"
echo "💾 Database: Convex (quixotic-crow-802)"
echo ""

# Start API
echo "Starting API on http://localhost:8000..."
cd "$(dirname "$0")"
../venv/bin/python3 unified_agent_api.py &
API_PID=$!

echo "API PID: $API_PID"
echo ""
echo "Waiting for API to start..."
sleep 3

# Check if API is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API is running!"
    echo ""
    echo "Opening UI in browser..."

    # Open browser
    if command -v xdg-open > /dev/null; then
        xdg-open unified_chat.html
    elif command -v open > /dev/null; then
        open unified_chat.html
    else
        echo "⚠️  Please manually open: $(pwd)/unified_chat.html"
    fi

    echo ""
    echo "=========================================="
    echo "✅ UI READY!"
    echo "=========================================="
    echo ""
    echo "Try asking:"
    echo "  • Show me all contractors"
    echo "  • List all projects"
    echo "  • How many contractors?"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""

    # Wait for user to stop
    wait $API_PID
else
    echo "❌ API failed to start"
    kill $API_PID 2>/dev/null
    exit 1
fi
