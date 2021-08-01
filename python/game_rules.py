"""Here, we implement the rules of Fantasy Premier League
"""


def validate_team(team, budget):
    """Check if team follows the Fantasy PL rules:
        - Accepted formations are 4-3-3, 4-4-2, 4-5-1, 3-4-3, 3-5-2
        - Maximum three players from each club is allowed
        - The total price of players cannot exceed 100M
    """

    def validate_formation(team):
        """Validate formation. Accepted formations are 4-3-3, 4-4-2, 
        4-5-1, 3-4-3, 3-5-2. 
        """
        valid_bench_positions = [[1, 2, 3, 3],
                                 [1, 2, 3, 4],
                                 [1, 2, 4, 4],
                                 [1, 2, 2, 3],
                                 [1, 2, 2, 4]]
        bench_positions = []
        for player in team.bench:
            bench_positions.append(player.get_player_position_id(team.season))
        assert sort(bench_positions) in valid_bench_positions, "Formation not approved!"
        print("Formation approved")

    def validate_player_team(team):
        """Maximum three players can be picked from each team
        """
        team_ids = team.get_team_ids()
        team_count = {i:team_ids.count(i) for i in team_ids}
        for duplicates in team_count.values():
            assert duplicates <= 3, "Found more than three players from a team"
        print("Player teams approved")

    def validate_player_costs(team, budget):
        """
        """
        total_cost = team.get_team_cost()
        assert total_cost <= budget, "Budget exceeded"
        print("Team cost is within budget")

    validate_formation(team)
    validate_player_team(team)
    validate_player_costs(team, budget)


def get_number_of_transfers(team1, team2):
    changes = list(set(team1.player_ids) - set(team2.player_ids))
    return len(changes)

def display_all_changes(team1, team2):
    changes = list(set(team1.player_ids) - set(team2.player_ids))
    return changes


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
    GAMEWEEKS = 38

    def __init__(self, team, chips):
        self.team = team
        self.chips = chips

        self.wildcard_played = False
        self.free_hit_played = False
        self.triple_cap_played = False
        self.bench_boost_played = False

        self.free_transfers = 1
        self.gameweek = 1

        self.money_bank = 1000
        self.total_player_value = 0

        self.total_points = 0
        self.points_current_round = 0
        self.total_transfers = 0

        validate_team(team)
        self.update_chips()

    def update_chips(self):
        """The chips played needs to be updated after action is performed
        (before every new gameweek)
        """
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
        self.total_points += team.get_team_points_gameweek(self.gameweek)
        self.gameweek += 1
        self.free_transfers += 1
        if self.free_transfers > MAX_FREE_TRANSFERS:
            self.free_transfers = MAX_FREE_TRANSFERS
        if self.gameweek == NEW_WILDCARD_GAMEWEEK:
            self.wildcard_played = False
        if self.gameweek > GAMEWEEKS:
            print("Game is over")

    def perform_actions(team, chips):
        """Update team and play chips
        """
        self.old_team = self.team
        self.team = team
        self.update_chips(chips)
        validate_team(team)

        num_transfers = get_number_of_transfers(self.team, self.old_team)

        num_nonfree_transfers = num_transfers - self.free_transfers

        self.free_transfers -= num_transfers
        if self.free_transfers < 0:
            self.free_transfers = 0

        total_transfer_cost = TRANSFER_COST * num_nonfree_transfers


if __name__ == "__main__":
    """
    Example: Playing with same team for entire season and
    do not play chips
    """

    from players import Player
    from team import Team

    season = "2020-21"

    ## team
    # keepers
    mccarthy = Player("Alex McCarthy")
    nyland = Player("Ørjan Nyland")
    keepers = [mccarthy, nyland]

    # defenders
    arnold = Player("Trent Alexander-Arnold")
    justin = Player("James Justin")
    stevens = Player("Enda Stevens")
    vinagre = Player("Rúben Gonçalo Silva Nascimento Vinagre")
    dallas = Player("Stuart Dallas")
    defenders = [arnold, justin, stevens, vinagre, dallas]

    # midfielders
    salah = Player("Mohamed Salah")
    aubameyang = Player("Pierre-Emerick Aubameyang")
    maddison = Player("James Maddison")
    stephens = Player("Dale Stephens")
    romeu = Player("Oriol Romeu Vidal")
    midfielders = [salah, aubameyang, maddison, stephens, romeu]

    # forwards
    kane = Player("Harry Kane")
    ings = Player("Danny Ings")
    mitrovic = Player("Aleksandar Mitrović")
    forwards = [kane, ings, mitrovic]

    bench = [nyland, stevens, romeu, mitrovic]
    captain = kane
    vice_captain = salah

    team = Team(season, keepers, defenders, midfielders, forwards, bench, captain, vice_captain)
    print("Initial team cost: ", team.get_team_cost_gameweek(1))

    ## chips
    wildcard = False
    free_hit = False
    triple_cap = False
    bench_boost = False
    chips = [wildcard, free_hit, triple_cap, bench_boost]

    ## play game
    game = FPL(team, chips)
    for _ in range(38):
        game.next_gameweek()
    print("Final points: ", game.total_points)    
