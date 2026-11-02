"""Generate a deterministic repository inventory; never infer feature completion."""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "document" / "INVENTORY.md"
EXCLUDED = {
    ".git", ".venv", "venv", "env", "ENV", "__pycache__", "node_modules",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".nox", ".idea",
    ".vscode", ".vs", ".codex", ".agents", ".aws", "build", "dist",
    "htmlcov", "uploads", "exports", ".npm", ".vite", ".parcel-cache",
    ".hypothesis", ".eggs", ".pyre", ".ipynb_checkpoints",
}
RUNTIME = {"instance", "logs", "backups"}


def visible(path):
    parts = path.relative_to(ROOT).parts
    if any(part in EXCLUDED or part.endswith(".egg-info") for part in parts):
        return False
    if parts[0] in RUNTIME:
        return path.name == ".gitkeep"
    name = path.name.lower()
    if name.startswith(".env") and not name.endswith(".example"):
        return False
    if any(marker in name for marker in (".sqlite", ".db-")):
        return False
    if name.endswith((".db", ".pyc", ".pyo", ".log", ".pem", ".key", ".p12", ".pfx", ".bak", ".backup", ".dump", ".tmp", ".temp")):
        return False
    if name == "credentials.json" or name.startswith("service-account"):
        return False
    return True


def collect(directory):
    # Prune ignored directories before traversing, including local runtime data.
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        if path.is_symlink():
            continue
        if path.is_dir():
            if path.name not in EXCLUDED and not path.name.endswith(".egg-info"):
                if path.parent == ROOT and path.name in RUNTIME:
                    marker = path / ".gitkeep"
                    if marker.is_file():
                        yield marker
                else:
                    yield from collect(path)
        elif visible(path):
            yield path


def render():
    files = {path.relative_to(ROOT).as_posix() for path in collect(ROOT)}
    files.add(OUTPUT.relative_to(ROOT).as_posix())
    lines = [
        "# Danh mục file tự sinh", "",
        "Sinh bằng `python scripts/update_docs.py`. Không sửa tay.", "",
        "Danh mục file không phải danh sách chức năng hoàn thành. Xem [STATUS.md](STATUS.md).",
        "Không liệt kê môi trường ảo, dữ liệu runtime và các nhóm file nhạy cảm phổ biến.",
        "Script chỉ ghi đường dẫn, không đọc nội dung file; không thay thế kiểm tra secrets.", "",
        "```text", *sorted(files), "```", "",
        f"Tổng: {len(files)} file (bao gồm file danh mục này).", "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if inventory is stale; write nothing")
    args = parser.parse_args()
    expected = render()
    actual = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if args.check:
        if actual != expected:
            print("Inventory is stale. Run: python scripts/update_docs.py")
            return 1
        print("Inventory is up to date.")
        return 0
    if actual != expected:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        with OUTPUT.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(expected)
    print("Updated document/INVENTORY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
