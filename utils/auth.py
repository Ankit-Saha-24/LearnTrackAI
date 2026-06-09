import bcrypt
from utils.db import conn, cursor


def register_user(username, password):

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            (
                username,
                hashed_password
            )
        )

        conn.commit()

        return True

    except:

        return False


def login_user(username, password):

    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cursor.fetchone()

    if user:

        stored_password = user[0]

        if bcrypt.checkpw(
            password.encode(),
            stored_password
        ):
            return True

    return False