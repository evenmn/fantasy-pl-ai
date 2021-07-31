"""
Team base class
"""

from player_information import PlayerStats

class Team:
    """Football team class. Contains information about
        - Players
        - Formation
        - Captain
        - Vice captain

    Parameters:
    ----------
    players : list
        list containing all player IDs (15)
    bench : list
        list containing all IDs of players on the bench (4)
    captain : int
        ID of captain
    vice_captain : int
        ID of vice captain
    """

    def __init__(self, season, keepers, defenders, midfielders, forwards, bench, captain, vice_captain):
        self.season = season

        self.keeper_ids = keepers
        self.defender_ids = defenders
        self.midfielder_ids = midfielders
        self.forward_ids = forwards

        self.player_ids = keepers + defenders + midfielders + forwards
        self.positions = [self.keeper_ids, self.defender_ids, self.midfielder_ids, self.forward_ids]
        
        self.bench = bench
        self.captain = captain
        self.vice_captain = vice_captain

        assert len(keepers) == 2, "Exactly 2 keepers required!"
        assert len(defenders) == 5, "Exactly 5 defenders required!"
        assert len(midfielders) == 5, "Exactly 5 midfielders required!"
        assert len(forwards) == 3, "Exactly 3 forwards required!"
        assert len(bench) == 4, "4 players have to be on the bench!"

        self.check_player_existence()
        self.check_player_duplicate()
        self.check_players_on_bench()
        self.check_captains()

    def __str__(self):
        """Display team nicely
        """
        names = self.get_names()
        positions = self.get_positions()

        print("My team")

    def check_player_existence(self):
        """Assert that all player IDs link to actual players
        """
        self.players = []
        for i, position in enumerate(self.positions, start=1):
            self.players.append([])
            for player_id in position:
                player = PlayerStats(self.season, player_id)
                position_id = player.get_player_position_id()
                assert position_id == i, "Position error"
                self.players[-1].append(player)
        print("All players exist")

    def check_player_duplicate(self):
        """Check if the same player is picked two or more times
        """
        for position in self.positions:
            assert len(set(position)) == len(position), "Player duplicated"
        print("No duplicates")

    def check_players_on_bench(self):
        """Assert that all players on bench also are among the players
        """
        for bench_player in self.bench:
            assert bench_player in self.player_ids, f"Bench player {bench_player} is not among the listed players"
        print("All players on the bench are in the team")

    def check_captains(self):
        """Check is captain and vice captain are among players
        """
        assert self.captain in self.player_ids, "Captain not among selected players!"
        assert self.vice_captain in self.player_ids, "Vice captain not among selected players!"
        print("Captains approved")

    def get_names(self):
        """Get player names
        """
        names = []
        for player in self.players:
            # call vaasev
            name = ""
            names.append(name)
        return names

    def get_teams(self):
        """Get player teams
        """
        teams = []
        for player in self.players:
            # call vaasev
            team = ""
            teams.append(team)
        return teams

    def get_costs(self):
        """Get player costs
        """
        costs = []
        for player in self.players:
            # call vaasev
            cost = ""
            costs.append(cost)
        return costs

    def get_positions(self):
        """Get player positions
        """
        positions = []
        for player in self.players:
            # call vaasev
            position = ""
            positions.append(position)
        return positions

    def get_customs(self, keyword):
        customs = []
        for player in self.players:
            # call vaasev
            custom = ""
            customs.append(custom)
        return customs


if __name__ == "__main__":
    season = 1920

    keepers = [14, 427]
    defenders = [2, 5, 6, 7, 10]
    midfielders = [541, 15, 16, 18, 20]
    forwards = [11, 13, 12]

    arsenal = Team(season, keepers, defenders, midfielders, forwards, [427, 10, 12, 13], 11, 12)
