# This is a proof of concept of how to connect to the SQL Server Database

# import pyodbc

## BASIC REQUIREMENTS
# SERVER = 'Marcus_Comp'
# DATABASE = 'Alexandria'
# USERNAME = 'Marcus'
# PASSWORD = '1234'

## EXAMPLE CONNECTION STRING
# connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
# conn = pyodbc.connect(connectionString)

## USING CURSOR TO INTERACT WITH SQL SERVER
# cur = conn.cursor()
## "SELECT @@SERVERNAME" --> get the servername using a query
# result = cur.execute("SELECT @@SERVERNAME").fetchall()
# print(result)


