import pandas as pd

def build_team_stats(games_df, teams_df):
    records = []

    for team_id in teams_df["TeamID"]:
        team_games = games_df[
            (games_df["HomeID"] == team_id) | (games_df["AwayID"] == team_id)
        ]

        conf_games = team_games[team_games["IsConference"] == True]
        opponents = [
            g["AwayID"] if g["HomeID"] == team_id else g["HomeID"]
            for _, g in conf_games.iterrows()
        ]

        finals = team_games[team_games["Status"] == "Final"]

        wins = losses = points_for = points_against = 0

        for _, g in finals.iterrows():
            is_home = g["HomeID"] == team_id
            team_score = g["HomeScore"] if is_home else g["AwayScore"]
            opp_score = g["AwayScore"] if is_home else g["HomeScore"]

            points_for += team_score
            points_against += opp_score

            if team_score > opp_score:
                wins += 1
            elif team_score < opp_score:
                losses += 1

        records.append({
            "TeamID": team_id,
            "Wins": wins,
            "Losses": losses,
            "Points_For": points_for,
            "Points_Against": points_against,
            "Opponents": opponents,
        })

    return pd.DataFrame(records)