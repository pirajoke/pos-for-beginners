#!/bin/zsh
set -e

cd "$(dirname "$0")"

echo "POS FOR BEGINNERS installer"
echo ""
echo "Drag the target Obsidian vault folder here, then press Enter:"
read VAULT_PATH

if [ -z "$VAULT_PATH" ]; then
  echo "No vault path provided."
  exit 1
fi

echo ""
echo "Optional: drag a folder containing approved Notion/Mail/Granola/Crisp source exports, or press Enter to skip:"
read SOURCE_PATH

ARGS=(scripts/bootstrap_client.py --vault "$VAULT_PATH")

if [ -n "$SOURCE_PATH" ]; then
  ARGS+=(--scan-path "$SOURCE_PATH")
fi

python3 "${ARGS[@]}"

echo ""
echo "Done. Open START HERE - POS FOR BEGINNERS Setup.md in Obsidian."
