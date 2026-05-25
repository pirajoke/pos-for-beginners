#!/bin/zsh
set -e

cd "$(dirname "$0")"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║       POS FOR BEGINNERS — Setup Wizard          ║"
echo "║                                                  ║"
echo "║  8 steps from zero to a working system.          ║"
echo "║  Each step builds on the previous one.           ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Drag your Obsidian vault folder here, then press Enter:"
read VAULT_PATH

if [ -z "$VAULT_PATH" ]; then
  echo "No vault path provided."
  exit 1
fi

# Remove potential quotes from drag-and-drop
VAULT_PATH=$(echo "$VAULT_PATH" | sed "s/^'//" | sed "s/'$//" | sed 's/^ //' | sed 's/ $//')

echo ""
python3 scripts/setup_pos.py --vault "$VAULT_PATH"
