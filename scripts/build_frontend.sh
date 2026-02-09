#!/bin/bash
# Build React frontend for production
echo "Building React Frontend for Production..."
cd "$(dirname "$0")/.."
cd react_frontend
echo ""
echo "Installing/updating dependencies..."
npm install
echo ""
echo "Building optimized production bundle..."
npm run build
echo ""
echo "Build complete! Files are in react_frontend/build/"
echo ""
echo "To serve the production build:"
echo "  - Use a web server (nginx, Apache)"
echo "  - Or install serve: npm install -g serve"
echo "  - Then run: serve -s build -l 3000"
