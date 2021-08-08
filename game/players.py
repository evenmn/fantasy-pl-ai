"""
Python Football Fantasy
"""

import difflib
import pandas as pd


################################
### GET OVERVIEW OF PLAYERS
################################

stats_dir = "~/Fantasy-Premier-League/data/"


def list_teams(season):
    """List teams from the 'season/teams.csv' file
    """
    teams_file = stats_dir + season + "/teams.csv"
    teams = pd.read_csv(teams_file)
    ids = teams['id']
    names = teams['name']
    short_names = teams['short_name']
    print("ID Name (Short name)\n" + 20*"-")
    for id, name, short_name in zip(ids, names, short_names):
        print(f"{id:>4}. {name:<16} ({short_name})")
    print("")


def list_positions():
    """List positions from positions.py
    file
    """
    from positions import names, short_names
    print("ID Name (Short name)\n" + 20*"-")
    for i in names.keys():
        print(f"{i:>4}. {names[i]:<16} ({short_names[i]})")
    print("")


def list_sort_opt(season):
    """List sorting options from the 'season/cleaned_players.csv'
    and eventually the 'season/players/<player>/gw.csv' files
    file. The latter might not be available.
    """
    cleaned_players_file = stats_dir + season + "/cleaned_players.csv"
    cleaned_players = pd.read_csv(cleaned_players_file)
    for col in cleaned_players.columns:
        print(col)


def list_players(team=None, position=None, sort="total_points"):
    """List players, filtered by team and position.

    Parameters:
    -----------
    team : str or int
        team, name, short name or ID
    position : str or int
        position, name, short name or ID
    sort : str
        sorting style. 'total_points' as default
    """
    # display sort, total points, cost
    pass


def search_player(player):
    """Search player by name
    """
    pass


##############################
### PLAYER CLASS
##############################

class Player:
    """Player base class. A player is identified by his name.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self, season):
        """String representation of player
        """
        position, pos_short = self.get_player_position(season)
        team, team_short = self.get_team_name(season)
        print(self.name.upper())
        print(f" - {position:<16} ({pos_short})")
        print(f" - {team:<16} ({team_short})")
        print("")

    def get_player_id(self, season):
        """
        """
        player_idlist_file = stats_dir + season + "/player_idlist.csv"
        players = pd.read_csv(player_idlist_file)
        ids = players['id']
        first_name = players['first_name']
        second_name = players['second_name']
        full_name = players['first_name'] + " " + players['second_name']
        try:
            row_ind = players.index[self.name == full_name].to_list()[0]
        except IndexError:
            matches = difflib.get_close_matches(self.name, list(full_name))
            raise IndexError(f"No player with name {self.name} exists, did you mean {matches}?")
        return ids[row_ind]


    def get_player_position_id(self, season):
        """Get player position id, given player ID. This is based 
        on the 'season/players_raw.csv' file
        """
        player_id = self.get_player_id(season)
        players_raw_file = stats_dir + season + "/players_raw.csv"
        players = pd.read_csv(players_raw_file)
        player_ids = players['id']
        position_ids = players['element_type']
        row_ind = player_ids.index[player_ids == player_id].to_list()[0]
        return position_ids[row_ind]

    def get_player_position(self, season):
        """Get player position, given player ID. 
        """
        from positions import names, short_names
        position_id = self.get_player_position_id(season)
        return names[position_id].lower(), short_names[position_id]

    def get_team_id(self, season):
        """Get the ID of team, given player ID. This is based
        on the 'season/players_raw.csv' file
        """
        player_id = self.get_player_id(season)
        players_raw_file = stats_dir + season + "/players_raw.csv"
        players = pd.read_csv(players_raw_file)
        player_ids = players['id']
        team_ids = players['team']
        row_ind = player_ids.index[player_ids == player_id].to_list()[0]
        return team_ids[row_ind]
    
    def get_team_name(self, season):
        """Get team name, given player ID. This is based on the
        'season/teams.csv' file
        """
        team_id = self.get_team_id(season)
        team_file = stats_dir + season + "/teams.csv"
        teams = pd.read_csv(team_file)
        team_ids = teams['id']
        name = teams['name']
        short_name = teams['short_name']
        row_ind = team_ids.index[team_ids == team_id].to_list()[0]
        return name[row_ind], short_name[row_ind]

    def get_current_price(self, season):
        """Get current price of player, given player ID. This
        is based on the 'season/players_raw.csv' file
        """
        players_raw_file = stats_dir + season + "/players_raw.csv"
        players = pd.read_csv(players_raw_file)
        player_ids = players['id']
        now_cost = players['now_cost']
        row_ind = player_ids.index[player_ids == self.player_id].to_list()[0]
        return now_cost[row_ind]

    def get_gameweek_price(self, season, gameweek):
        """Get player price at a certain gameweek
        """
        player_id = self.get_player_id(season)
        gw_file = stats_dir + season + f"/gws/gw{gameweek}.csv"
        stats = pd.read_csv(gw_file)
        player_ids = stats['element']
        price = stats['value']
        try:
            row_ind = player_ids.index[player_ids == player_id].to_list()[0]
            return price[row_ind]
        except IndexError:
            return 0


    def get_gameweek_points(self, season, gameweek):
        """Get player points at a certain gameweek
        """
        player_id = self.get_player_id(season)
        gw_file = stats_dir + season + f"/gws/gw{gameweek}.csv"
        stats = pd.read_csv(gw_file)
        player_ids = stats['element']
        points = stats['total_points']
        try:
            row_ind = player_ids.index[player_ids == player_id].to_list()[0]
            return points[row_ind]
        except IndexError:
            return 0


class Goalkeeper(Player):
    """Goalkeeper class
    """
    def get_player_position_id(self, season):
        position_id = super(Goalkeeper, self).get_player_position_id(season)
        assert position_id == 1, "Player is not a goalkeeper"
        return position_id
    
class Defender(Player):
    """Defender class
    """
    def get_player_position_id(self, season):
        position_id = super(Defender, self).get_player_position_id(season)
        assert position_id == 2, "Player is not a defender"
        return position_id

class Midfielder(Player):
    """Midfielder class
    """
    def get_player_position_id(self, season):
        position_id = super(Midfielder, self).get_player_position_id(season)
        assert position_id == 3, "Player is not a midfielder"
        return position_id

class Forward(Player):
    """Forward class
    """
    def get_player_position_id(self, season):
        position_id = super(Forward, self).get_player_position_id(season)
        assert position_id == 4, "Player is not a forward"
        return position_id


if __name__ == "__main__":
    # lists
    list_teams("2019-20")
    list_positions()
    list_sort_opt("2019-20")

    # players
    deGea = Goalkeeper("David de Gea")
    print(deGea.get_player_position("2019-20"))
    print(deGea.get_team_name("2019-20"))

    Xhaka = Player("Granit Xhaka")
    print(Xhaka.get_team_name("2020-21"))
