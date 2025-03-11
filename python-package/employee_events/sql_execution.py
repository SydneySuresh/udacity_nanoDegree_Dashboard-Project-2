from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Define db_path using pathlib to point to 'employee_events.db'
db_path = Path(__file__).parent / 'employee_events.db'

# Leave this code unchanged
def query(func):
    """
    Decorator that executes an SQL query and returns results as a list of tuples.
    It connects to the database, runs the query, fetches results, and closes the connection.
    """
    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query

# OPTION 1: MIXIN
# Define a mixin class for database queries
class QueryMixin:
    
    # Define a method to execute an SQL query and return a pandas DataFrame
    def pandas_query(self, query: str) -> pd.DataFrame:
        """Executes an SQL query and returns a pandas DataFrame."""
        with connect(db_path) as conn:
            return pd.read_sql_query(query, conn)

    # Define a method to execute an SQL query and return results as a list of tuples
    @query
    def query(self, sql_query: str):
        """Executes an SQL query and returns results as a list of tuples."""
        return sql_query  # The decorator handles execution

