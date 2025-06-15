"""Database connection string loaded from the DB_CONN environment variable."""

import os

connectionString = os.environ["DB_CONN"]
