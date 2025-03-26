import sqlite3

# Connect to the SQLite3 database
con = sqlite3.connect('database1.db')

# Create a cursor object
cur = con.cursor()

# Create the records table
cur.execute('''
    CREATE TABLE records (
        id TEXT,
        coach_number TEXT,
        watering_stations TEXT,
        contact_person TEXT,
        mobile_number TEXT,
        water_level TEXT
    )
''')

# Commit the changes and close the connection
con.commit()
con.close()

print("Database and table created successfully.")
