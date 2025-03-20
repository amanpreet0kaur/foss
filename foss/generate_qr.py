import sqlite3
import qrcode
import json
import random
import os

# Create 'qr' folder if it doesn't exist
qr_folder = "qr"
os.makedirs(qr_folder, exist_ok=True)

# Connect to Database
conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

# Create tickets table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT PRIMARY KEY,
        user_id TEXT,
        event_id TEXT,
        expiry TEXT,
        scanned INTEGER DEFAULT 0
    )
""")

# Function to generate a random user ID
def generate_user_id():
    return f"USR{random.randint(10000, 99999)}"

# Function to generate random event ID
def generate_event_id():
    return f"E{random.randint(1000, 9999)}"

# Generate 10 QR codes
for i in range(1, 11):
    ticket_id = f"EVT{random.randint(10000000, 99999999)}"  # Unique Ticket ID
    user_id = generate_user_id()
    event_id = generate_event_id()
    expiry = "2025-02-25 18:00:00"

    # Insert into Database
    cursor.execute("INSERT INTO tickets (ticket_id, user_id, event_id, expiry) VALUES (?, ?, ?, ?)",
                   (ticket_id, user_id, event_id, expiry))
    
    # Generate QR Code Data (Convert Ticket Info to JSON)
    ticket_data = {"ticket_id": ticket_id, "user_id": user_id, "event_id": event_id, "expiry": expiry}
    qr = qrcode.make(json.dumps(ticket_data))

    # Save QR Code in 'qr' folder
    qr_path = os.path.join(qr_folder, f"QR_{ticket_id}.png")
    qr.save(qr_path)
    print(f"✅ QR Code saved as {qr_path}")

# Commit changes and close connection
conn.commit()
conn.close()

print("🎟️ 10 QR codes generated and saved in 'qr' folder successfully!")
