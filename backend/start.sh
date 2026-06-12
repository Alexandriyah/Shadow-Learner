#!/usr/bin/env bash
set -e

echo "==> Setting up datasets directory..."
mkdir -p datasets

# Try Render's absolute path first, then fall back to relative path (Railway / local)
if [ -d "/opt/render/project/src/datasets" ]; then
    DATASETS_SRC="/opt/render/project/src/datasets"
elif [ -d "../datasets" ]; then
    DATASETS_SRC="../datasets"
else
    DATASETS_SRC=""
fi

if [ -n "$DATASETS_SRC" ]; then
    cp -n "$DATASETS_SRC/topics.csv"   datasets/ 2>/dev/null || true
    cp -n "$DATASETS_SRC/quizzes.csv"  datasets/ 2>/dev/null || true
    echo "==> Datasets copied from $DATASETS_SRC"
else
    echo "==> WARNING: No datasets source directory found. Skipping CSV copy."
fi

echo "==> Starting uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
