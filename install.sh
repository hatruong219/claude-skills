#!/usr/bin/env bash
set -e

DOTFILES="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

link() {
  local src="$1" dst="$2"
  if [ -L "$dst" ]; then
    rm "$dst"
  elif [ -e "$dst" ]; then
    echo "  skip $dst (exists, not a symlink — move it manually)"
    return
  fi
  ln -s "$src" "$dst"
  echo "  linked $dst → $src"
}

echo "Installing claude skills from $DOTFILES"

mkdir -p ~/.claude
link "$DOTFILES/.claude/commands" ~/.claude/commands
link "$DOTFILES/.claude/agents"   ~/.claude/agents

echo "Done."
