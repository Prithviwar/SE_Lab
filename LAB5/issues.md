# Static Code Analysis Issues & Resolution Log

This document lists all static analysis issues identified by **Pylint**, **Bandit**, and **Flake8** in `bike_share_stations.py`, along with their classifications, descriptions, and applied resolution strategies.

---

## Findings & Resolutions Table

| Issue ID / Code | Analysis Tool | Line(s) | Severity / Category | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B608** | Bandit | 9 | **Medium** / Security (CWE-89) | Hardcoded SQL expressions using string concatenation (`VALUES ('" + name + "')`), making the application vulnerable to SQL Injection attacks. | Replaced raw string concatenation with standard parameterized SQL queries using `?` placeholders: `VALUES (?, ?, ?)`. |
| **B311** | Bandit | 26 | **Low** / Security (CWE-330) | Standard pseudo-random generator (`random.randint`) used for PIN generation, which is unsuitable for security or cryptographic purposes. | Replaced `random.randint(1000, 9999)` with cryptographically secure `secrets.randbelow(9000) + 1000`. |
| **B110 / W0702 / E722** | Bandit / Pylint / Flake8 | 34–35, 38–39 | **Low / Critical** / Quality & Security | Bare `try/except:` block with `pass` suppressed all exceptions, hiding system signals and execution errors. | Updated `try/except` block to catch a specific exception (`sqlite3.OperationalError`) and explicitly print an informative error message. |
| **W0102** | Pylint | 8 | **Warning** / Bug Risk | Dangerous default value `log=[]` as function parameter. Default argument expressions are evaluated once, causing state persistence across calls. | Changed function default to `log: Optional[List[str]] = None` and initialized `log = []` inside the function body when `None`. |
| **W0611** | Pylint | 1 | **Warning** / Clean Code | Unused import `random`. | Removed the unused import module from the file imports. |
| **W0612 / F841** | Pylint / Flake8 | 27, 39 | **Warning** / Style & Maintenance | Local variable `summary` assigned but never used. | Removed the dead `summary` variable assignment. |
| **C0103** | Pylint | 8, 14, 21, 25, 31, 38 | **Convention** / Naming Standard | Functions (`addStation`, `rentBike`, `unlockPin`, `fullStations`, `resetStation`, `hasBikes`) did not follow `snake_case` naming rules. | Refactored all function identifiers and calls to follow standard Python `snake_case` naming conventions (`add_station`, `rent_bike`, etc.). |
| **C0121 / E711** | Pylint / Flake8 | 40 | **Convention** / Style | Singleton comparison `row[0] == None` used instead of identity check. | Updated comparison expression to `row[0] is None`. |
| **E501** | Flake8 | 9, 45 | **Style** / PEP 8 Formatting | Lines exceeded the maximum allowed line length of 79 characters. | Reformatted SQL queries and argument lists across multiple lines to adhere strictly to the 79-character limit. |
| **W292** | Flake8 | 67 | **Style** / PEP 8 Formatting | Missing newline at the end of the file. | Added a trailing blank line at the bottom of `bike_share_stations.py`. |