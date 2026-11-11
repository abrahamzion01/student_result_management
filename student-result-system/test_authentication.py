
import secrets

from authentication import register_user, login_user

# Generate unique usernames so the test can run repeatedly
suffix = secrets.token_hex(3)

accounts = [
    (f"student_{suffix}", "student123", "student"),
    (f"teacher_{suffix}", "teacher123", "teacher"),
    (f"admin_{suffix}", "admin123", "admin")
]

for username, password, role in accounts:

    # Register account
    registered = register_user(username, password, role)
    print(f"{role} registration:", registered)

    # Test correct password
    user = login_user(username, password)
    print(f"{role} login:", user)

    # Test incorrect password
    wrong_login = login_user(username, "wrongpassword")
    print(f"{role} wrong password:", wrong_login)

    print("-------------------------")
