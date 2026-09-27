#!/usr/bin/env bash
# Fails if any asset under Assets/ is missing its .meta, or a .meta has no asset.
# Unity skips hidden (.name) and tilde (name~) entries, so we do too.
set -euo pipefail

readonly ASSETS_DIR="Assets"
readonly META_EXT=".meta"
missing=0
orphan=0

list_assets() {
  find "$ASSETS_DIR" -mindepth 1 \
    \( -name '.*' -o -name '*~' \) -prune -o \
    ! -name "*$META_EXT" -print
}

list_metas() {
  find "$ASSETS_DIR" -mindepth 1 \
    \( -name '.*' -o -name '*~' \) -prune -o \
    -name "*$META_EXT" -print
}

while IFS= read -r asset; do
  [[ -e "$asset$META_EXT" ]] && continue
  echo "::error file=$asset::Missing $META_EXT file (open the project in Unity and commit the generated .meta)"
  missing=$((missing + 1))
done < <(list_assets)

while IFS= read -r meta; do
  [[ -e "${meta%"$META_EXT"}" ]] && continue
  echo "::error file=$meta::Orphan $META_EXT file (asset was deleted/moved without its .meta)"
  orphan=$((orphan + 1))
done < <(list_metas)

echo "Missing metas: $missing · Orphan metas: $orphan"
[[ $missing -eq 0 && $orphan -eq 0 ]]
