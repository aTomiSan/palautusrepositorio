class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1 = player1_name
        self.player2 = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == self.player1:
            self.player1_score += 1
        else:
            self.player2_score += 1

    def get_score(self):
        if self.player1_score == self.player2_score:
            return self.draw() 
        elif self.player1_score >= 4 or self.player2_score >= 4:
            return self.advantage()
        else:
            return f"{self.score_in_text(self.player1_score)}-{self.score_in_text(self.player2_score)}"

    def draw(self): 
        if self.player1_score > 2:
            return "Deuce"
        return f"{self.score_in_text(self.player1_score)}-All"

    def advantage(self): 
        advantage = self.player1_score - self.player2_score
        if advantage == 1:
            return f"Advantage {self.player1}" 
        elif advantage == -1:
            return f"Advantage {self.player2}" 
        elif advantage >= 2:
            return f"Win for {self.player1}"
        else:
            return f"Win for {self.player2}"

    def score_in_text(self, score): 
        if score == 0:
            return "Love"
        elif score == 1:
            return "Fifteen"
        elif score == 2:
            return "Thirty"
        elif score == 3:
            return "Forty"
