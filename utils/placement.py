from utils.db import conn, cursor

def save_progress(
    username,
    dsa,
    aptitude,
    projects,
    interviews
):

    cursor.execute(
        """
        INSERT INTO placement_tracker
        (
        username,
        dsa,
        aptitude,
        projects,
        interviews
        )
        VALUES(?,?,?,?,?)
        """,
        (
            username,
            dsa,
            aptitude,
            projects,
            interviews
        )
    )

    conn.commit()
def get_latest_progress(username):

    cursor.execute(
        """
        SELECT
        dsa,
        aptitude,
        projects,
        interviews
        FROM placement_tracker
        WHERE username=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (username,)
    )

    return cursor.fetchone()
def save_study_hours(username, hours):

    cursor.execute(
        """
        INSERT INTO study_tracker
        (username, study_hours)
        VALUES(?,?)
        """,
        (username, hours)
    )

    conn.commit()


def get_total_study_hours(username):

    cursor.execute(
        """
        SELECT SUM(study_hours)
        FROM study_tracker
        WHERE username=?
        """,
        (username,)
    )

    result = cursor.fetchone()

    if result and result[0]:
        return result[0]

    return 0