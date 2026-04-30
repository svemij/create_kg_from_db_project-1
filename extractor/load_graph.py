
from pathlib import Path
import sys
import argparse
import sqlite3
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import config

driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))

def run(tx, q, p=None):
    tx.run(q, p or {})

def create_constraints():
    with driver.session() as s:
        statements = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (o:Order) REQUIRE o.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Category) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Supplier) REQUIRE s.id IS UNIQUE",
        ]
        for stmt in statements:
            s.execute_write(run, stmt)
    print("Constraints ensured")

def clear_graph():
    with driver.session() as s:
        s.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))
    print("Existing graph cleared")

def load():
    db_path = Path(config.SQLITE_DB_PATH)
    if not db_path.exists():
        raise FileNotFoundError(f"SQLite database not found at {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    with driver.session() as s:
        for user_id, name, country in cur.execute("SELECT user_id, name, country FROM users"):
            s.execute_write(run,
                            "MERGE (u:User {id:$id}) SET u.name = $name, u.country = $country",
                            {"id": user_id, "name": name, "country": country})

        for product_id, name, price in cur.execute("SELECT product_id, name, price FROM products"):
            s.execute_write(run,
                            "MERGE (p:Product {id:$id}) SET p.name = $name, p.price = $price",
                            {"id": product_id, "name": name, "price": price})

        for order_id, user_id, order_date in cur.execute("SELECT order_id, user_id, order_date FROM orders"):
            s.execute_write(run,
                            "MERGE (o:Order {id:$id}) SET o.date = $date",
                            {"id": order_id, "date": order_date})

        for user_id, order_id in cur.execute("SELECT user_id, order_id FROM orders"):
            s.execute_write(run,
                            "MATCH (u:User {id:$user_id}), (o:Order {id:$order_id}) MERGE (u)-[:PLACED]->(o)",
                            {"user_id": user_id, "order_id": order_id})

        for order_id, product_id, quantity in cur.execute("SELECT order_id, product_id, quantity FROM order_items"):
            s.execute_write(run,
                            "MATCH (o:Order {id:$order_id}), (p:Product {id:$product_id}) MERGE (o)-[:BOUGHT {quantity:$quantity}]->(p)",
                            {"order_id": order_id, "product_id": product_id, "quantity": quantity})

        for user_id, product_id, rating in cur.execute("SELECT user_id, product_id, rating FROM reviews"):
            s.execute_write(run,
                            "MATCH (u:User {id:$user_id}), (p:Product {id:$product_id}) MERGE (u)-[:REVIEWED {rating:$rating}]->(p)",
                            {"user_id": user_id, "product_id": product_id, "rating": rating})

        for category_id, name, parent_id in cur.execute("SELECT category_id, name, parent_id FROM categories"):
            s.execute_write(run,
                            "MERGE (c:Category {id:$id}) SET c.name = $name, c.parent_id = $parent",
                            {"id": category_id, "name": name, "parent": parent_id})

        for supplier_id, name in cur.execute("SELECT supplier_id, name FROM suppliers"):
            s.execute_write(run,
                            "MERGE (s:Supplier {id:$id}) SET s.name = $name",
                            {"id": supplier_id, "name": name})

    conn.close()
    print("Graph loaded")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load SQLite data into Neo4j")
    parser.add_argument("--clean", action="store_true", help="Clear existing graph before loading")
    args = parser.parse_args()

    create_constraints()
    if args.clean:
        clear_graph()
    load()
