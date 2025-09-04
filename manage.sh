#!/bin/bash
set -e

ACTION=$1   # first argument (up or down)

if [[ -z "$ACTION" ]]; then
  echo "Usage: $0 [up|down]"
  exit 1
fi

# Array of project scripts
SCRIPTS=(
  "PWN/pwn.sh"
  "Miscellenous/misc.sh"
  "Forensic/forensic.sh"
)

for script in "${SCRIPTS[@]}"; do
  if [[ -f "$script" ]]; then
    echo "⚙️ Running $script $ACTION ..."
    bash "$script" "$ACTION"
  else
    echo "❌ Script not found: $script"
  fi
done

echo "✅ All done."

