import os
import sys
import datetime

# This script checks for overdue tasks for a given subject.
# It is intended to be called from a Xano endpoint.

# TODO: Fill in the database connection details below.
# It is recommended to use environment variables for security.
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

def check_overdue_tasks(subject_id):
    """
    Checks if a subject has overdue tasks.

    Args:
        subject_id: The ID of the subject to check.

    Returns:
        True if the subject has overdue tasks, False otherwise.
    """
    # This is a placeholder for the actual database query.
    # You will need to replace this with a real database connection
    # and query to check for overdue tasks.
    
    # Example using psycopg2 (for PostgreSQL)
    # try:
    #     import psycopg2
    #     conn = psycopg2.connect(
    #         host=DB_HOST,
    #         port=DB_PORT,
    #         dbname=DB_NAME,
    #         user=DB_USER,
    #         password=DB_PASSWORD,
    #     )
    #     cur = conn.cursor()
    #     query = """
    #         SELECT COUNT(*)
    #         FROM academic_tasks
    #         WHERE subject_id = %s
    #           AND due_date < %s
    #           AND status != 'completed'
    #     """
    #     cur.execute(query, (subject_id, datetime.datetime.now()))
    #     count = cur.fetchone()[0]
    #     cur.close()
    #     conn.close()
    #     return count > 0
    # except Exception as e:
    #     # Log the error to stderr
    #     print(f"Error connecting to the database: {e}", file=sys.stderr)
    #     return False

    # For now, we'll use a dummy implementation that returns False.
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        subject_id = sys.argv[1]
        if check_overdue_tasks(subject_id):
            print("true")
        else:
            print("false")
    else:
        print("Usage: python check_overdue_tasks.py <subject_id>", file=sys.stderr)
        sys.exit(1)
