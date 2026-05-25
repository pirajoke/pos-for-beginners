#!/bin/bash
# POS FOR BEGINNERS — One-line installer
# Usage: curl -fsSL https://raw.githubusercontent.com/pirajoke/pos-for-beginners/main/install.sh | bash
set -e

REPO="https://github.com/pirajoke/pos-for-beginners.git"
DIR="$HOME/pos-for-beginners"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║       POS FOR BEGINNERS — Installer              ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── Check dependencies ──────────────────────────────────
check() {
  if ! command -v "$1" &>/dev/null; then
    echo "✗ $1 not found."
    return 1
  fi
  echo "✓ $1 found: $(command -v "$1")"
  return 0
}

missing=0

if ! check python3; then
  echo ""
  echo "  Python 3 is required."
  echo "  macOS:   xcode-select --install"
  echo "  Ubuntu:  sudo apt install python3"
  echo "  Windows: https://python.org/downloads"
  missing=1
fi

if ! check git; then
  echo ""
  echo "  Git is required."
  echo "  macOS:   xcode-select --install"
  echo "  Ubuntu:  sudo apt install git"
  echo "  Windows: https://git-scm.com"
  missing=1
fi

if [ "$missing" -eq 1 ]; then
  echo ""
  echo "Install the missing tools above, then re-run this script."
  exit 1
fi

# ── Clone or update ─────────────────────────────────────
if [ -d "$DIR/.git" ]; then
  echo ""
  echo "Updating existing installation..."
  git -C "$DIR" pull --ff-only 2>/dev/null || true
else
  echo ""
  echo "Downloading POS FOR BEGINNERS..."
  git clone --depth 1 "$REPO" "$DIR"
fi

# ── Detect vault path ───────────────────────────────────
VAULT=""

# Check common Obsidian locations
for candidate in \
  "$HOME/ObsidianVault" \
  "$HOME/Documents/ObsidianVault" \
  "$HOME/Documents/Obsidian Vault" \
  "$HOME/Obsidian" \
  "$HOME/Documents/Obsidian"; do
  if [ -d "$candidate/.obsidian" ]; then
    VAULT="$candidate"
    break
  fi
done

if [ -n "$VAULT" ]; then
  echo ""
  echo "Found Obsidian vault: $VAULT"
  printf "Use this vault? [Y/n]: "
  read -r yn
  case "$yn" in
    [nN]*) VAULT="" ;;
  esac
fi

if [ -z "$VAULT" ]; then
  echo ""
  echo "Drag your Obsidian vault folder here (or type a path):"
  printf "→ "
  read -r VAULT
  # Clean drag-and-drop artifacts
  VAULT=$(echo "$VAULT" | sed "s/^'//" | sed "s/'$//" | sed 's/^ //' | sed 's/\\ / /g' | sed 's/ $//')
fi

if [ -z "$VAULT" ]; then
  echo "No vault path provided. Using: ~/ObsidianVault"
  VAULT="$HOME/ObsidianVault"
fi

# ── Run wizard ──────────────────────────────────────────
echo ""
cd "$DIR"
python3 scripts/setup_pos.py --vault "$VAULT"
