"""Demo data. Credentials here are for local testing only."""
import sqlite3

from app.auth import hash_password

DEMO_USERS = [
    ("admin", "admin123", "admin"),
    ("viewer", "viewer123", "viewer"),
]

# (key, value, value_type, environment, description)
SAMPLE_CONFIGS = [
    ("feature.new_dashboard", "true", "bool", "dev", "Enable the redesigned dashboard"),
    ("feature.new_dashboard", "false", "bool", "staging", "Enable the redesigned dashboard"),
    ("feature.new_dashboard", "false", "bool", "prod", "Enable the redesigned dashboard"),
    ("api.rate_limit_per_minute", "1000", "int", "dev", "Requests allowed per client per minute"),
    ("api.rate_limit_per_minute", "300", "int", "prod", "Requests allowed per client per minute"),
    ("smtp.host", "smtp.dev.example.com", "string", "dev", "Outbound mail server"),
    ("smtp.host", "smtp.example.com", "string", "prod", "Outbound mail server"),
    ("log.level", "DEBUG", "string", "dev", "Application log level"),
    ("log.level", "WARNING", "string", "prod", "Application log level"),
    ("retry.policy", '{"max_attempts": 3, "backoff_seconds": 2}', "json", "staging", "HTTP retry policy"),
]


def seed(conn: sqlite3.Connection) -> None:
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        for username, password, role in DEMO_USERS:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, hash_password(password), role),
            )
    if conn.execute("SELECT COUNT(*) FROM configs").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO configs (key, value, value_type, environment, description) "
            "VALUES (?, ?, ?, ?, ?)",
            SAMPLE_CONFIGS,
        )
