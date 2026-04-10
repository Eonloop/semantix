# SQL Injection in Login Forms

SQL injection occurs when untrusted input is concatenated into SQL statements.

Risk indicators:
- Dynamic query strings built from request parameters.
- Missing parameterized queries.

Potential impact:
- Authentication bypass.
- Data exposure from user tables.
- Unauthorized data modification.

Recommended controls:
- Parameterized queries and prepared statements.
- Least-privileged database roles.
- Strict input validation.
