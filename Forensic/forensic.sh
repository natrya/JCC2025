#!/bin/bash
set -e

ACTION=$1   # first argument (up or down)

if [[ -z "$ACTION" ]]; then
  echo "Usage: $0 [up|down]"
  exit 1
fi

# List of projects you want to manage
PROJECTS=("forensic-easy" "forensic-medium")

for proj in "${PROJECTS[@]}"; do
  if [[ -d "$proj" ]]; then
    if [[ -f "$proj/docker-compose.yml" || -f "$proj/docker-compose.yaml" ]]; then
      echo "⚙️ Processing $proj ..."
      (
        cd "$proj"
        if [[ "$ACTION" == "up" ]]; then
          docker-compose up -d
        elif [[ "$ACTION" == "down" ]]; then
          docker-compose down --rmi all
        else
          echo "❌ Unknown action: $ACTION"
          exit 1
        fi
      )
    else
      echo "⚠️ No docker-compose file found in $proj"
    fi
  else
    echo "⚠️ Directory $proj does not exist"
  fi
done

echo "✅ Done."

