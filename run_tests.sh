#!/usr/bin/env bash

if [ -d "venv" ]; then
  source venv/bin/activate
  echo "Virtual environment activated."
else
  echo "Virtual environment not found. Please ensure 'venv' exists."
  exit 1
fi

# Run pytest and store exit code
echo "🚀 Running test suite..."
pytest --maxfail=1 --disable-warnings -q
TEST_EXIT_CODE=$?

# Deactivate virtual environment
deactivate

# Check result
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "All tests passed!"
  exit 0
else
  echo "Some tests failed."
  exit 1
fi
