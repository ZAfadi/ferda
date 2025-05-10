import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create a users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and 'users' table created successfully.")
