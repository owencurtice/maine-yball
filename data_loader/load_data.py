import pandas as pd


def load_teams():
    return pd.read_csv("data/teams.csv")


def load_schedule():
    return pd.read_csv("data/schedule.csv")


def load_results():
    return pd.read_csv("data/results.csv")


def load_stats():
    return pd.read_csv("data/football_stats.csv")