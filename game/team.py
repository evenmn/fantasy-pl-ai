"""
Team base class
"""

#from player_information import PlayerStats
from players import Player

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
        assert len(keepers) == 2, "Exactly 2 keepers required!"
        assert len(defenders) == 5, "Exactly 5 defenders required!"
        assert len(midfielders) == 5, "Exactly 5 midfielders required!"
        assert len(forwards) == 3, "Exactly 3 forwards required!"
        assert len(bench) == 4, "4 players have to be on the bench!"
        self.season = season

        # ensure that all players are Player objects
        #positions = [keepers, defenders, midfielders, forwards]
        #for position in positions:
        #    for i in len(position):
        #        if isinstance(position[i], str):
        #            position[i] = Player(position[i])
                    
        self.keepers = keepers
        self.defenders = defenders
        self.midfielders = midfielders
        self.forwards = forwards

        self.players = keepers + defenders + midfielders + forwards
        self.positions = [keepers, defenders, midfielders, forwards]
        
        self.bench = bench
        self.captain = captain
        self.vice_captain = vice_captain

        self.check_player_existence()
        self.check_player_duplicate()
        self.check_players_on_bench()
        self.check_captains()

    def __str__(self):
        """Display team nicely
        """
        # names = self.get_names()
        # positions = self.get_positions()

        print("My team")

    def check_player_existence(self):
        """Assert that all player IDs link to actual players
        """
        from positions import names
        for i, position in enumerate(self.positions, start=1):
            for player in position:
                position_id = player.get_player_position_id(self.season)
                assert position_id == i, f"Position error for {player.name} ({names[position_id].lower()})"
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
            assert bench_player in self.players, f"Bench player {bench_player} is not among the listed players"
        print("All players on the bench are in the team")

    def check_captains(self):
        """Check is captain and vice captain are among players
        """
        assert self.captain in self.players, "Captain not among selected players!"
        assert self.vice_captain in self.players, "Vice captain not among selected players!"
        print("Captains approved")

    def get_names(self):
        """Get player names
        """
        names = []
        for player in self.players:
            names.append(player.name)
        return names

    def get_team_ids(self):
        """Get player team ids
        """
        team_ids = []
        for player in self.players:
            team_ids.append(player.get_team_id(self.season))
        return team_ids

    def get_team_cost(self, gameweek):
        """Get total player costs
        """
        total_cost = 0
        for player in self.players:
            total_cost += player.get_gameweek_price(self.season, gameweek)
        return total_cost

    def get_team_cost_gameweek(self, gameweek):
        """Get total player price at a certain gameweek
        """
        total_cost = 0
        for player in self.players:
            total_cost += player.get_gameweek_price(self.season, gameweek)
        return total_cost

    def get_team_points_gameweek(self, gameweek):
        """Get total player points at a certain gameweek
        """
        total_points = 0
        for player in self.players:
            total_points += player.get_gameweek_points(self.season, gameweek)
        return total_points

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

    ## Man United 2019-20
    # keepers
    deGea = Player("David de Gea")
    henderson = Player("Dean Henderson")
    keepers = [deGea, henderson]

    # defenders
    wanbissaka = Player("Aaron Wan-Bissaka")
    maguire = Player("Harry Maguire")
    lindelof = Player("Victor Lindelöf")
    shaw = Player("Luke Shaw")
    bailly = Player("Eric Bailly")
    defenders = [wanbissaka, maguire, lindelof, shaw, bailly]

    # midfielders
    matic = Player("Nemanja Matic")
    mctominay = Player("Scott McTominay")
    james = Player("Daniel James")
    martial = Player("Anthony Martial")
    pogba = Player("Paul Pogba")
    midfielders = [matic, mctominay, james, martial, pogba]

    # forwards
    greenwood = Player("Mason Greenwood")
    kane = Player("Harry Kane")
    rashford = Player("Marcus Rashford")
    forwards = [greenwood, kane, rashford]

    # bench
    bench = [henderson, bailly, greenwood, rashford]

    # captain and vice captain 
    captain = martial
    vice_captain = rashford

    manutd = Team("2019-20", keepers, defenders, midfielders, forwards, bench, captain, vice_captain)
    print(manutd.get_team_cost_gameweek(15))
    print(manutd.get_team_points_gameweek(15))
