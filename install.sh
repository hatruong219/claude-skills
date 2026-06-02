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

echo "Installing claude dotfiles from $DOTFILES"

mkdir -p ~/.claude

# Skills và Agents — available in mọi project
link "$DOTFILES/.claude/commands"  ~/.claude/commands
link "$DOTFILES/.claude/agents"    ~/.claude/agents

# Global harness: hooks, permissions — áp dụng mọi project
link "$DOTFILES/.claude/settings.json" ~/.claude/settings.json

# Global instructions — mọi project đọc, project có thể override bằng ./CLAUDE.md riêng
link "$DOTFILES/.claude/CLAUDE.md" ~/.claude/CLAUDE.md

echo "Done. Agents, skills, harness và global instructions đã được link."
echo ""
echo "Cấu trúc 2 cấp:"
echo "  Global : ~/.claude/  (từ dotfiles, dùng cho mọi project)"
echo "  Project: <project>/CLAUDE.md + <project>/.claude/settings.json (tùy chỉnh per project)"
