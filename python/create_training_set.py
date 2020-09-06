import numpy as np
import pandas as pd

class TrainingSet:
    def __init__(self, year):
        self.year = year
        self.collect_fixtures_data(year)

    def collect_fixtures_data(self, year):
        path = f"/home/evenmn/Fantasy-Premier-League/data/{year}/fixtures.csv"
        self.fixtures = pd.read_csv(path)

    def collect_player_ids(self, year):
        path = f"/home/evenmn/Fantasy-Premier-League/data/{year}/player_idlist.csv"
        self.player_ids = pd.read_csv(path)
        return self.player_ids

    def collect_player_data(self, year, id):
        player_ids = self.collect_player_ids(year)
        index = player_ids[player_ids["id"] == id].index[0]
        player_name = player_ids["first_name"][index] + " " + \
                      player_ids["second_name"][index]
        player_name = player_name.replace(" ", "_")
        path = f"/home/evenmn/Fantasy-Premier-League/data/{year}/players/{player_name}_{id}/gw.csv"
        return pd.read_csv(path)

    def expected_points(self):
        id = 55
        round = 4
        data = self.collect_player_data(self.year, id)
        player_properties = ["bps", "creativity", "ict_index", "influence", "minutes", "opponent_team", "team_a_score", "team_h_score", "threat", "total_points", "was_home"]
        print(data[player_properties])

if __name__ == "__main__":
    train = TrainingSet(year="2018-19")
    train.expected_points()
