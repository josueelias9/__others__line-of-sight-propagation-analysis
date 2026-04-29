#! /usr/bin/env bash

set -e
set -x

PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)

# Wait for the DB to be ready
PYTHONPATH="$PROJECT_ROOT" python app/backend_pre_start.py

# Create tables and load initial data
PYTHONPATH="$PROJECT_ROOT" python app/initial_data.py
