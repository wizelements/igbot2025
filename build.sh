#!/bin/bash
# Build script for Vercel Python deployment
# This ensures only the Python API is built

echo "Installing Python dependencies..."
pip install -r requirements-vercel.txt

echo "Python backend ready for deployment!"
