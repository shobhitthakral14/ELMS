#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Starting ELMS Backend Server                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

cd backend

echo "📦 Checking dependencies..."
pip list | grep -q fastapi || echo "⚠️  Installing dependencies..."

echo ""
echo "🚀 Starting Backend Server..."
echo "   API: http://localhost:8001"
echo "   Docs: http://localhost:8001/docs"
echo ""

python run.py
