#!/usr/bin/env bash
set -e

# Render runs the build from the 'backend' rootDir.
# The dataset CSVs live one level up at datasets/ relative to the project root,
# so we copy them into a local 'datasets/' folder the app can see.

echo "==> Setting up datasets directory..."
mkdir -p datasets

# Copy CSVs from the project root's datasets folder (mounted at /opt/render/project/src/datasets)
DATASETS_SRC="/opt/render/project/src/datasets"
if [ -d "$DATASETS_SRC" ]; then
    cp -n "$DATASETS_SRC/topics.csv"   datasets/ 2>/dev/null || true
    cp -n "$DATASETS_SRC/quizzes.csv"  datasets/ 2>/dev/null || true
    echo "==> Datasets copied successfully."
else
    echo "==> WARNING: datasets source directory not found at $DATASETS_SRC"
fi

echo "==> Starting uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
