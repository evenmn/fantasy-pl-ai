# Fantasy-PL-AI [WORK IN PROGRESS]
This repo consists of two packages: A Python implementation of Fantasy Premier League (FPL) game and an engine to play the game. To get real game statistics (player information, cost and points), [Vaastav Anand's great scraper](https://github.com/vaastav/Fantasy-Premier-League) is used.

The engine is based on Q-learning. The agent plays the recent seasons of FPL again and again with different teams and actions. The rules are never presented directly to the agent, but she is told if she tries to do something illegal. The environment state consists of all statistics provided by Vaastav Anand prior to a gameweek. This includes game impact, creativity, expected goals, expected assists, player status and upcoming fixtures for all players. 

## License


