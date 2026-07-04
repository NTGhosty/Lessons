from mcp.server.fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("python-project-mcp")

@mcp.tool()
def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

@mcp.tool()
def write_file(path: str, content: str) -> str:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")
    return f"Файл {path} сохранён."

@mcp.tool()
def run_tests(test_path: str = "tests/") -> str:
    import subprocess
    res = subprocess.run(["pytest", test_path, "-v", "--tb=short"], capture_output=True, text=True)
    return f"STDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"

if __name__ == "__main__":
    print("Запуск MCP-сервера (stdio)...")
    mcp.run()