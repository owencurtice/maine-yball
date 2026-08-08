import math
import pandas as pd

STARTING_BASE = 1500
PRESEASON_SCALE = 8
HOME_ADVANTAGE = 50
K_FACTOR = 20


def seed_elo(teams):
    preseason = pd.read_csv("data/preseason.csv")
    elo = {}
    for _, row in preseason.iterrows():
        elo[row["TeamID"]] = STARTING_BASE + (row["PreseasonScore"] - 75) * PRESEASON_SCALE
    for tid in teams["TeamID"]:
        elo.setdefault(tid, STARTING_BASE)
    return elo


def win_probability(elo_a, elo_b, home_advantage=0):
    return 1 / (1 + 10 ** (-((elo_a + home_advantage) - elo_b) / 400))


def mov_multiplier(margin, winner_elo, loser_elo):
    elo_diff = winner_elo - loser_elo
    return math.log(max(margin, 1) + 1) * (2.2 / (0.001 * elo_diff + 2.2))


def compute_elo_timeline(games, teams):
    elo = seed_elo(teams)
    weeks = sorted(games["Week"].dropna().unique())
    elo_entering_week = {}
    records = []

    for wk in weeks:
        elo_entering_week[wk] = elo.copy()
        week_games = games[(games["Week"] == wk) & (games["IsConference"] == True)]
        updates = {}

        for _, g in week_games.iterrows():
            home, away = g["HomeID"], g["AwayID"]
            home_elo = elo[home]
            away_elo = elo[away]
            p_home = win_probability(home_elo, away_elo, HOME_ADVANTAGE)

            row = {
                "Week": wk, "GameID": g["GameID"], "HomeID": home, "AwayID": away,
                "HomeElo": home_elo, "AwayElo": away_elo,
                "HomeWinProb": p_home, "AwayWinProb": 1 - p_home,
                "Status": g["Status"], "HomeScore": g["HomeScore"], "AwayScore": g["AwayScore"],
                "Upset": False, "EloDiff": None
            }

            if g["Status"] == "Final":
                home_score, away_score = g["HomeScore"], g["AwayScore"]
                margin = abs(home_score - away_score)
                home_won = home_score > away_score

                s_home = 1 if home_won else 0
                winner_elo = home_elo if home_won else away_elo
                loser_elo = away_elo if home_won else home_elo
                mult = mov_multiplier(margin, winner_elo, loser_elo)
                delta = K_FACTOR * mult * (s_home - p_home)

                updates[home] = updates.get(home, 0) + delta
                updates[away] = updates.get(away, 0) - delta

                winner_prob = p_home if home_won else (1 - p_home)
                row["Upset"] = winner_prob < 0.5
                row["EloDiff"] = (away_elo - home_elo) if home_won else (home_elo - away_elo)

            records.append(row)

        for tid, delta in updates.items():
            elo[tid] = elo[tid] + delta

    predictions = pd.DataFrame(records)
    return elo_entering_week, elo, predictions