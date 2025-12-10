#!/bin/bash

cd /usr/src/api && uv run alembic upgrade head && uv run uvicorn main:app --reload --port=8000 --host=0.0.0.0