import os
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
import torch.nn as nn


class TrainingSet:
    def __init__(self, season):
        self.season = season
        # self.collect_fixtures_data(season)

    def collect_fixtures_data(self, season):
        path = f"/home/evenmn/Fantasy-Premier-League/data/{season}/fixtures.csv"
        self.fixtures = pd.read_csv(path)

    def collect_player_ids(self, season):
        path = f"/home/evenmn/Fantasy-Premier-League/data/{season}/player_idlist.csv"
        self.player_ids = pd.read_csv(path)
        return self.player_ids

    def collect_player_data(self, season, id):
        player_ids = self.collect_player_ids(season)
        index = player_ids[player_ids["id"] == id].index[0]
        player_name = player_ids["first_name"][index] + " " + \
                      player_ids["second_name"][index]
        player_name = player_name.replace(" ", "_")
        path = f"/home/evenmn/Fantasy-Premier-League/data/{season}/players/{player_name}_{id}/gw.csv"
        return pd.read_csv(path)

    def expected_points(self):
        id = 55
        round = 4
        data = self.collect_player_data(self.season, id)
        player_properties = ["bps", "creativity", "ict_index", "influence", "minutes", "opponent_team", "team_a_score", "team_h_score", "threat", "total_points", "was_home"]
        print(data[player_properties])

    def collect_player_datas(self):
        print("Collecting player data...")
        season = self.season
        path = f"/home/evenmn/Fantasy-Premier-League/data/{season}/players/"
        # player_properties = ["bps", "creativity", "ict_index", "influence", "minutes", "opponent_team", "team_a_score", "team_h_score", "threat", "total_points", "was_home"]
        players = next(os.walk(path))[1]
        all_data = []
        for player in tqdm(players):
            full_path = path + player + "/gw.csv"
            data = pd.read_csv(full_path)
            all_data.append(data)  # [player_properties])
        return all_data

    def prepare_data_sets(self, dept=5, test=0.2):
        """Preparing training set, test set and targets
        """
        # player_properties = ["bps", "creativity", "ict_index", "influence", "minutes", "opponent_team", "team_a_score", "team_h_score", "threat", "total_points", "was_home"]
        player_properties = ["assists", "attempted_passes", "big_chances_created", "big_chances_missed", "bonus", "bps", "clean_sheets", "clearances_blocks_interceptions", "completed_passes", "creativity", "dribbles", "ea_index", "element", "errors_leading_to_goal", "errors_leading_to_goal_attempt", "fixture", "fouls", "goals_conceded", "goals_scored", "ict_index", "id", "influence", "key_passes", "loaned_in", "loaned_out", "minutes", "offside", "open_play_crosses", "opponent_team", "own_goals", "penalties_conceded", "penalties_missed", "penalties_saved", "recoveries", "red_cards", "round", "saves", "selected", "tackled", "tackles", "target_missed", "team_a_score", "team_h_score", "threat", "total_points", "transfers_balance", "transfers_in", "transfers_out", "value", "was_home", "winning_goals", "yellow_cards"]
        number_of_features = dept * len(player_properties)
        datas = self.collect_player_datas()
        print("\nPreparing training set...")
        print(f"Number of features: {number_of_features}")
        inputs = []
        targets = []
        j = 0
        for data in tqdm(datas):
            end = False
            i = 0
            while not end:
                try:
                    inp = np.asarray(data[player_properties][i:i+dept], dtype=float).flatten()
                    if len(inp) == number_of_features:
                        targets.append(data["total_points"][i+dept+1])
                        inputs.append(inp)
                        j += 1
                    else:
                        end = True
                except KeyError:
                    end = True
                i += 1
        inputs = np.asarray(inputs, dtype=float)
        targets = np.asarray(targets, dtype=int)

        assert len(inputs) == len(targets)

        total_size = len(inputs)
        test_size = int(test * total_size)
        train_size = total_size - test_size

        train_x = inputs[test_size:]
        train_t = targets[test_size:].reshape(train_size, 1)
        test_x = inputs[:test_size]
        test_t = targets[:test_size].reshape(test_size, 1)

        return train_x, train_t, test_x, test_t

    def set_model(self, modules):
        self.model = nn.Sequential(*modules)
        return self.model

    def train_torch(self, x, t, lr, max_iter):
        """Train the neural network model.
        """
        print("\nTraining...")
        # Get data
        x = torch.tensor(x)
        t = torch.tensor(t)

        # Define loss and optimizer
        loss_func = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

        # Train network
        for epoch in range(max_iter):
            # Forward propagation
            y = self.model(x.float())
            loss = loss_func(y, t.float())
            print("epoch: ", epoch, " loss: ", loss.item())  # Zero the gradients
            optimizer.zero_grad()

            # Backward propagation
            loss.backward()   # perform a backward pass (backpropagation)
            optimizer.step()  # update parameters

    def test(self, x, t):
        """
        """
        print("\nTesting...")
        # Get data
        x = torch.tensor(x)
        t = torch.tensor(t)

        # Test network
        y = self.model(x.float())
        loss_func = nn.MSELoss()
        loss = loss_func(y, t.float())
        print(loss)


if __name__ == "__main__":
    seasons = ["2016-17", "2017-18", "2018-19", "2019-20"]
    train_x, train_t, test_x, test_t = [], [], [], []
    for season in seasons:
        print(f"\nSEASON {season}")
        train = TrainingSet(season=season)
        modules = [nn.Linear(260, 64),
                   nn.ReLU(),
                   nn.Linear(64, 64),
                   nn.ReLU(),
                   nn.Linear(64, 1)]
        train.set_model(modules)
        trx, trt, tex, tet = train.prepare_data_sets()
        train_x.append(trx)
        train_t.append(trt)
        test_x.append(tex)
        test_t.append(tet)
    train_x = np.vstack(train_x)
    train_t = np.vstack(train_t)
    test_x = np.vstack(test_x)
    test_t = np.vstack(test_t)

    train.train_torch(train_x, train_t, lr=2e-2, max_iter=1000)
    train.test(test_x, test_t)
