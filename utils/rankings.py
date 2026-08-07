import pandas as pd
from models.mpi import calculate_mpi
from utils.stats import build_team_stats

def get_rankings(games, teams):
    season_started = (games["Status"] == "Final").any()

    if not season_started:
        preseason = pd.read_csv("data/preseason.csv")
        rankings = preseason.merge(teams[["TeamID", "School", "Class"]], on="TeamID")
        rankings = rankings.rename(columns={"School": "Team", "PreseasonScore": "MPI"})
        rankings["Wins"] = 0
        rankings["Losses"] = 0
        rankings["Points_For"] = 0
        rankings["Points_Against"] = 0
    else:
        stats = build_team_stats(games, teams)
        stats = calculate_mpi(stats)
        rankings = stats.merge(teams[["TeamID", "School", "Class"]], on="TeamID")
        rankings = rankings.rename(columns={"School": "Team"})

    rankings = rankings.sort_values("MPI", ascending=False).reset_index(drop=True)
    rankings["Rank"] = rankings.index + 1

    return rankings, season_started