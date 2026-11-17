#!/usr/bin/env bash
# Lanzador local de la aplicación R5 — sigue el README al pie de la letra.
# Uso: ./ejecutar_app.sh [--puerto=8000] [--host=127.0.0.1]
set -e
cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
  echo "No se encontró .venv. Creándolo e instalando dependencias mínimas..."
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
fi

export PYTHONPATH=src
exec .venv/bin/python -m quindio.app "$@"
