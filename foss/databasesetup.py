import sqlite3

# Connect to SQLite (Creates 'tickets.db' if not exists)
conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

# Create Table for Tickets
cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                    ticket_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    event_id TEXT,
                    expiry TEXT,
                    status TEXT DEFAULT 'Valid')''')

# Create Table for Scanned Entries
cursor.execute('''CREATE TABLE IF NOT EXISTS entries (
                    ticket_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    event_id TEXT,
                    scan_time TEXT)''')

conn.commit()
conn.close()

print("✅ Database setup complete!")
