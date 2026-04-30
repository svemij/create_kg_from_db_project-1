
CREATE TABLE users (user_id INTEGER PRIMARY KEY, name TEXT, country TEXT);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT, price REAL);
CREATE TABLE categories (category_id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER);
CREATE TABLE suppliers (supplier_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, user_id INTEGER, order_date TEXT);
CREATE TABLE order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, product_id INTEGER, quantity INTEGER);
CREATE TABLE reviews (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, rating INTEGER);
