#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Starting ELMS Frontend Server                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

cd frontend

echo "📦 Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "⚠️  Installing dependencies..."
    npm install
fi

echo ""
echo "🚀 Starting Frontend Server..."
echo "   App: http://localhost:3000"
echo ""

npm run dev
