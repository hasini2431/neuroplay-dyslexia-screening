import sqlite3
import bcrypt


DATABASE = "users.db"


# ============================================================
# CREATE / UPDATE DATABASE
# ============================================================

def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Create the original table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    # Add new columns if they don't already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if "gender" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN gender TEXT DEFAULT 'Female'"
        )

    if "nativelang" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN nativelang TEXT DEFAULT 'Telugu'"
        )

    if "otherlang" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN otherlang TEXT DEFAULT 'No'"
        )

    connection.commit()
    connection.close()


# ============================================================
# SIGN UP
# ============================================================

def signup(
    username,
    password,
    age,
    gender="Female",
    nativelang="Telugu",
    otherlang="No"
):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Check whether username already exists
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        connection.close()

        return {
            "success": False,
            "message": "Username already exists"
        }

    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    # Store user
    cursor.execute(
        """
        INSERT INTO users
        (username, password, age, gender, nativelang, otherlang)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            hashed_password.decode("utf-8"),
            age,
            gender,
            nativelang,
            otherlang
        )
    )

    connection.commit()
    connection.close()

    return {
        "success": True,
        "message": "Account created successfully"
    }


# ============================================================
# SIGN IN
# ============================================================

def signin(username, password):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT username, password, age,
               gender, nativelang, otherlang
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    # Username not found
    if user is None:

        return {
            "success": False,
            "message": "Username or password is incorrect"
        }

    stored_username = user[0]
    stored_password = user[1]
    age = user[2]
    gender = user[3]
    nativelang = user[4]
    otherlang = user[5]

    # Check password
    password_correct = bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password.encode("utf-8")
    )

    if password_correct:

        return {
            "success": True,
            "message": "Login successful",
            "username": stored_username,
            "age": age,
            "gender": gender,
            "nativelang": nativelang,
            "otherlang": otherlang
        }

    return {
        "success": False,
        "message": "Username or password is incorrect"
    }
def get_user(username):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT username, age, gender, nativelang, otherlang
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    return {
        "username": user[0],
        "age": user[1],
        "gender": user[2],
        "nativelang": user[3],
        "otherlang": user[4]
    }
def reset_password(username, new_password):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    if user is None:
        connection.close()

        return {
            "success": False,
            "message": "Username not found"
        }

    hashed_password = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    )

    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE username = ?
        """,
        (
            hashed_password.decode("utf-8"),
            username
        )
    )

    connection.commit()
    connection.close()

    return {
        "success": True,
        "message": "Password reset successfully"
    }


# ============================================================
# CREATE DATABASE WHEN FILE RUNS
# ============================================================

if __name__ == "__main__":

    create_database()

    print("Database created/updated successfully.")