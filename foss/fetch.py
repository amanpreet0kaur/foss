from flask import Flask, jsonify, render_template
import sqlite3
import os
import json
from collections import Counter

app = Flask(__name__)

# Ensure the templates directory exists
os.makedirs("templates", exist_ok=True)

# Fetch classification data
def fetch_classification_data():
    conn = sqlite3.connect("classifications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT gender, nationality, age, sentiment FROM classifications")
    rows = cursor.fetchall()
    conn.close()

    data = [{"gender": row[0], "nationality": row[1], "age": row[2], "sentiment": row[3]} for row in rows]

    # Count occurrences
    gender_count = dict(Counter([row["gender"] for row in data]))
    nationality_count = dict(Counter([row["nationality"] for row in data]))
    age_count = dict(Counter([row["age"] for row in data]))

    return gender_count, nationality_count, age_count

# Fetch ticket and entry data
def fetch_ticket_entry_data():
    conn = sqlite3.connect("event_tickets.db")
    cursor = conn.cursor()

    # Count total tickets
    cursor.execute("SELECT COUNT(*) FROM tickets")
    total_tickets = cursor.fetchone()[0]

    # Count total entries
    cursor.execute("SELECT COUNT(*) FROM entries")
    total_entries = cursor.fetchone()[0]

    conn.close()
    
    return {"Tickets Issued": total_tickets, "Entries": total_entries}

@app.route("/")
def index():
    gender_count, nationality_count, age_count = fetch_classification_data()
    ticket_entry_count = fetch_ticket_entry_data()

    return render_template("index1.html",
                           gender_count=json.dumps(gender_count),
                           nationality_count=json.dumps(nationality_count),
                           age_count=json.dumps(age_count),
                           ticket_entry_count=json.dumps(ticket_entry_count))

@app.route("/get_data", methods=["GET"])
def get_data():
    gender_count, nationality_count, age_count = fetch_classification_data()
    ticket_entry_count = fetch_ticket_entry_data()

    return jsonify({
        "gender_count": gender_count,
        "nationality_count": nationality_count,
        "age_count": age_count,
        "ticket_entry_count": ticket_entry_count
    })

if __name__ == "__main__":
    app.run(debug=True)
