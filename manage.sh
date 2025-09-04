#!/bin/bash
set -e

ACTION=$1     # first argument (up, down, status)
TARGET=$2     # optional second argument (folder name)

if [[ -z "$ACTION" ]]; then
  echo "Usage: $0 [up|down|status] [Web|PWN|Miscellenous|Forensic]"
  exit 1
fi

# List of project directories and their scripts
PROJECTS=(
  "Web:web.sh"
  "PWN:pwn.sh"
  "Miscellenous:misc.sh"
  "Forensic:forensic.sh"
)

run_project() {
  local FOLDER=$1
  local SCRIPT=$2

  echo "⚙️ Processing $FOLDER ..."

  if [[ -f "$FOLDER/$SCRIPT" ]]; then
    echo "➡️ Running custom script: $SCRIPT with action: $ACTION"
    (
      cd "$FOLDER"
      bash "$SCRIPT" "$ACTION"
    )

  elif [[ -f "$FOLDER/docker-compose.yml" || -f "$FOLDER/docker-compose.yaml" ]]; then
    echo "➡️ Running docker-compose in $FOLDER"
    (
      cd "$FOLDER"
      if [[ "$ACTION" == "up" ]]; then
        docker-compose up -d
      elif [[ "$ACTION" == "down" ]]; then
        docker-compose down --rmi all
      elif [[ "$ACTION" == "status" ]]; then
        echo "📊 Status for $FOLDER"
        docker-compose ps
        echo
      else
        echo "❌ Unknown action: $ACTION"
        exit 1
      fi
    )
  else
    echo "⚠️ No script or docker-compose found in $FOLDER"
  fi
}

for proj in "${PROJECTS[@]}"; do
  FOLDER="${proj%%:*}"    # before colon
  SCRIPT="${proj##*:}"    # after colon

  if [[ -z "$TARGET" || "$TARGET" == "$FOLDER" ]]; then
    run_project "$FOLDER" "$SCRIPT"
  fi
done

echo "✅ Done."

