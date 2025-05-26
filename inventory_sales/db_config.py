import pyodbc

def database_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER={WKSPUN05GTR1604};'
            'DATABASE={retailstores};'
            'Trusted_Connection=yes;'
        )
        return conn      
    except Exception as e:
        print(f"Database connection error: {e}")
        return None
