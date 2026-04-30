
from pathlib import Path
import sys
from pyvis.network import Network
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import config


def get_driver():
    return GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))


def node_title(node):
    props = dict(node)
    title = "<br>".join(f"{key}: {value}" for key, value in props.items())
    return title or list(node.labels)[0]


def edge_title(rel):
    props = dict(rel)
    info = "<br>".join(f"{key}: {value}" for key, value in props.items())
    return f"{rel.type}" + (f"<br>{info}" if info else "")


def build_graph(limit=100):
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
    net.show_buttons(filter_=["physics"])
    net.force_atlas_2based()

    nodes_added = set()
    with get_driver().session() as s:
        result = s.run("MATCH (n)-[r]->(m) RETURN n, r, m LIMIT $limit", {"limit": limit})
        for row in result:
            n = row["n"]
            m = row["m"]
            r = row["r"]
            n_id = n.element_id
            m_id = m.element_id

            if n_id not in nodes_added:
                net.add_node(n_id, label=list(n.labels)[0], title=node_title(n), group=list(n.labels)[0])
                nodes_added.add(n_id)
            if m_id not in nodes_added:
                net.add_node(m_id, label=list(m.labels)[0], title=node_title(m), group=list(m.labels)[0])
                nodes_added.add(m_id)

            net.add_edge(n_id, m_id, title=edge_title(r))

        isolated = s.run("MATCH (n) WHERE NOT (n)--() RETURN n LIMIT 50")
        for row in isolated:
            n = row["n"]
            n_id = n.element_id
            if n_id not in nodes_added:
                net.add_node(n_id, label=list(n.labels)[0], title=node_title(n), group=list(n.labels)[0])
                nodes_added.add(n_id)

    output_path = Path(config.GRAPH_OUTPUT_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    net.show(str(output_path), notebook=False)
    print(f"Graph visualization saved to {output_path}")


if __name__ == "__main__":
    build_graph()
