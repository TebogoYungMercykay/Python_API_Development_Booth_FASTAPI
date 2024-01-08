# Generic single-database configuration.

- Review Previous Migrations:
    ```python
    alembic history
    ```
- Using Alembic to Automatically Create and Update Database Tables:
    ```python
    alembic revision --autogenerate -m "{version_name}"
    alembic upgrade head # running the database migrations
    ```
- Creating a Revision:
    ```python
    alembic revision -m "add some {column} to {table}"
    ```
- Getting the Current Revision:
    ```python
    alembic current
    ```
- Getting the Latest Revision:
    ```python
    alembic heads
    ```
- Upgrading a Revision:
    ```python
    alembic upgrade {revision}
    ```
- Rolling back a Revision:
    ```python
    alembic downgrade {down_revision}
    ```

---

---

<p align="center">The End, Thank You!</p>

---