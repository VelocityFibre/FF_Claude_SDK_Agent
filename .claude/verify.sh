#!/bin/bash
# Team verification script
# Run this after pulling team changes

case "$1" in
  qfield)
    echo "🔍 Verifying QFieldCloud..."
    curl -s localhost:8082/health 2>/dev/null || echo "❌ QFieldCloud not running"
    ;;

  wa)
    echo "🔍 Verifying WhatsApp..."
    curl -s localhost:8081/status 2>/dev/null || echo "❌ WhatsApp service not running"
    ;;

  storage)
    echo "🔍 Verifying Storage API..."
    curl -s localhost:8091/health 2>/dev/null || echo "❌ Storage API not running"
    ;;

  tests)
    echo "🔍 Running tests..."
    if [ -d tests/ ]; then
        ./venv/bin/pytest tests/ -v --tb=short
    else
        echo "⚠️  No tests directory found"
    fi
    ;;

  all)
    $0 qfield
    $0 wa
    $0 storage
    $0 tests
    ;;

  *)
    echo "Usage: $0 {qfield|wa|storage|tests|all}"
    exit 1
    ;;
esac
