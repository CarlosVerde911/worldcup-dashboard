import sqlite3
import os
from datetime import datetime, timezone, timedelta

DB_PATH = os.environ.get("DB_PATH", "worldcup.db")

def main_db():
    # CREATE CONNECTION TO DATABASE FILE
    db_conn = sqlite3.connect(DB_PATH)
    
    # CREATE TABLES IF THEY DON'T ALREADY EXIST
    db_conn.execute("""
        CREATE TABLE IF NOT EXISTS match_days (
            match_id        INTEGER PRIMARY KEY,
            matchday        INTEGER,
            stage           TEXT,
            group_name      TEXT,
            home_team       TEXT,
            away_team       TEXT,
            match_date      TEXT,
            home_score      INTEGER,
            away_score      INTEGER,
            status          TEXT
        )
    """)

    db_conn.execute("""
        CREATE TABLE IF NOT EXISTS group_standings (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name      TEXT,
            position        INTEGER,
            team_name       TEXT,
            won             INTEGER,
            draw            INTEGER,
            lost            INTEGER,
            goal_difference INTEGER,
            points          INTEGER,
            UNIQUE(group_name, team_name)
        )
    """)

    db_conn.execute("""
        CREATE TABLE IF NOT EXISTS top_scorers (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            rank            INTEGER,
            player_name     TEXT,
            team_name       TEXT,
            goals           INTEGER,
            UNIQUE(player_name, team_name)
        )
    """)

    db_conn.execute("""
        CREATE TABLE IF NOT EXISTS last_updated (
            id              INTEGER PRIMARY KEY CHECK (id = 1),
            match_days_ts   TEXT,
            standings_ts    TEXT,
            top_scorers_ts  TEXT
        )
    """)

    db_conn.execute("INSERT OR IGNORE INTO last_updated (id) VALUES (1)")

    # COMMIT .DB FILE TO SAVE ALL CHANGES
    db_conn.commit()
    # RELEASE THE .DB FILE
    db_conn.close()


def now_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save_match_days(matches):
    # USE RAW API JSON RESPONSE, UPSERTS ROWS INTO MATCH_DAYS TABLE
    eastern_timezone = timezone(timedelta(hours=-4))
    rows = []
    for match in matches:
        match_date = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).astimezone(eastern_timezone).strftime("%Y-%m-%d")
        rows.append(
            (
                match["id"],
                match["matchday"],
                match["stage"],
                match.get("group"),
                match["homeTeam"]["name"] or "TBD",
                match["awayTeam"]["name"] or "TBD",
                match_date,
                match["score"]["fullTime"]["home"],
                match["score"]["fullTime"]["away"],
                match["status"],
            )
        )

    db_conn = sqlite3.connect(DB_PATH)
    db_conn.executemany("""
        INSERT OR REPLACE INTO match_days (
            match_id, 
            matchday, 
            stage, 
            group_name, 
            home_team, 
            away_team, 
            match_date, 
            home_score, 
            away_score, 
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
    db_conn.execute("UPDATE last_updated SET match_days_ts = ? WHERE id = 1", (now_timestamp(),))
    db_conn.commit()
    db_conn.close()


def save_standings(standings):
    rows = []
    for group in standings:
        group_name = group.get("group", "Unknown Group")
        if not group_name.startswith("Group") and group_name != "Unknown Group":
            continue
        for entry in group.get("table", []):
            rows.append((
                group_name,
                entry["position"],
                entry["team"]["name"],
                entry["won"],
                entry["draw"],
                entry["lost"],
                entry["goalDifference"],
                entry["points"],
            ))

    db_conn = sqlite3.connect(DB_PATH)
    db_conn.executemany("""
        INSERT OR REPLACE INTO group_standings (
            group_name,
            position,
            team_name,
            won,
            draw,
            lost,
            goal_difference,
            points
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
    db_conn.execute("UPDATE last_updated SET standings_ts = ? WHERE id = 1", (now_timestamp(),))
    db_conn.commit()
    db_conn.close()

def save_top_scorers(scorers):
    rows = []
    for i, scorer in enumerate(scorers, start =1):
        rows.append((
            i,
            scorer["player"]["name"],
            scorer["team"]["name"],
            scorer["goals"],
        ))

    db_conn = sqlite3.connect(DB_PATH)
    db_conn.executemany("""
        INSERT OR REPLACE INTO top_scorers (
            rank,
            player_name,
            team_name,
            goals
        )
        VALUES (?, ?, ?, ?)
    """, rows)
    db_conn.execute("UPDATE last_updated SET top_scorers_ts = ? WHERE id = 1", (now_timestamp(),))
    db_conn.commit()
    db_conn.close()


def fetch_matches():
    db_conn = sqlite3.connect(DB_PATH)
    db_conn.row_factory = sqlite3.Row
    rows = db_conn.execute("SELECT * FROM match_days ORDER BY match_date").fetchall()
    db_conn.close()
    return rows


def fetch_standings():
    db_conn = sqlite3.connect(DB_PATH)
    db_conn.row_factory = sqlite3.Row
    rows = db_conn.execute("SELECT * FROM group_standings ORDER BY group_name, position").fetchall()
    db_conn.close()
    return rows

def fetch_scorers():
    db_conn = sqlite3.connect(DB_PATH)
    db_conn.row_factory = sqlite3.Row
    rows = db_conn.execute("SELECT * FROM top_scorers ORDER BY rank").fetchall()
    db_conn.close()
    return rows