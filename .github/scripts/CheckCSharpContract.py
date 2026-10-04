"""Enforces the text-checkable rules of Docs/01-csharp-best-practices.md (see §16) on framework and game C# files.

One type per file named after the file · namespace under the asmdef rootNamespace · no empty catch ·
no UnityEditor in Runtime/ without #if UNITY_EDITOR · file length cap. Judgment rules are left to review.
"""
import json
import re
import sys
from pathlib import Path

ASSETS_DIR = Path("Assets")
CHECKED_DIRS = (ASSETS_DIR / "_Framework", ASSETS_DIR / "_Game")
MAX_FILE_LINES = 300
RUNTIME_DIR = "Runtime"
EDITOR_NAMESPACE = "UnityEditor"
EDITOR_GUARD = "#if UNITY_EDITOR"
NAMESPACE_KEYWORD = "namespace"
# "where T : class\n where U" would otherwise read as a type named "where"
CONSTRAINT_KEYWORD = "where"

COMMENT_OR_STRING = re.compile(r'//[^\n]*|/\*.*?\*/|@"(?:[^"]|"")*"|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'', re.DOTALL)
EMPTY_CATCH = re.compile(r"\bcatch\b\s*(?:\([^)]*\))?\s*(?:when\s*\([^)]*\))?\s*\{\s*\}")
DECLARATION_OR_BRACE = re.compile(r"\b(namespace|class|struct|interface|enum|record)\s+([A-Za-z_][\w.]*)|[{};]")


def strip_comments_and_strings(source: str) -> str:
    def blank(match: re.Match[str]) -> str:
        text = match.group()
        return "\n" * text.count("\n") if text.startswith("/") else '""'

    return COMMENT_OR_STRING.sub(blank, source)


def line_of(code: str, index: int) -> int:
    return code.count("\n", 0, index) + 1


def scan_declarations(code: str) -> list[tuple[str, str, bool]]:
    """Returns (kind, name, is_top_level) per declaration; top level = only namespace blocks enclose it."""
    declarations: list[tuple[str, str, bool]] = []
    open_blocks: list[str] = []
    pending_kind = ""
    for match in DECLARATION_OR_BRACE.finditer(code):
        kind, name = match.group(1), match.group(2)
        if kind and name != CONSTRAINT_KEYWORD:
            declarations.append((kind, name, all(block == NAMESPACE_KEYWORD for block in open_blocks)))
            pending_kind = kind
        elif match.group() == "{":
            open_blocks.append(pending_kind)
            pending_kind = ""
        elif match.group() == "}" and open_blocks:
            open_blocks.pop()
        elif match.group() == ";":
            pending_kind = ""
    return declarations


def find_root_namespace(path: Path) -> str:
    for folder in path.parents:
        asmdef = next(folder.glob("*.asmdef"), None)
        if asmdef:
            return json.loads(asmdef.read_text(encoding="utf-8-sig")).get("rootNamespace", "")
        if folder == ASSETS_DIR:
            return ""
    return ""


def find_type_violations(path: Path, top_level_types: list[str]) -> list[str]:
    if len(top_level_types) > 1:
        return [f"{path}: one type per file, found {', '.join(top_level_types)}. Move the extras to their own files"]
    if top_level_types and top_level_types[0] != path.stem:
        return [f"{path}: type '{top_level_types[0]}' must live in '{top_level_types[0]}.cs'"]
    return []


def find_namespace_violations(path: Path, namespaces: list[str]) -> list[str]:
    root = find_root_namespace(path)
    if not root:
        return []
    if not namespaces:
        return [f"{path}: missing namespace, expected '{root}'"]
    if namespaces[0] == root or namespaces[0].startswith(f"{root}."):
        return []
    return [f"{path}: namespace '{namespaces[0]}' must be '{root}' or start with '{root}.'"]


def find_empty_catches(path: Path, code: str) -> list[str]:
    return [
        f"{path}:{line_of(code, match.start())}: empty catch swallows the error. Log or rethrow it"
        for match in EMPTY_CATCH.finditer(code)
    ]


def find_editor_violations(path: Path, code: str, source: str) -> list[str]:
    if RUNTIME_DIR not in path.parts or EDITOR_NAMESPACE not in code or EDITOR_GUARD in source:
        return []
    return [f"{path}: uses {EDITOR_NAMESPACE} in {RUNTIME_DIR}/ without {EDITOR_GUARD}. Move it to Editor/ or guard it"]


def find_length_violations(path: Path, source: str) -> list[str]:
    line_count = len(source.splitlines())
    if line_count <= MAX_FILE_LINES:
        return []
    return [f"{path}: {line_count} lines (max {MAX_FILE_LINES}). Split it"]


def check_file(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8-sig")
    code = strip_comments_and_strings(source)
    declarations = scan_declarations(code)
    namespaces = [name for kind, name, _ in declarations if kind == NAMESPACE_KEYWORD]
    top_level_types = [name for kind, name, is_top in declarations if kind != NAMESPACE_KEYWORD and is_top]
    return [
        *find_type_violations(path, top_level_types),
        *find_namespace_violations(path, namespaces),
        *find_empty_catches(path, code),
        *find_editor_violations(path, code, source),
        *find_length_violations(path, source),
    ]


def main() -> int:
    files = sorted(file for folder in CHECKED_DIRS for file in folder.rglob("*.cs"))
    violations = [v for file in files for v in check_file(file)]

    for violation in violations:
        print(f"::error::{violation}")
    print(f"Checked {len(files)} C# files · {len(violations)} violation(s)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
