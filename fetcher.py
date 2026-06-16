import requests
import json
import os
from datetime import datetime, timezone, timedelta
import database

def main():
    BASE_URL = "https://api.football-data.org/v4/competitions/WC"

    API_TOKEN = os.environ.get("FOOTBALL_DATA_API_KEY")

    HEADERS = {"X-Auth-Token": API_TOKEN}

    database.main_db()

    get_match_days(BASE_URL, HEADERS)

    get_standings(BASE_URL, HEADERS)

    get_top_scorers(BASE_URL, HEADERS)


def get_match_days(base_url, headers):
    url = f"{base_url}/matches"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Request Failed. Status: {response.status_code}, Response: {response.text}")
    
    else:
        matches = response.json()["matches"]
        current_matchday = None
        current_group = None

        print("2026 FIFA WORLD CUP")
        print(f"{len(matches)} GAMES.")

        for match in matches:
            matchday = match["matchday"]
            stage = match["stage"]
            group = match.get("group", None)
            home_team = match["homeTeam"]["name"] if match["homeTeam"]["name"] else "TBD"
            away_team = match["awayTeam"]["name"] if match["awayTeam"]["name"] else "TBD"
            date = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-4))).strftime("%Y-%m-%d")
            home_score = match["score"]["fullTime"]["home"]
            away_score = match["score"]["fullTime"]["away"]
            matchday_label = f"MATCHDAY {matchday}" if matchday else "PLAY-OFFS"

            if matchday != current_matchday:
                current_matchday = matchday
                current_group = None
                print(f"\n --- {matchday_label} {stage} ---")

            if group and group != current_group:
                current_group = group
                print(f"\n{group}")

            status = match["status"]

            if status == "TIMED":
                print(f"{date}   {home_team} VS {away_team}   Timed: {home_score} - {away_score}")
            elif status == "FINISHED":
                print(f"{date}   {home_team} VS {away_team}   Final Score: {home_score} - {away_score}")
            elif status == "IN_PLAY":
                print(f"{date}   {home_team} VS {away_team}   In Play: {home_score} - {away_score}")

        database.save_match_days(matches)


def get_standings(base_url, headers):
    url = f"{base_url}/standings"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Request Failed. Status: {response.status_code}, Response: {response.text}")
    
    else:
        data = response.json()

        standings = data.get("standings", [])

        for group in standings:
            group_name = group.get("group", "Unknown Group")
            print(f"\n--- {group_name.upper()} STANDINGS ---")

            for entry in group.get("table", []):
                team_name = entry["team"]["name"]
                won = entry["won"]
                draw = entry["draw"]
                lost = entry["lost"]
                goal_diff = entry["goalDifference"]

                print(f" {entry['position']} {team_name} --- Won: {won}  Draw: {draw}  Lost: {lost}  Goal Difference: {goal_diff}")
            
        database.save_standings(standings)


def get_top_scorers(base_url, headers):
    url = f"{base_url}/scorers"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Request Failed. Status: {response.status_code}, Response: {response.text}")
    
    else:
        scorers = response.json()["scorers"]

        print("\n --- FIFA World Cup - Top Scorers ---")

        for i, scorer in enumerate(scorers, start=1):
            player_name = scorer["player"]["name"]
            team = scorer["team"]["name"]
            goals = scorer["goals"]

            print(f"{i}. Player Name: {player_name} // Team: {team} // Goals Scored: {goals}")

        database.save_top_scorers(scorers)


if __name__ == "__main__":
    main()
