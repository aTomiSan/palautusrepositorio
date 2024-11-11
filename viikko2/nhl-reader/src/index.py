from rich.console import Console 
from rich.table import Table
from player import PlayerReader, PlayerStats 

console =  Console()

def create_table(nationality, season): 
    table = Table(title=f"Top scorers of {nationality} season {season}")
    table.add_column("name", justify="left", style="cyan")
    table.add_column("team", justify="left", style="purple")
    table.add_column("goals", justify="right", style="green")
    table.add_column("assists", justify="right", style="green")
    table.add_column("points", justify="right", style="green")
    return table 

def main():
    print()
    print("NHL statistics by nationality")
    print()
    season = console.input("Select season [purple][2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/][/]: ")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    print()
    print("Select nationality")
    nationality = console.input("[purple][AUT/CZE/AUS/SWE/GER/DEN/SUI/SVK/NOR/RUS/CAN/LAT/BLR/SLO/USA/FIN/GBR)][/]: ")
    print()
    while nationality != "":
        stats = PlayerStats(reader)
        players = stats.top_scorers_by_nationality(nationality)
        table = create_table(nationality, season) 
        for player in players:
            table.add_row(str(player.name), str(player.team), str(player.goals), str(player.assists), str(player.points))
        console.print(table)
        print()
        print("Select nationality")
        nationality = console.input("[purple][AUT/CZE/AUS/SWE/GER/DEN/SUI/SVK/NOR/RUS/CAN/LAT/BLR/SLO/USA/FIN/GBR)][/]: ")

if __name__ == "__main__":
    main()
