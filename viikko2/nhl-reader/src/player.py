import requests

class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.team = dict['team']
        self.goals = dict['goals']
        self.assists = dict['assists']
        self.points = self.goals + self.assists
        self.nationality = dict['nationality']
    
    def __str__(self):
        return "{:<20} {:3}  {:2} + {:2} = {:<3}".format(self.name, self.team, self.goals, self.assists, self.goals+self.assists)

class PlayerReader: 
    def __init__(self, url):
        self.players = []
        response = requests.get(url).json()
        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)

class PlayerStats: 
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nation): 
        stats = []
        for player in self.reader.players:
            if player.nationality == nation: 
                stats.append(player) 
        stats.sort(key=lambda player: player.points, reverse=True) 
        return stats