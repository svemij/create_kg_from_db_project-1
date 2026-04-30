
import random
import sqlite3
from pathlib import Path
from faker import Faker

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.db"
fake = Faker()


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript(open(BASE_DIR / "schema.sql").read())

    for i in range(50):
        cur.execute("INSERT INTO users VALUES (?, ?, ?)", (i, fake.name(), fake.country()))

    for i in range(100):
        cur.execute("INSERT INTO products VALUES (?, ?, ?)", (i, fake.word(), random.uniform(5, 200)))

    for i in range(10):
        cur.execute("INSERT INTO categories VALUES (?, ?, ?)", (i, f"Cat{i}", None if i < 3 else random.randint(0, 2)))

    for i in range(20):
        cur.execute("INSERT INTO suppliers VALUES (?, ?)", (i, fake.company()))

    for i in range(150):
        uid = random.randint(0, 49)
        cur.execute("INSERT INTO orders VALUES (?, ?, ?)", (i, uid, fake.date()))
        for _ in range(random.randint(1, 4)):
            cur.execute(
                "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                (i, random.randint(0, 99), random.randint(1, 5)),
            )

    for i in range(200):
        cur.execute(
            "INSERT INTO reviews VALUES (?, ?, ?, ?)",
            (i, random.randint(0, 49), random.randint(0, 99), random.randint(1, 5)),
        )

    conn.commit()
    conn.close()
    print("DB ready")


if __name__ == "__main__":
    main()
