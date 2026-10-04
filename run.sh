#!/usr/bin/env bash
# =====================================================================
# NEXUS CORE - Activity Runner Wrapper
# =====================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

export GIT_DISCOVERY_ACROSS_FILESYSTEM=1
export PYTHONUNBUFFERED=1

# Executa com python3 padrão ou python do ambiente
PYTHON_BIN="python3"
if [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
    PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
elif [ -f "/root/.orchestrator-venv/bin/python" ]; then
    PYTHON_BIN="/root/.orchestrator-venv/bin/python"
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/engine/bot.py" "$@"
