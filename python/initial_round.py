import os
import glob
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
import torch.nn as nn


class InitialRound:

    BUDGET = 1000

    def __init__(self):
        pass

    def collect_player_history(self):
        print("Collecting player history...")
        seasons = ["2016-17", "2017-18", "2018-19", "2019-20"]
        player_features = ["assists", "bonus", "bps", "clean_sheets", "creativity", "element_code", "end_cost", "goals_conceded", "goals_scored", "ict_index", "influence", "minutes", "own_goals", "penalties_missed", "penalties_saved", "red_cards", "saves", "start_cost", "threat", "total_points", "yellow_cards"]
        path = "/home/evenmn/Fantasy-Premier-League/data/{}/players/"
        x, t = [], []
        for i in tqdm(range(len(seasons) - 1)):
            players = next(os.walk(path.format(seasons[i])))[1]
            for player in players:
                splitted = player.split("_")
                name_only = "_".join(splitted[:2])
                path1 = path.format(seasons[i]) + name_only + "*/history.csv"
                path2 = path.format(seasons[i+1]) + name_only + "*/gw.csv"
                try:
                    data1 = pd.read_csv(glob.glob(path1)[-1])
                    data2 = pd.read_csv(glob.glob(path2)[-1])
                    x.append(list(data1[player_features].iloc[-1]))
                    t.append(data2["total_points"].iloc[0])
                except IndexError:
                    continue
        return np.asarray(x, dtype=float), np.asarray(t, dtype=int).reshape(len(x), 1)

    def gen_train_test(self, test=0.2):
        x, t = self.collect_player_history()
        print(x.shape)
        print(t.shape)
        num_test = int(len(x) * test)
        num_train = int(len(x) - num_test)
        x_train = x[:num_train]
        t_train = t[:num_train]
        x_test = x[:num_test]
        t_test = t[:num_test]
        return x_train, t_train, x_test, t_test

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
        print(float(loss))

    def predict(self, season):
        print("\nPredicting scores...")
        path = "/home/evenmn/Fantasy-Premier-League/data/{}/players/"
        players = next(os.walk(path.format(season)))[1]

        names = []
        predicted_points = []
        for player in players:
            splitted = player.split("_")
            name_only = "_".join(splitted[:2])
            path1 = path.format("2019-20") + name_only + "*/history.csv"
            try:
                data1 = pd.read_csv(glob.glob(path1)[-1])
                x = list(data1.iloc[-1].drop("season_name"))
                x = torch.tensor(x)
                t = self.model(x.float())
                # print(f"\nAccording to AiAi, {name_only} will get {int(t)} points the first round")
                names.append(name_only)
                predicted_points.append(float(t))
            except IndexError:
                continue
        return names, predicted_points

    def select_initial_team(self, formation="3-5-2", season="2020-21"):
        formation_split = np.asarray(formation.split("-"), dtype=int)
        formation_split = np.insert(formation_split, 0, 1)

        num_teams = 20

        num_players = np.sum(formation_split)
        assert num_players == 11, "Invalid formation!"

        names, predicted_points = self.predict(season)
        names = np.asarray(names, dtype=str)
        predicted_points = np.asarray(predicted_points, dtype=float)
        sorted = np.argsort(predicted_points)

        print("\nSetting up team...")
        path = "/home/evenmn/Fantasy-Premier-League/data/{}/players_raw.csv"
        data = pd.read_csv(path.format(season))
        players = [[] for _ in range(len(formation_split))]
        points = [[] for _ in range(len(formation_split))]
        total_points = []
        cost = 0
        players_teams = np.zeros(num_teams)
        for i in sorted[::-1]:
            name = names[i]
            name_split = name.split("_")
            j = 0
            for f, s in zip(data["first_name"], data["second_name"]):
                if f == name_split[0] and s == name_split[1]:
                    position = data["element_type"].iloc[j]
                    new_cost = cost + data["now_cost"].iloc[j]
                    team = data["team"].iloc[j]
                    if len(players[position-1]) < formation_split[position-1] and new_cost < self.BUDGET and players_teams[team-1] < 3:
                        players[position-1].append(name)
                        total_points.append(predicted_points[i])
                        points[position-1].append(int(predicted_points[i]))
                        cost = new_cost
                        players_teams[team-1] += 1
                j += 1
        print(f"Total team cost: {cost/10:1f}")
        print(players)
        print(points)
        print(sum(total_points))

        self.display_team(players, points)

    def display_team(self, players, points):
        print("\n\n\n")
        for position in players:
            print(" ".join(position), end="\n\n")


if __name__ == "__main__":
    init = InitialRound()

    x_train, t_train, x_test, t_test = init.gen_train_test()

    modules = [nn.Linear(21, 128),
               nn.ReLU(),
               nn.Linear(128, 128),
               nn.ReLU(),
               nn.Linear(128, 128),
               nn.ReLU(),
               nn.Linear(128, 1)]
    init.set_model(modules)

    init.train_torch(x_train, t_train, lr=1e-6, max_iter=10000)
    init.test(x_test, t_test)
    init.select_initial_team(formation="3-5-2")
