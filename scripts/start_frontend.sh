#!/bin/bash
# Start React Frontend Development Server
echo "Starting React Frontend..."
cd "$(dirname "$0")/.."
cd react_frontend
echo ""
echo "Starting development server on http://localhost:3000"
npm start
