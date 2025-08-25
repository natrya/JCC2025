import os


def get_database_path() -> str:
    db_path = os.getenv("DB_PATH", os.path.join(os.getcwd(), "data", "app.db"))
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return db_path


def get_database_url() -> str:
    # Use a file-based SQLite DB. check_same_thread is set on engine creation.
    return f"sqlite:///{get_database_path()}"


