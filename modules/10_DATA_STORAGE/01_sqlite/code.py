import sqlite3


with sqlite3.connect('prototype.db') as conn:
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    conn.commit()

    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Иван Иванов', 30))
    conn.commit()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    print(f"Все пользователи: {users}")

    cur.execute("UPDATE users SET age = ? WHERE name = ?", (45, 'Иван Иванов'))
    conn.commit()

    cur.execute("SELECT * FROM users")
    user = cur.fetchone()
    print(f"Пользователь: {user}")

    cur.execute("DELETE FROM users WHERE name = ?", ('Иван Иванов',))
    conn.commit()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    print(f"Все пользователи: {users}")

