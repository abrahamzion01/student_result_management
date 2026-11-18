
import hashlib
import secrets
import hmac

from database import get_connection, initialize_database


# Allowed account types
VALID_ROLES = ("student", "teacher", "admin")

# Password hashing settings
ITERATIONS = 600_000


def hash_password(password, salt):
    password_bytes = password.encode("utf-8")
    salt_bytes = bytes.fromhex(salt)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt_bytes,
        ITERATIONS
    )

    return password_hash.hex()


def register_user(username, password, role, reg_no=None):
    username = username.strip()
    role = role.strip().lower()

    if not username or not password:
        return False

    if len(password) < 8:
        return False

    if role not in VALID_ROLES:
        return False

    if role == "student":
        if not reg_no or not reg_no.strip():
            return False
        reg_no = reg_no.strip()

    # Generate a random salt
    salt = secrets.token_hex(16)

    # Hash the password
    password_hash = hash_password(password, salt)

    initialize_database()
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (username, password_hash, salt, role)
            VALUES (?, ?, ?, ?)
        """, (username, password_hash, salt, role))

        user_id = cursor.lastrowid

        if role == "student":
            cursor.execute("""
                INSERT INTO student_accounts (user_id, reg_no)
                VALUES (?, ?)
            """, (user_id, reg_no))

        connection.commit()
        return True

    except Exception as error:
        print("Account registration error:", error)
        return False

    finally:
        connection.close()


def login_user(username, password):
    username = username.strip()

    initialize_database()
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if user is None:
            return None

        entered_hash = hash_password(password, user["salt"])

        if hmac.compare_digest(
            entered_hash,
            user["password_hash"]
        ):
            return {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }

        return None

    finally:
        connection.close()
