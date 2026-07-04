from pathlib import Path

IGNORE_DIRS = {".venv", "venv", "env", "__pycache__", ".git", "node_modules", "site-packages"}


def merge_project(root_dir: str, output_path: str = "merged_project.txt") -> str:
    merged = []
    root = Path(root_dir).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Папка не найдена: {root}")

    print(f"Сканирование: {root}...")

    for py_file in root.rglob("*.py"):
        if any(part in IGNORE_DIRS for part in py_file.parts):
            continue

        try:
            content = py_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                content = py_file.read_text(encoding="cp1251")
            except UnicodeDecodeError:
                content = py_file.read_text(encoding="utf-8", errors="replace")
        merged.append(f"# === FILE: {py_file.relative_to(root)} ===\n{content}\n")

    if not merged:
        print("Python-файлы не найдены (проверьте, не попали ли они в игнорируемые папки).")
        return ""

    full_text = "\n\n".join(merged)
    Path(output_path).write_text(full_text, encoding="utf-8")
    print(f"Собрано {len(merged)} файлов вашего проекта.")
    return full_text