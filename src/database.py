import sqlite3
import os
import cv2
import numpy as np

DB_FILE = 'database.sqlite'
# Directory to securely store the reference images
DB_IMAGES_DIR = 'database_records'

def setup_db():
    if not os.path.exists(DB_IMAGES_DIR):
        os.makedirs(DB_IMAGES_DIR)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            signature_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(name, image):
    setup_db()
    # Sanitize name to prevent file-system issues
    safe_name = "".join([c for c in name if c.isalpha() or c.isdigit()]).rstrip()
    if not safe_name:
        return False, "Invalid name."
        
    path = os.path.join(DB_IMAGES_DIR, f"{safe_name}.png")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, signature_path) VALUES (?, ?)", (name, path))
        conn.commit()
        conn.close()
        
        # Write to disk securely within DB image dir
        cv2.imwrite(path, image)
        return True, f"User '{name}' registered successfully."
    except sqlite3.IntegrityError:
        return False, "A user with this name already exists in the database."
    except Exception as e:
        return False, str(e)

def get_user_signature(name):
    # Retrieve the image in cv2 format given a user's name
    setup_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT signature_path FROM users WHERE name=?", (name,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        path = row[0]
        if os.path.exists(path):
            img = cv2.imread(path)
            return img
    return None

def get_all_users():
    setup_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]
