import sqlite3

conn = sqlite3.connect('physics_playground.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Insert a record
cursor.execute('''INSERT INTO people (name, age) VALUES (?, ?)''', ('John', 30))

# Commit the changes
conn.commit()

# Retrieve data
cursor.execute('''SELECT * FROM people''')
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()

def use_std_db (conn):
    def decorator_use_std_db(func):
        @functools.wraps(func)
        def wrapper_use_std_db(conn, *args, **kwargs):
            conn = sqlite3.connect('physics_playground.db')

            rtn = func(*args, **kwargs)
        
            conn.close()
        return wrapper_use_std_db
    return decorator_use_std_db
