import sqlite3
import pandas as pd
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ride_performance.db")
excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ride_performance_dataset.xlsx")

print("Initializing SQLite database...")
if os.path.exists(db_path):
    print("Removing existing database file...")
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table rides1 with COLLATE NOCASE on text columns
print("Creating table rides1...")
cursor.execute("""
CREATE TABLE rides1 (
    Date TEXT,
    Time REAL,
    Booking_ID TEXT,
    Booking_Status TEXT COLLATE NOCASE,
    Customer_ID TEXT,
    Vehicle_Type TEXT COLLATE NOCASE,
    Pickup_Location TEXT,
    Drop_Location TEXT,
    V_TAT REAL,
    C_TAT REAL,
    Canceled_Rides_by_Customer TEXT COLLATE NOCASE,
    Canceled_Rides_by_Driver TEXT COLLATE NOCASE,
    Incomplete_Rides TEXT COLLATE NOCASE,
    Incomplete_Rides_Reason TEXT COLLATE NOCASE,
    Booking_Value REAL,
    Payment_Method TEXT COLLATE NOCASE,
    Ride_Distance REAL,
    Driver_Ratings REAL,
    Customer_Rating REAL,
    Vehicle_Images TEXT
)
""")

print("Loading data from Excel sheet 'July'...")
df = pd.read_excel(excel_path, sheet_name="July")
# Replace spaces in column names with underscores to match standard SQL syntax
df.columns = [c.replace(" ", "_") for c in df.columns]

print(f"Writing {len(df)} rows to database...")
df.to_sql("rides1", conn, if_exists="append", index=False)

# Let's execute the SQL script commands
sql_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ride_performance_project.sql")
print(f"Reading SQL script {sql_script_path}...")
with open(sql_script_path, "r") as f:
    sql_text = f.read()

# Preprocess SQL statements
statements = []
current_statement = []
for line in sql_text.split("\n"):
    # Strip comments starting with #
    clean_line = line.split("#")[0].strip()
    if not clean_line:
        continue
    current_statement.append(clean_line)
    if clean_line.endswith(";"):
        stmt = " ".join(current_statement)
        statements.append(stmt)
        current_statement = []

print(f"Parsed {len(statements)} SQL statements.")

# Execute SQL commands, skipping create database and use
for stmt in statements:
    lower_stmt = stmt.lower()
    if "create database" in lower_stmt or "use " in lower_stmt:
        print(f"Skipping MySQL-specific statement: {stmt}")
        continue
    
    print(f"Executing: {stmt}")
    try:
        cursor.execute(stmt)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        # If there's an error due to Max_Min_Driver_Rating view missing, we can create it
        if "no such table: Max_Min_Driver_Rating" in str(e):
            print("Creating Max_Min_Driver_Rating view alias...")
            cursor.execute("CREATE VIEW Max_Min_Driver_Rating AS SELECT * FROM min_max_Drating")
            # Retry
            cursor.execute(stmt)
            print("Success on retry!")
        else:
            raise e

# Make sure we also have Max_Min_Driver_Rating view defined just in case it wasn't triggered
cursor.execute("SELECT name FROM sqlite_master WHERE type='view' AND name='Max_Min_Driver_Rating'")
if not cursor.fetchone():
    print("Defining Max_Min_Driver_Rating view alias...")
    cursor.execute("CREATE VIEW Max_Min_Driver_Rating AS SELECT * FROM min_max_Drating")

conn.commit()
conn.close()
print("Database initialization completed successfully!")
