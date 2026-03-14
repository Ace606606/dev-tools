import os
import re
import sys
from typing import Dict, List, Set, Tuple


def parse_project(root_dir: str) -> Dict[str, Set[str]]:
    root_dir = os.path.abspath(root_dir)
    include_pattern = re.compile(r'#include\s+"(.+?)"')
    graph: Dict[str, Set[str]] = {}
    file_map: Dict[str, List[str]] = {}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [
            d for d in dirs if d not in {".git", "build", ".venv", "docs"}
        ]
        for file in files:
            if file.endswith((".cpp", ".hpp", ".c", ".h", ".cc")):
                abs_path = os.path.abspath(os.path.join(root, file))
                graph[abs_path] = set()
                file_map.setdefault(file, []).append(abs_path)

    for file_path in graph.keys():
        current_dir = os.path.dirname(file_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.strip().startswith("//"):
                        continue
                    match = include_pattern.search(line)
                    if not match:
                        continue

                    inc_str: str = match.group(1)
                    inc_name: str = os.path.basename(inc_str)

                    candidate = os.path.normpath(
                        os.path.join(current_dir, inc_str)
                    )
                    if candidate in graph:
                        graph[file_path].add(candidate)
                        continue

                    if inc_name in file_map:
                        found = False
                        for potential_abs in file_map[inc_name]:
                            if potential_abs.endswith(inc_str.strip("./")):
                                graph[file_path].add(potential_abs)
                                found = True
                                break
                        if not found and len(file_map[inc_name]) == 1:
                            graph[file_path].add(file_map[inc_name][0])
        except Exception:
            pass
    return graph


def generate_dot(
    graph: Dict[str, Set[str]], target_abs: str, max_depth: int
) -> str:
    impacted: Set[str] = {target_abs}
    edges: Set[Tuple[str, str]] = set()

    current_layer = {target_abs}

    for _ in range(max_depth):
        next_layer: Set[str] = set()
        for node, includes in graph.items():
            if node in impacted:
                continue

            for inc in includes:
                if inc in current_layer:
                    impacted.add(node)
                    next_layer.add(node)
                    edges.add((node, inc))
                    break

        if not next_layer:
            break
        current_layer = next_layer

    lines: List[str] = [
        "digraph G {",
        "  rankdir=BT; nodesep=0.6; ranksep=1.2;",
        '  node [shape=box, fontname="Verdana", fontsize=10, '
        'style="filled,rounded"];',
        "  edge [arrowhead=vee, arrowsize=0.8];",
    ]

    for node in impacted:
        label = "/".join(node.split(os.sep)[-2:])
        is_header = node.endswith((".hpp", ".h"))

        if node == target_abs:
            attr = (
                'fillcolor="#ffcccc", color="#cc0000", '
                'fontcolor="#8b0000", penwidth=2'
            )
        elif is_header:
            attr = 'fillcolor="#bbdefb", color="#1976d2", fontcolor="#0d47a1"'
        else:
            attr = 'fillcolor="#f5f5f5", color="#757575", fontcolor="#424242"'

        lines.append(f'  "{node}" [label="{label}", {attr}];')

    for src, dst in edges:
        if src.endswith((".hpp", ".h")) and dst.endswith((".hpp", ".h")):
            edge_attr = 'color="#1976d2", style="dashed"'
        else:
            edge_attr = 'color="#ff6600"'
        lines.append(f'  "{src}" -> "{dst}" [{edge_attr}];')

    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    root_arg: str = os.path.abspath(sys.argv[1])
    target_arg: str = sys.argv[2]
    depth_arg: int = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    full_graph = parse_project(root_arg)
    target_path = next(
        (
            p
            for p in full_graph
            if p.endswith(target_arg) or os.path.basename(p) == target_arg
        ),
        None,
    )

    if target_path:
        print(generate_dot(full_graph, target_path, depth_arg))
