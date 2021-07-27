"""Here, we implement the rules of Fantasy Premier League
"""


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
    """Actions:
        - Transfer players (15 player IDs)
        - Choose captain (1 player ID)
        - Choose vice captain (1 player ID)
        - Play chips (4 booleans)
    """

    def __init__(self, players, bench, captain, vice_captain):
        self.players = players
        self.bench = bench
        self.captain = captain
        self.vice_captain = vice_captain

        assert len(players) == 15, "15 players required!"
        assert len(bench) == 4, "4 players have to be on the bench!"

        self.check_player_existence()
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
        for player in self.players:
            try:
                # call vaasev
            except:
                raise ValueError(f"No player with ID {player} found!")
        print("All players exist")

    def check_player_duplicate(self):
        pass

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
        


def validate_team(team, budget):
    """Check if team follows the Fantasy PL rules:
        - Each team contains:
            -> 2 keepers
            -> 5 defenders
            -> 5 midfielders
            -> 3 forwards
        - Accepted formations are 4-3-3, 4-4-2, 4-5-1, 3-4-3, 3-5-2
        - Maximum three players from each club is allowed
        - The total price of players cannot exceed 100M
    """

    def validate_players(team):
        """Ensure that there are 2 keepers, 5 defenders,
        5 midfielders and 3 forwards
        """
        expected_positions = ["k", "k", "d", "d", "d", "d", "d",
                              "m", "m", "m", "m", "m", "f", "f", "f"]
        positions = team.get_positions()
        assert sort(positions) == sort(expected_positions), "..."
        print("All positions are filled correctly")

    def validate_formation(team):
        pass 

    def validate_player_team(team):
        pass

    def validate_player_costs(team, budget):
        """
        """
        costs = team.get_costs()
        assert costs <= budget, "Budget exceeded"


def get_number_of_transfers(team1, team2):
    pass

def display_all_changes(team1, team2):
    pass


class FPL:
    """FPL game

    One round state consists of a team and chips. The team
    is defined by the Team class above. The chips are given
    in the following order:
        - Wildcard (w)
        - Free hit (f)
        - Triple captain (t)
        - Bench boost (b)
    """

    MAX_FREE_TRANSFERS = 2
    TRANSFER_COST = 4
    NEW_WILDCARD_GAMEWEEK = 20

    def __init__(self, team, chips):
        self.team = team
        self.chips = chips

        self.wildcard_played = False
        self.free_hit_played = False
        self.triple_cap_played = False
        self.bench_boost_played = False

        self.free_transfers = 1
        self.gameweek = 1

        validate_team(team)
        self.update_chips()

    def update_chips(self):
        assert count(self.chips, True) <= 1, "Only one chip can be played at once"

        if self.chips[0] is True:
            assert self.wildcard_played is False, "Wildcard is already played"
            self.wildcard_played = True
        if self.chips[1] is True:
            assert self.free_hit_played is False, "Free hit is already played"
            self.free_hit_played = True
        if self.chips[2] is True:
            assert self.triple_cap_played is False, "Triple captain is already played"
            self.triple_cap_played = True
        if self.chips[3] is True:
            assert self.bench_boost_played is False, "Bench boost is already played"
            self.bench_boost_played = True

    def next_gameweek(self):
        self.gameweek += 1
        self.free_transfers += 1
        if self.free_transfers > MAX_FREE_TRANSFERS:
            self.free_transfers = MAX_FREE_TRANSFERS
        if self.gameweek == NEW_WILDCARD_GAMEWEEK:
            self.wildcard_played = False

    def perform_action(team, chips):
        self.old_team = self.team
        self.team = team
        self.update_chips(chips)

        num_transfers = get_number_of_transfers(self.team, self.old_team)

        num_nonfree_transfers = num_transfers - self.free_transfers

        self.free_transfers -= num_transfers
        if self.free_transfers < 0:
            self.free_transfers = 0

        total_transfer_cost = TRANSFER_COST * num_nonfree_transfers

        


def __name__ == "__main__":
    team1 = Team([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [12, 13, 14, 15], 1, 2)
    validate_team(team1)

    team2 = Team([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16], [12, 13, 14, 16], 1, 2)
    validate_team(team2)

    num_transfers = get_number_of_transfers(team1, team2)
