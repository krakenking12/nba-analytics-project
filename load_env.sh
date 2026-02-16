#!/bin/bash
# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✓ Loaded API key from .env file"
else
    echo "⚠️  No .env file found. Create one with:"
    echo "   echo 'NBA_API_KEY=your_key_here' > .env"
fi
