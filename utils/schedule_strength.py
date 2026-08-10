import pandas as pd

def compute_schedule_strength(games, teams):
    preseason = pd.read_csv("data/preseason.csv")
    score_lookup = dict(zip(preseason["TeamID"], preseason["PreseasonScore"]))

    conf_games = games[games["IsConference"] == True]

    rows = []
    for team_id in teams["TeamID"]:
        team_games = conf_games[
            (conf_games["HomeID"] == team_id) | (conf_games["AwayID"] == team_id)
        ]

        opponents = [
            g["AwayID"] if g["HomeID"] == team_id else g["HomeID"]
            for _, g in team_games.iterrows()
        ]

        opp_scores = [score_lookup.get(o, 50) for o in opponents]
        avg_strength = sum(opp_scores) / len(opp_scores) if opp_scores else 0

        rows.append({"TeamID": team_id, "AvgOpponentScore": avg_strength, "GamesCounted": len(opponents)})

    result = pd.DataFrame(rows).merge(teams[["TeamID", "School", "Class"]], on="TeamID")
    result = result.rename(columns={"School": "Team"})
    result = result.sort_values("AvgOpponentScore", ascending=False).reset_index(drop=True)
    result["Rank"] = result.index + 1

    return result