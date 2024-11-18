## Setup

Make sure to create a `config.py` in the `app/` directory.

Should contain the following information:

```python
class Config:
    MYSQL_HOST = 'localhost'  # or whatever IP address. 
    MYSQL_USER = '<replace>' # your root username in MySQL
    MYSQL_PASSWORD = '<replace>' # password to access database instance in MySQL
    MYSQL_DB = '<replace>' # the name of the database being accessed
```