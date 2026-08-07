import pandas as pd

HISTORY_COLUMNS = ["Week", "TeamID", "MPI"]

def load_history(path="data/mpi_history.csv"):
    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        return pd.DataFrame(columns=HISTORY_COLUMNS)

def save_snapshot(week, rankings, path="data/mpi_history.csv"):
    history = load_history(path)
    history = history[history["Week"] != week]
    new_rows = rankings[["TeamID", "MPI"]].copy()
    new_rows.insert(0, "Week", week)
    history = pd.concat([history, new_rows], ignore_index=True)
    history.to_csv(path, index=False)

def get_movers(games, teams, top_n=5):
    from utils.rankings import get_rankings

    rankings, season_started = get_rankings(games, teams)
    if not season_started:
        return None

    current_week = games[games["Status"] == "Final"]["Week"].max()
    history = load_history()

    past_weeks = history[history["Week"] < current_week]["Week"]

    if not past_weeks.empty:
        baseline_week = past_weeks.max()
        baseline = history[history["Week"] == baseline_week][["TeamID", "MPI"]].rename(columns={"MPI": "PrevMPI"})
        baseline_label = f"Week {int(baseline_week)}"
    else:
        preseason = pd.read_csv("data/preseason.csv").rename(columns={"PreseasonScore": "PrevMPI"})
        baseline = preseason[["TeamID", "PrevMPI"]]
        baseline_label = "Preseason"

    merged = rankings.merge(baseline, on="TeamID", how="left")
    merged["PrevMPI"] = merged["PrevMPI"].fillna(merged["MPI"])
    merged["Delta"] = merged["MPI"] - merged["PrevMPI"]

    risers = merged.sort_values("Delta", ascending=False).head(top_n)
    fallers = merged.sort_values("Delta", ascending=True).head(top_n)

    return {
        "risers": risers,
        "fallers": fallers,
        "baseline_label": baseline_label,
        "current_week": int(current_week)
    }