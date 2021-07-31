""" Fantasy Premier League AI Project

author: Even Marius Nordhagen
email: evenmn@mn.uio.no

This script gives the information provided by the
official Fantasy Premier League site. This includes
player IDs, player names, player positions, team,
and total points.

Statistics are provided by Vaastav Anand's great
Fantasy Premier League scraper.
"""

import pandas as pd


stats_dir = "~/Fantasy-Premier-League/data/"


class PlayerStats:
    """Statstics provided by Vaastav Anand's great 
    Fantasy Premier League scraper.

    season : int
        season ID (2016-2017 is 1617 and so on)
    player : int
        player ID
    """
    def __init__(self, season, player):
        # season
        assert season in [1920, 2021, 2122], "Given season is not available!"
        season = str(season)
        self.season_verb_repr = f"20{season[:2]}-{season[2:]}"
        self.season_dir = stats_dir + self.season_verb_repr + "/"
        # player
        self.player_id = player
        self.first_name, self.second_name = self.get_player_name()

    def get_player_name(self):
        """Get player name, given player ID. This is based on
        the 'season/player_idlist.csv' file
        """
        player_idlist_file = self.season_dir + "player_idlist.csv"
        players = pd.read_csv(player_idlist_file)
        player_ids = players['id']
        first_names = players['first_name']
        second_names = players['second_name']
        try:
            row_ind = player_ids.index[player_ids == self.player_id].to_list()[0]
        except IndexError:
            raise IndexError(f"No player with ID {self.player_id} found!")
        return first_names[row_ind], second_names[row_ind]

    def get_player_position_id(self):
        """Get player position id, given player ID. This is based 
        on the 'season/players_raw.csv' file
        """
        players_raw_file = self.season_dir + "players_raw.csv"
        players = pd.read_csv(players_raw_file)
        player_ids = players['id']
        position_ids = players['element_type']
        row_ind = player_ids.index[player_ids == self.player_id].to_list()[0]
        return position_ids[row_ind]

    def get_player_position(self):
        """Get player position, given player ID. 
        """
        positions = {1: "goalkeeper",
                     2: "defender",
                     3: "midfielder",
                     4: "forward"}
        position_id = self.get_player_position_id()
        return positions[position_id]

    def get_team_id(self):
        """Get the ID of team, given player ID. This is based
        on the 'season/players_raw.csv' file
        """
        players_raw_file = self.season_dir + "players_raw.csv"
        players = pd.read_csv(players_raw_file)
        player_ids = players['id']
        team_ids = players['team']
        row_ind = player_ids.index[player_ids == self.player_id].to_list()[0]
        return team_ids[row_ind]
    
    def get_team_name(self):
        """Get team name, given player ID. This is based on the
        'season/teams.csv' file
        """
        team_id = self.get_team_id()
        team_file = self.season_dir + "teams.csv"
        teams = pd.read_csv(team_file)
        team_ids = teams['id']
        name = teams['name']
        short_name = teams['short_name']
        row_ind = team_ids.index[team_ids == team_id].to_list()[0]
        return name[row_ind], short_name[row_ind]

    def get_current_price(self):
        """Get current price of player, given player ID. This
        is based on the 'season/players_raw.csv' file
        """
        players_raw_file = self.season_dir + "players_raw.csv"
        players = pd.read_csv(players_raw_file)
        player_ids = players['id']
        now_cost = players['now_cost']
        row_ind = player_ids.index[player_ids == self.player_id].to_list()[0]
        return now_cost[row_ind]


if __name__ == "__main__":
    # user-input
    season = 1920
    player_id = 300

    player = PlayerStats(season, player_id)
    first_name, second_name = player.get_player_name()
    position = player.get_player_position()
    team_name, team_name_short = player.get_team_name()

    print(f"{first_name} {second_name} plays for the Premier League club {team_name} ({team_name_short}) and is a {position}.")

    """ run example
    >>> player_information.py
    Mark Duffy plays for the Premier League club Sheffield Utd (SHU) and is a midfielder.
    """

