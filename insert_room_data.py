import sqlite3

db = sqlite3.connect(
    "db.sqlite3", isolation_level=None,
)

insert_sql = """
    INSERT INTO rooms (name, hotel_id)
    VALUES
        ('シングルルーム', 1),
        ('ダブルルーム', 1),
        ('スイートルーム', 1),
        ('ツインルーム', 2),
        ('和室', 3)
"""

db.execute(insert_sql)
db.close()