from pathlib import Path
import sys
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import config


def get_driver():
    return GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))


def recommendations(user_id, limit=5):
    query = '''
        MATCH (u:User {id:$id})-[:PLACED]->(:Order)-[:BOUGHT]->(p:Product)
        MATCH (other:User)-[:PLACED]->(:Order)-[:BOUGHT]->(p)
        MATCH (other)-[:PLACED]->(:Order)-[:BOUGHT]->(rec:Product)
        WHERE NOT (u)-[:PLACED]->(:Order)-[:BOUGHT]->(rec)
        RETURN DISTINCT rec.name AS recommendation
        LIMIT $limit
    '''
    with get_driver().session() as s:
        return [r["recommendation"] for r in s.run(query, {"id": user_id, "limit": limit})]


def top_rated_products(limit=10):
    query = '''
        MATCH (:User)-[r:REVIEWED]->(p:Product)
        WITH p, avg(r.rating) AS avgRating, count(r) AS reviews
        RETURN p.name AS name, avgRating, reviews
        ORDER BY avgRating DESC, reviews DESC
        LIMIT $limit
    '''
    with get_driver().session() as s:
        return [
            {
                "name": r["name"],
                "avg_rating": r["avgRating"],
                "reviews": r["reviews"],
            }
            for r in s.run(query, {"limit": limit})
        ]


def user_order_history(user_id):
    query = '''
        MATCH (u:User {id:$id})-[:PLACED]->(o:Order)-[:BOUGHT]->(p:Product)
        RETURN o.id AS order_id, o.date AS order_date, collect(p.name) AS products
        ORDER BY o.date DESC
    '''
    with get_driver().session() as s:
        return [
            {
                "order_id": r["order_id"],
                "order_date": r["order_date"],
                "products": r["products"],
            }
            for r in s.run(query, {"id": user_id})
        ]


def main():
    print("Recommendations for User 1:", recommendations(1))
    print("Top rated products:", top_rated_products())
    print("User 1 order history:", user_order_history(1))


if __name__ == "__main__":
    main()
