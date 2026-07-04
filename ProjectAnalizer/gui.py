import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import sys
import os
import subprocess
from pathlib import Path

from code_merger import merge_project
from graph_builder import build_graphs
from rag_llm import simple_rag, ask_llm, generate_tests, suggest_and_improve


class ThreadLog:
    def __init__(self, q): self.q = q

    def write(self, s):
        if s.strip(): self.q.put(s)

    def flush(self): pass


class AnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Project RAG Analyzer")
        self.root.geometry("950x720")
        self.root.minsize(750, 500)

        self.log_queue = queue.Queue()
        self.running = False
        self.mcp_process = None

        self._build_ui()
        self._start_queue_listener()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Путь к проекту:").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.proj_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.proj_var, width=60).grid(row=0, column=1, padx=5, sticky=tk.EW)
        ttk.Button(top, text="Обзор", command=self._browse_dir).grid(row=0, column=2, padx=5)

        ttk.Label(top, text="Файл слияния:").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.out_var = tk.StringVar(value="merged_project.txt")
        ttk.Entry(top, textvariable=self.out_var, width=60).grid(row=1, column=1, padx=5, sticky=tk.EW)

        ttk.Label(top, text="Папка для графов:").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.graph_dir_var = tk.StringVar(value="project_graphs")
        ttk.Entry(top, textvariable=self.graph_dir_var, width=60).grid(row=2, column=1, padx=5, sticky=tk.EW)
        ttk.Button(top, text="Обзор", command=self._browse_graph_dir).grid(row=2, column=2, padx=5)

        ttk.Label(top, text="Модель LLM:").grid(row=3, column=0, sticky=tk.W, pady=4)
        self.model_var = tk.StringVar(value="qwen/qwen3.5-9b")
        ttk.Entry(top, textvariable=self.model_var, width=60).grid(row=3, column=1, padx=5, sticky=tk.EW)
        ttk.Label(top, text="(название из LM Studio)", font=("", 8), foreground="gray").grid(row=3, column=2,
                                                                                             sticky=tk.W, padx=5)

        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Запустить анализ", command=self._start_analysis).pack(side=tk.LEFT, padx=(10, 5))
        self.mcp_btn = ttk.Button(btn_frame, text="Запустить MCP-сервер", command=self._toggle_mcp)
        self.mcp_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить лог", command=self._clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Открыть папку с графами", command=self._open_graphs).pack(side=tk.LEFT,
                                                                                                padx=(5, 10))

        log_frame = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 10), bg="#f8f9fa")
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Готово к работе (запустите LM Studio перед анализом)")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=4).pack(fill=tk.X,
                                                                                                          side=tk.BOTTOM)

    def _browse_dir(self):
        path = filedialog.askdirectory()
        if path: self.proj_var.set(path)

    def _browse_graph_dir(self):
        path = filedialog.askdirectory()
        if path: self.graph_dir_var.set(path)

    def _clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _open_graphs(self):
        dir_path = os.path.abspath(self.graph_dir_var.get().strip() or "project_graphs")
        os.makedirs(dir_path, exist_ok=True)
        try:
            os.startfile(dir_path) if os.name == 'nt' else os.system(f'open "{dir_path}"')
        except:
            pass

    def _start_queue_listener(self):
        def pull_logs():
            try:
                while True:
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, self.log_queue.get_nowait() + "\n")
                    self.log_text.see(tk.END)
                    self.log_text.config(state=tk.DISABLED)
            except queue.Empty:
                pass
            self.root.after(100, pull_logs)

        self.root.after(100, pull_logs)

    def _toggle_mcp(self):
        if self.mcp_process and self.mcp_process.poll() is None:
            self.mcp_process.terminate()
            self.mcp_process = None
            self.mcp_btn.config(text="Запустить MCP-сервер")
            self.status_var.set("MCP-сервер остановлен")
            self.log_queue.put("MCP-сервер остановлен.")
        else:
            mcp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")
            if not os.path.exists(mcp_path):
                messagebox.showerror("Ошибка", "Файл mcp_server.py не найден в папке с приложением.")
                return
            self.log_queue.put("Запуск MCP-сервера (stdio)...")
            try:
                self.mcp_process = subprocess.Popen(
                    [sys.executable, mcp_path],
                    cwd=os.path.dirname(os.path.abspath(__file__)),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                self.mcp_btn.config(text="Остановить MCP-сервер")
                self.status_var.set("MCP-сервер запущен (ждёт подключений)")
                self.log_queue.put("MCP-сервер работает в фоне.")
            except Exception as e:
                self.log_queue.put(f"Ошибка запуска MCP: {e}")

    def _start_analysis(self):
        if self.running: return
        proj = self.proj_var.get().strip()
        if not proj or not os.path.isdir(proj):
            messagebox.showerror("Ошибка", "Укажите корректную папку с Python-проектом")
            return

        self.running = True
        self._clear_log()
        self.status_var.set("Выполняется анализ...")
        threading.Thread(target=self._run_pipeline, daemon=True).start()

    def _run_pipeline(self):
        old_stdout = sys.stdout
        sys.stdout = ThreadLog(self.log_queue)
        try:
            proj = self.proj_var.get().strip()
            out = self.out_var.get().strip() or "merged_project.txt"
            graph_dir = self.graph_dir_var.get().strip() or "project_graphs"
            model = self.model_var.get().strip() or "qwen/qwen3.5-9b"

            self.log_queue.put(f"Слияние кода → {out}")
            merged = merge_project(proj, output_path=out)
            if not merged:
                self.log_queue.put("Python-файлы не найдены. Прерываю.")
                return
            self.log_queue.put(f"Сохранено: {out} ({len(merged):,} символов)")

            self.log_queue.put(f"\nПостроение графов в: {graph_dir}...")
            build_graphs(merged, output_dir=graph_dir)

            self.log_queue.put(f"\nГенерация тестов (модель: {model})...")
            first_py = next((p for p in Path(proj).rglob("*.py") if "__pycache__" not in str(p)), None)
            if first_py:
                code = first_py.read_text(encoding="utf-8", errors="replace")
                test_path = generate_tests(code, str(first_py), model=model)
                if test_path and Path(test_path).exists():
                    self.log_queue.put("Запуск pytest (тайм-аут 60 сек)...")
                    try:
                        res = subprocess.run(
                            ["pytest", test_path, "-v", "--tb=short", "--maxfail=1"],
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=60
                        )
                        if "ModuleNotFoundError" in (res.stderr or ""):
                            self.log_queue.put("Тест требует внешних зависимостей. Пропускаю.")
                        elif res.returncode == 0:
                            self.log_queue.put("Все тесты пройдены!")
                            if res.stdout: self.log_queue.put(res.stdout)
                        else:
                            self.log_queue.put("Тесты завершились с ошибками:")
                            self.log_queue.put(res.stdout or res.stderr)
                    except subprocess.TimeoutExpired:
                        self.log_queue.put("Тесты выполнялись дольше 60 сек. Прервано.")
                        self.log_queue.put("Совет: проверьте тесты на бесконечные циклы или тяжёлые импорты.")
                else:
                    self.log_queue.put("Тесты не созданы.")
            else:
                self.log_queue.put("В проекте нет .py файлов.")

            self.log_queue.put(f"\nГенерация улучшений (модель: {model})...")

            chunks = merged.split("# === FILE: ")[1:]

            priority_keywords = ['main.py', 'app.py', '__init__.py', 'config.py', 'settings.py', 'core.py']
            priority_chunks = []
            other_chunks = []

            for chunk in chunks:
                if any(kw in chunk.lower() for kw in priority_keywords):
                    priority_chunks.append(chunk)
                else:
                    other_chunks.append(chunk)

            selected_chunks = priority_chunks[:5] + other_chunks[:5]

            ctx = "\n\n".join(selected_chunks)
            if len(ctx) > 50000:
                ctx = ctx[:50000] + "\n... [обрезано до 50000 символов]"

            self.log_queue.put(f"Анализирую {len(selected_chunks)} файлов ({len(ctx):,} символов)...")
            suggest_and_improve(ctx, model=model)

            self.log_queue.put("\nАнализ завершён! Графы и отчёты готовы.")
        except Exception as e:
            self.log_queue.put(f"\nКритическая ошибка: {e}")
        finally:
            sys.stdout = old_stdout
            self.running = False
            self.root.after(0, lambda: self.status_var.set("Готово к работе"))

    def _on_close(self):
        if self.mcp_process and self.mcp_process.poll() is None:
            self.mcp_process.terminate()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyzerGUI(root)
    root.mainloop()