import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
SQLITE_DB_PATH = Path(os.getenv("SQLITE_DB_PATH", str(ROOT_DIR / "database" / "db.db")))
GRAPH_OUTPUT_PATH = Path(os.getenv("GRAPH_OUTPUT_PATH", str(ROOT_DIR / "visualization" / "graph.html")))
