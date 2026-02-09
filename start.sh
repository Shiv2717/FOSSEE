#!/bin/bash
# Quick Start Launcher for Chemical Visualizer
cd "$(dirname "$0")"
./scripts/start_backend.sh &
./scripts/start_frontend.sh &
