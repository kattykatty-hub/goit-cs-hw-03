import os, time, random
from faker import Faker
import psycopg2
from psycopg2.extras import execute_values

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "task_manager")
DB_USER = os.getenv("DB_USER", "task_user")
DB_PASS = os.getenv("DB_PASS", "strongpassword")

fake = Faker()
statuses = ['new', 'in progress', 'completed']

def seed():
    conn = None
    # Retry loop
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            print("✅ Connected to DB!")
            break
        except psycopg2.OperationalError:
            print(f"DB not ready, retrying ({i+1}/10)...")
            time.sleep(3)
    else:
        raise Exception("Could not connect to database after 10 retries")

    with conn, conn.cursor() as cur:
        # Ensure tables exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS status (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                status_id INTEGER NOT NULL REFERENCES status(id),
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # Insert statuses
        for s in statuses:
            cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (s,))

        # Insert users
        users = [(fake.name(), fake.unique.email()) for _ in range(10)]
        execute_values(cur, "INSERT INTO users (fullname, email) VALUES %s ON CONFLICT (email) DO NOTHING;", users)

        # Get IDs
        cur.execute("SELECT id FROM users")
        user_ids = [r[0] for r in cur.fetchall()]
        cur.execute("SELECT id, name FROM status")
        status_map = {name: sid for sid, name in [(r[0], r[1]) for r in cur.fetchall()]}

        # Insert tasks
        tasks = []
        for _ in range(30):
            tasks.append((
                fake.sentence(nb_words=5),
                fake.paragraph(nb_sentences=2),
                status_map[random.choice(statuses)],
                random.choice(user_ids)
            ))

        execute_values(cur, "INSERT INTO tasks (title, description, status_id, user_id) VALUES %s;", tasks)

    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed()
    
   

