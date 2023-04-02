import sqlite3

def create_db():
    conn = sqlite3.connect('../DB/database.db')
    cursor = conn.cursor()

    # Создаем таблицу accounts
    cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    wallet_address TEXT,
                    twitter TEXT,
                    discord TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    extra_info TEXT,
                    field1 TEXT,
                    field2 TEXT,
                    field3 TEXT
                    )""")

    # Создаем таблицу projects
    cursor.execute("""CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    deadline DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    field1 TEXT,
                    field2 TEXT,
                    field3 TEXT
                    )""")

    # Создаем таблицу activities
    cursor.execute("""CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    field1 TEXT,
                    field2 TEXT,
                    field3 TEXT,
                    project_id INTEGER,
                    FOREIGN KEY(project_id) REFERENCES projects(id)
                    )""")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()
