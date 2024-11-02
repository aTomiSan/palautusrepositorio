from statistics_service import StatisticsService, SortBy
from player_reader import PlayerReader

def main(): 
    url = "https://studies.cs.helsinki.fi/nhlstats/2022-23/players.txt"
    stats = StatisticsService(PlayerReader(url))
    philadelphia_flyers_players = stats.team("PHI")
#    top_scorers = stats.top(10)

    top5 = stats.top(4, SortBy.ASSISTS) 
    compare = [] 
    for one in top5: 
        compare.append(str(one))
    print(compare)

"""     print("Philadelphia Flyers:")
    for player in philadelphia_flyers_players:
        print(player)

    print("Top point getters:")
    for player in top_scorers:
        print(player) """


if __name__ == "__main__":
    main()
