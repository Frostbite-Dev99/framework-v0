"""Enforces the framework layer rules (Docs/01-csharp-best-practices.md §13) on every framework asmdef.

Core -> nothing in UIX/Logic · UIX <-/-> Logic · _Framework never -> Game.
Resolves "GUID:" references (Unity's default when editing asmdefs in the Inspector).
"""
import json
import re
import sys
from pathlib import Path

ASSETS_DIR = Path("Assets")
FRAMEWORK_DIR = ASSETS_DIR / "_Framework"
GUID_PREFIX = "GUID:"
META_GUID_PATTERN = re.compile(r"^guid:\s*([0-9a-f]+)", re.MULTILINE)
GAME_PREFIX = "Game."

# layer -> reference prefixes that layer must never use
FORBIDDEN_BY_LAYER: dict[str, tuple[str, ...]] = {
    "Core": ("FW.UIX.", "FW.Logic.", GAME_PREFIX),
    "UIX": ("FW.Logic.", GAME_PREFIX),
    "Logic": ("FW.UIX.", GAME_PREFIX),
}


def load_asmdef_name(path: Path) -> str:
    return json.loads(path.read_text(encoding="utf-8-sig"))["name"]


def build_guid_index() -> dict[str, str]:
    index: dict[str, str] = {}
    for meta in ASSETS_DIR.rglob("*.asmdef.meta"):
        match = META_GUID_PATTERN.search(meta.read_text(encoding="utf-8"))
        if not match:
            continue
        index[match.group(1)] = load_asmdef_name(meta.with_suffix(""))
    return index


def resolve_reference(reference: str, guid_index: dict[str, str]) -> str:
    if not reference.startswith(GUID_PREFIX):
        return reference
    guid = reference[len(GUID_PREFIX):]
    return guid_index.get(guid, reference)


def find_violations(asmdef: Path, guid_index: dict[str, str]) -> list[str]:
    layer = asmdef.relative_to(FRAMEWORK_DIR).parts[0]
    forbidden = FORBIDDEN_BY_LAYER.get(layer)
    if forbidden is None:
        return [f"{asmdef}: unknown layer '{layer}' (expected {', '.join(FORBIDDEN_BY_LAYER)})"]

    data = json.loads(asmdef.read_text(encoding="utf-8-sig"))
    references = [resolve_reference(ref, guid_index) for ref in data.get("references", [])]
    return [
        f"{asmdef}: layer '{layer}' must not reference '{ref}'"
        for ref in references
        if ref.startswith(forbidden)
    ]


def main() -> int:
    guid_index = build_guid_index()
    asmdefs = sorted(FRAMEWORK_DIR.rglob("*.asmdef"))
    violations = [v for asmdef in asmdefs for v in find_violations(asmdef, guid_index)]

    for violation in violations:
        print(f"::error::{violation}")
    print(f"Checked {len(asmdefs)} asmdefs · {len(violations)} violation(s)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
