from code_merger import merge_project
from graph_builder import build_graphs
from rag_llm import simple_rag, ask_llm, generate_tests, suggest_and_improve
import subprocess
from pathlib import Path

def main():
    project_dir = input("Путь к Python-проекту: ").strip()
    print("Слияние кода...")
    merged = merge_project(project_dir)
    if not merged:
        print("Python-файлы не найдены.")
        return

    print("Построение графов...")
    build_graphs(merged)

    query = input("Запрос к проекту (или Enter для пропуска): ").strip()
    if query:
        print("RAG-поиск...")
        context = simple_rag(merged, query)
        print("Ответ LLM:")
        print(ask_llm(f"Контекст проекта:\n{context[:3000]}\n\nВопрос: {query}"))

    print("Генерация тестов...")
    first_py = next((p for p in Path(project_dir).rglob("*.py") if "__pycache__" not in str(p)), None)
    if first_py:
        code = first_py.read_text(encoding="utf-8", errors="replace")
        test_path = generate_tests(code, str(first_py))
        if test_path and Path(test_path).exists():
            print("Запуск тестов...")
            try:
                res = subprocess.run(["pytest", test_path, "-v", "--tb=short"],
                                     capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
                if "ModuleNotFoundError" in (res.stderr or ""):
                    print("Нет зависимостей для теста. Игнорирую.")
                else:
                    print("Результаты:\n", res.stdout or res.stderr or "Пусто.")
            except Exception as e:
                print(f"Тесты не запущены: {e}")

    print("Генерация улучшений...")
    chunks = merged.split("# === FILE: ")[1:]
    ctx = "\n\n".join(chunks[:2]) if len(chunks) >= 2 else merged[:4000]
    try:
        suggest_and_improve(ctx)
    except Exception as e:
        print(f"Ошибка при генерации улучшений: {e}")

    print("Готово! Графы в `*_graph.html`")

if __name__ == "__main__":
    main()