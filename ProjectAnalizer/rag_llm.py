import requests
import ast
import re
from pathlib import Path


def ask_llm(prompt: str, model: str = "local-model", system: str = "Ты эксперт по Python. Отвечай чётко.",
            timeout: int = 120, max_tokens: int = 4096) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens,
        "stream": False
    }

    try:
        resp = requests.post("http://localhost:1234/v1/chat/completions", json=payload, timeout=timeout)

        if resp.status_code != 200:
            try:
                err = resp.json()
                return f"LLM_ERROR {resp.status_code}: {err.get('error', {}).get('message', resp.text[:200])}"
            except:
                return f"LLM_ERROR {resp.status_code}: {resp.text[:300]}"

        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()

        finish_reason = data["choices"][0].get("finish_reason", "")
        if finish_reason == "length":
            print("Ответ обрезан по лимиту токенов. Попробуйте разбить запрос.")
            content += "\n\n[ОТВЕТ ОБРЕЗАН: модель достигла лимита max_tokens]"

        return content

    except requests.exceptions.ConnectionError:
        return "LLM_ERROR: Не удалось подключиться к LM Studio. Убедитесь, что сервер запущен на порту 1234."
    except requests.exceptions.Timeout:
        return "LLM_TIMEOUT"
    except Exception as e:
        return f"LLM_ERROR: {type(e).__name__} - {e}"


def simple_rag(merged_text: str, query: str) -> str:
    chunks = merged_text.split("# === FILE: ")[1:]
    if not chunks: return ""
    query_words = set(query.lower().split())
    scored = [(sum(1 for w in query_words if w in chunk.lower()), chunk) for chunk in chunks]
    scored = [(s, c) for s, c in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return "\n\n".join([c for _, c in scored[:2]]) if scored else chunks[0][:2500]


def generate_tests(module_code: str, module_path: str, model: str = "local-model"):
    if not module_code.strip(): return None
    prompt = f"Напиши pytest-тесты для этого кода. ТОЛЬКО pytest и стандартная библиотека. Верни код в ```python.\n\nКод:\n{module_code}"
    response = ask_llm(prompt, model=model, timeout=120, max_tokens=2048)

    if "LLM_ERROR" in response or "LLM_TIMEOUT" in response:
        print(f"Ошибка LLM: {response}")
        code = "import pytest\n\ndef test_stub():\n    assert True\n"
    else:
        code = re.sub(r"^```(?:python)?\s*", "", response.strip())
        code = re.sub(r"\s*```$", "", code).strip()
        try:
            if not code or not any(k in code for k in ["def test_", "import pytest", "assert"]):
                raise SyntaxError("Нет структуры теста")
            ast.parse(code)
        except SyntaxError:
            print("Невалидный код теста. Создаю заглушку.")
            code = "import pytest\n\ndef test_stub():\n    assert True\n"

    test_path = "tests/test_" + Path(module_path).name
    Path("tests").mkdir(exist_ok=True)
    Path(test_path).write_text(code, encoding="utf-8")
    print(f"Тесты: {test_path}")
    return test_path


def suggest_and_improve(project_context: str, model: str = "local-model"):
    if not project_context.strip():
        print("Контекст пуст.")
        return

    safe_context = project_context[:12000] + "\n... [обрезано]"

    prompt = f"""Ты Senior Python Developer. Проанализируй код и предложи улучшения.

ТРЕБОВАНИЯ К ОТВЕТУ:
1. Если предлагаешь изменить файл — верни ПОЛНЫЙ код файла, а не фрагмент.
2. Если файл очень большой — можно вернуть только изменённые функции, но с комментарием "# ... остальной код без изменений" в нужных местах.
3. Формат строго:
### FILE: путь/к/файлу.py
```python
# полный код здесь
4. Если улучшений нет — напиши только: "Нет предложений".

Код проекта для анализа:
{safe_context}"""
    response = ask_llm(
        prompt,
        model=model,
        system="Ты Senior Python Architect. Давай развёрнутые, детальные ответы с кодом.",
        timeout=300,
        max_tokens=16384
    )

    if "LLM_ERROR" in response:
        print(f"{response}")
        print("Проверьте в LM Studio: модель загружена, имя точное, сервер запущен")
        return
    if "LLM_TIMEOUT" in response:
        print("Тайм-аут. Попробуйте более лёгкую модель или уменьшите контекст.")
        return
    if "Нет предложений" in response or not response.strip():
        print("LLM: Нет предложений")
        return

    print(f"LLM ответила ({len(response):,} символов), разбираю...")

    # Парсер
    files = {}
    current_file, current_code, in_block = None, [], False
    for line in response.split("\n"):
        if line.startswith("### FILE:"):
            if current_file and current_code: files[current_file] = "\n".join(current_code)
            current_file = line.split(":", 1)[1].strip();
            current_code = []
            continue
        if "```python" in line: in_block = True; continue
        if "```" in line and in_block:
            if current_file and current_code: files[current_file] = "\n".join(current_code)
            current_file, in_block = None, False
            continue
        if in_block and current_file: current_code.append(line)
    if current_file and current_code: files[current_file] = "\n".join(current_code)

    out_dir = Path("suggested_improvements")
    out_dir.mkdir(exist_ok=True)

    if not files:
        (out_dir / "llm_response.txt").write_text(response, encoding="utf-8")
        print(f"Ответ сохранён в suggested_improvements/llm_response.txt")
    else:
        for path, code in files.items():
            try:
                save_path = out_dir / path
                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_text(code, encoding="utf-8")
                lines = len(code.splitlines())
                print(f"saved_improvements/{path} ({lines} строк)")
            except Exception as e:
                print(f"Ошибка сохранения {path}: {e}")