
import secrets

from authentication import register_user, login_user


def test_student_registration_and_login():
    username = f"student_{secrets.token_hex(3)}"

    registered = register_user(username, "student123", "student")

    assert registered is True

    user = login_user(username, "student123")

    assert user is not None


def test_teacher_registration_and_login():
    username = f"teacher_{secrets.token_hex(3)}"

    registered = register_user(username, "teacher123", "teacher")

    assert registered is True

    user = login_user(username, "teacher123")

    assert user is not None


def test_admin_registration_and_login():
    username = f"admin_{secrets.token_hex(3)}"

    registered = register_user(username, "admin123", "admin")

    assert registered is True

    user = login_user(username, "admin123")

    assert user is not None


def test_login_rejects_wrong_password():
    username = f"student_{secrets.token_hex(3)}"

    register_user(username, "student123", "student")

    user = login_user(username, "wrongpassword")

    assert user is None
