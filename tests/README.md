# Unit Tests Directory

Welcome to the Unit Tests directory! This directory houses unit tests for the FastAPI application, providing a robust testing suite to ensure the functionality and reliability of the codebase.

---

## File Structure:

- **test_main.py:**
  - Contains unit tests for the `main` module of the FastAPI application (`../app/main.py`).
  - Utilizes the `TestClient` class from `fastapi.testclient` for endpoint testing.
  - Sets up fixtures for creating a testing database and a testing client.

## Running Tests:
- **Creating the Python Virtual Environment:**
    ```markdown
    - sudo apt-get update
    - sudo apt-get install python3-venv
    - python3 -m venv venv

    - pip install virtualenv
    - virtualenv -p python3 <env_name>
    - source <env_name>/bin/activate
    - deactivate
    ```

- **Activating the Python Virtual Environment:**
    ```markdown
    - source venv/bin/activate
    ```

- **Deactivating the Python Virtual Environment:**
    ```markdown
    - deactivate
    ```

- **Install Dependencies:**
   - Ensure all project dependencies are installed. You can use a virtual environment for isolation:
     ```bash
     pip install -r requirements.txt
     ```

- **Run Tests:**
   - Execute the unit tests using a test runner (e.g., pytest):
     ```bash
     pytest tests/
     ```

## Test Fixtures:

- **session:**
  - A fixture that sets up a testing database session using SQLAlchemy.
  - Drops and recreates the database schema before running tests.

- **client:**
  - A fixture that sets up a testing client for FastAPI endpoints.
  - Overrides the `get_db` dependency in FastAPI to use the testing database session.

---

---

<p align="center">The End, Thank You!</p>

---