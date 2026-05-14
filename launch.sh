#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Activer le virtualenv si présent, sinon utiliser python3 système
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "AVERTISSEMENT : virtualenv introuvable. Utilisation de python3 système."
    echo "Lance d'abord ./install.sh si ce n'est pas fait."
    echo ""
fi

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

if [ "$PORT" -lt 1024 ] 2>/dev/null; then
    echo "ERREUR : le port $PORT est réservé au système (< 1024)."
    echo "Utilise un port >= 1024, par exemple : PORT=8141 ./launch.sh"
    exit 1
fi

echo "=== Lancement de FATE_95 ==="
echo ""
echo "Jeu :             http://$HOST:$PORT/"
echo "Page admin :      http://$HOST:$PORT/panel/"
echo "Session publique: http://$HOST:$PORT/session/"
echo ""
echo "Arrêt : Ctrl+C"
echo ""

python manage.py runserver "$HOST:$PORT"
