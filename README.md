
# Advanced Knowledge Graph Project

## Features
- Multi-entity graph loaded from SQLite into Neo4j
- Unique node constraints and id-based merge logic
- Recommendation and analytics queries
- Interactive visualization with PyVis

## Prerequisites
- Python 3.10+ installed
- Neo4j running locally on `bolt://localhost:7687`
- Neo4j credentials available as environment variables or defaults

## Configure
The project supports these environment variables:
- `NEO4J_URI` (default: `bolt://localhost:7687`)
- `NEO4J_USER` (default: `neo4j`)
- `NEO4J_PASSWORD` (default: `password`)
- `SQLITE_DB_PATH` (default: `database/db.db`)
- `GRAPH_OUTPUT_PATH` (default: `visualization/graph.html`)

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the pipeline
```powershell
cd database
python seed.py
cd ../extractor
python load_graph.py
cd ../queries
python queries.py
cd ../visualization
python graph_vis.py
```

### Clean load
To clear Neo4j before loading data:
```powershell
cd extractor
python load_graph.py --clean
```

### One-step pipeline
From the project root:
```powershell
python run_all.py
```

## Neo4j Browser
Open `http://localhost:7474` and run:
```cypher
MATCH (n)-[r]->(m)
RETURN n,r,m
LIMIT 100
```

## Notes
- `load_graph.py` now creates Neo4j uniqueness constraints before loading.
- `graph_vis.py` exports `visualization/graph.html` with node metadata and physics controls.
- `.gitignore` excludes the virtual environment, SQLite DB file, and generated HTML output.
