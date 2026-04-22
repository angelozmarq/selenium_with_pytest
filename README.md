# Selenium + Pytest Test Automation

This project demonstrates browser automation testing using Selenium WebDriver, Pytest, and Python.

## 1. Prerequisites Installation

**Ensure you have the following installed:**
- [Python 3.10+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) (a super-fast Python package manager)
- Browser(s) (Chrome, Firefox, Edge) and the appropriate [WebDriver binaries](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)

## 2. Setup and Dependency Installation with `uv`

[uv](https://github.com/astral-sh/uv) is recommended for managing Python environments and dependencies.

**Install `uv` globally (if not already):**
```sh
pip install uv
```

**Initialize a new project and environment:**
```sh
uv init
source .venv/bin/activate    # On Unix or MacOS
.venv\Scripts\activate       # On Windows
```

**Install dependencies using one of the following methods:**

- If you have a `pyproject.toml` file, run:
  ```sh
  uv sync
  ```
- If you have a `requirements.txt` file, run:
  ```sh
  uv pip install -r requirements.txt
  ```

*Make sure your `.env` file is set up with the appropriate environment variables (`URL`, etc.).*

## 4. Running the Tests

You can run the test suite with:
```sh
pytest --browser=chrome             # Run using Chrome (default)
pytest --browser=firefox            # Run using Firefox
pytest --browser=edge               # Run using Edge
pytest --headless                   # Add to run in headless mode
```

**To run tests in parallel (requires `pytest-xdist`):**
```sh
pytest -n auto                      # Automatically uses all CPU cores for parallel test execution
pytest -n 4                         # Run tests in 4 parallel workers
```

*An HTML report will be automatically saved to the `reports/html/` directory after test execution.*

**Note:**  
Test parameters (such as the application URL, timeouts, and metadata) can be configured in the `.env` file.

---