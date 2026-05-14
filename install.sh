#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Installation de FATE_95 ==="

# Vérifier Python 3
if ! command -v python3 &>/dev/null; then
    echo "ERREUR : python3 n'est pas installé."
    exit 1
fi

PYTHON=$(command -v python3)
echo "Python trouvé : $($PYTHON --version)"

# Créer le virtualenv s'il n'existe pas
if [ ! -d "venv" ]; then
    echo ""
    echo "Création du virtualenv..."
    $PYTHON -m venv venv
fi

# Activer le venv
source venv/bin/activate

echo ""
echo "Installation des dépendances..."
pip install --upgrade pip --quiet
pip install django==5.2 --quiet
echo ""
echo "Installation de sentence-transformers (MiniLM pour le KNN des conseils)..."
echo "⚠  Le modèle (~500 Mo) sera téléchargé au premier lancement du chatbot."
pip install sentence-transformers --quiet

echo ""
echo "Application des migrations..."
python manage.py migrate

echo ""
echo "Collecte des fichiers statiques (optionnel)..."
python manage.py collectstatic --noinput --clear 2>/dev/null || true

echo ""
echo "=== Installation terminée ! ==="
echo ""
echo "Pour lancer le projet :  ./launch.sh"
echo "Page admin :             http://127.0.0.1:8000/panel/"
echo "Session publique :       http://127.0.0.1:8000/session/"
