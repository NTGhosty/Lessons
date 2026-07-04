import ast
import os
import networkx as nx
from pyvis.network import Network

def _trim_graph(G, max_nodes=120):
    if len(G.nodes) <= max_nodes: return G
    degrees = dict(G.degree())
    top = sorted(degrees, key=degrees.get, reverse=True)[:max_nodes]
    return G.subgraph(top).copy()

def build_graphs(merged_text: str, output_dir: str = "project_graphs"):
    os.makedirs(output_dir, exist_ok=True)
    files = merged_text.split("# === FILE: ")[1:]
    m_nodes, m_edges = set(), []
    c_nodes, c_edges = set(), []
    f_nodes, f_edges = set(), []

    for block in files:
        lines = block.split("\n")
        filepath = lines[0].strip()
        code = "\n".join(lines[1:])
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                targets = [a.name for a in node.names] if isinstance(node, ast.Import) else ([node.module] if node.module else [])
                m_nodes.update(targets)
                m_edges.extend((filepath, t) for t in targets)
            if isinstance(node, ast.ClassDef):
                c_nodes.add(f"{filepath}:{node.name}")
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        c_edges.append((f"{filepath}:{node.name}", base.id))
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                f_nodes.add(f"{filepath}:{node.name}")
                for call in ast.walk(node):
                    if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
                        f_edges.append((f"{filepath}:{node.name}", call.func.id))

    def save(name, nodes, edges):
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        G.remove_edges_from(nx.selfloop_edges(G))
        G = _trim_graph(G)
        if not G.nodes: return

        net = Network(height="500px", width="100%", directed=True, notebook=False)
        net.from_nx(G)
        net.set_options('{"physics": {"enabled": false}, "interaction": {"hover": true, "tooltipDelay": 200}}')
        out_path = os.path.join(output_dir, f"{name}_graph.html")
        net.show(out_path, notebook=False)
        print(f"{os.path.basename(out_path)}")

    save("modules", m_nodes, m_edges)
    save("classes", c_nodes, c_edges)
    save("functions", f_nodes, f_edges)
    print(f"Все графы сохранены в: {os.path.abspath(output_dir)}")