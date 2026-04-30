from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
commands = [
    [sys.executable, str(ROOT / "database" / "seed.py")],
    [sys.executable, str(ROOT / "extractor" / "load_graph.py")],
    [sys.executable, str(ROOT / "visualization" / "graph_vis.py")],
]

if __name__ == "__main__":
    for command in commands:
        print("Running:", " ".join(command))
        result = subprocess.run(command)
        if result.returncode != 0:
            print(f"Command failed with exit code {result.returncode}")
            sys.exit(result.returncode)
    print("Pipeline complete. Open:", ROOT / "visualization" / "graph.html")
