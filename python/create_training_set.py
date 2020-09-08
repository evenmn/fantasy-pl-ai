import os
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
import torch.nn as nn

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

    def collect_player_datas(self):
        year = self.year
        path = f"/home/evenmn/Fantasy-Premier-League/data/{year}/players/"
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
        player_properties = ["bps", "creativity", "ict_index", "influence", "minutes", "opponent_team", "team_a_score", "team_h_score", "threat", "total_points", "was_home"]
        datas = self.collect_player_datas()
        inputs = []
        targets = []
        j = 0
        for data in tqdm(datas):
            end = False
            i = 0
            while not end:
                try:
                    inp = np.asarray(data[player_properties][i:i+dept], dtype=float).flatten()
                    if len(inp) == dept * len(player_properties):
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
        # train_size = total_size - test_size

        test_x = inputs[:test_size]
        test_t = targets[:test_size]
        train_x = inputs[test_size:]
        train_t = targets[test_size:]

        return test_x, test_t, train_x, train_t

    def set_model(self, modules):
        self.model = nn.Sequential(*modules)
        return self.model

    def train_torch(self, lr, max_iter):
        """Train the neural network model.
        """
        # Get data
        test_x, test_t, train_x, train_t = train.prepare_data_sets()
        #training_data = self.generate_training_data(initial_games, goal_steps)
        #x = torch.tensor([i[0] for i in training_data]).reshape(-1, 5)
        #t = torch.tensor([i[1] for i in training_data]).reshape(-1, 1)
        x = torch.tensor(train_x)
        t = torch.tensor(train_t)

        print(x.shape)
        print(t.shape)

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

if __name__ == "__main__":
    train = TrainingSet(year="2018-19")
    modules = [nn.Linear(55, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 1)]
    train.set_model(modules)
    train.train_torch(lr=2e-2, max_iter=500)
