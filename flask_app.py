from flask import Flask, render_template
import database

# --- Initialize the Flask app ---
# __name__ tells Flask where to look for templates/ and static/ folders
app = Flask(__name__)


# --- Main route ---
# The "/" route is what loads when someone visits your homepage
# render_template() tells Flask to find index.html inside your templates/ folder
# The variables after "index.html" are passed into the HTML file for Jinja2 to display

@app.route("/")

def index():
    matches   = database.fetch_matches()      # Reads from match_days table
    standings = database.fetch_standings()    # Reads from group_standings table
    scorers   = database.fetch_scorers()      # Reads from top_scorers table

    return render_template(
        "index.html",
        matches=matches,
        standings=standings,
        scorers=scorers
    )


# --- Run the app ---
# debug=True means Flask will auto-reload when you save changes to the file
# This only runs when you execute flask_app.py directly, not when imported

if __name__ == "__main__":
    app.run(debug=True)