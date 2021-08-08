# Fantasy-PL-AI [WORK IN PROGRESS]
This repo consists of two packages: A Python implementation of Fantasy Premier League (FPL) game and an engine to play the game. To get real game statistics (player information, cost and points), [Vaastav Anand's great scraper](https://github.com/vaastav/Fantasy-Premier-League) is used.

The engine is based on Q-learning. The agent plays the recent seasons of FPL again and again with different teams and actions. The rules are never presented directly to the agent, but she is told if she tries to do something illegal. The environment state consists of all statistics provided by Vaastav Anand prior to a gameweek. This includes game impact, creativity, expected goals, expected assists, player status and upcoming fixtures for all players. 

## Game
The game is oriented around the three classes `Player`, `Team` and `FPL`, which create player, team and game objects respectively. 

### `Player`
The `Player` class takes a player name as input:
``` python
deGea = Player("David de Gea")
```
The player position and team name in a given season can be found by:
``` bash
>>> deGea.get_player_position("2019-20")
('goalkeeper', 'GK')
>>> deGea.get_team_name("2019-20")
('Man Utd', 'MUN')
```
This is assumed to be constant during a season. Additionally, one can get gameweek information like player cost and player points. 

### `Team`
The `Team` class takes 15 players as inputs, in addition to which players that are on the bench, captain and vice captain.
``` python
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

team = Team("2020-21", keepers, defenders, midfielders, forwards, bench, captain, vice_captain)
```
Similar to the `Player` class, one can get the cost and points of the team at a given gameweek:
``` python
print("Initial team cost: ", team.get_team_cost_gameweek(1))
```

### `FPL`
Last, the game class is initialized with an initial team and initial chips. For enery round, the actions one can perform is changing the team and playing chips. The simplest game one can play is to choose an initial team, and not do any actions:
``` python
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
```
If the user tries to perform an illegal action (total player cost exceeds the budget, too many players from a team etc..), an error message will appear. 

## License


