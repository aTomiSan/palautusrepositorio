import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_pelaajahaku_toimii(self): 
        player = self.stats.search("Gretzky")
        self.assertEqual(str(player), "Gretzky EDM 35 + 89 = 124")

    def test_pelaajahaku_pelaajaa_ei_löydy(self): 
        player = self.stats.search("Kekkonen")
        self.assertEqual(player, None)

    def test_team_toimii(self): 
        pit = self.stats.team("PIT") 
        self.assertEqual(str(pit[0]), "Lemieux PIT 45 + 54 = 99")

    def test_top_points_toimii(self): 
        top_list = ["Gretzky EDM 35 + 89 = 124",
                    "Lemieux PIT 45 + 54 = 99",
                    "Yzerman DET 42 + 56 = 98",
                    "Kurri EDM 37 + 53 = 90",
                    "Semenko EDM 4 + 12 = 16"]
        top5 = self.stats.top(4, SortBy.POINTS) 
        compare = [] 
        for one in top5: 
            compare.append(str(one))
        self.assertEqual(compare, top_list)

    def test_top_goals_toimii(self): 
        top_list = ["Lemieux PIT 45 + 54 = 99",
                    "Yzerman DET 42 + 56 = 98",
                    "Kurri EDM 37 + 53 = 90",
                    "Gretzky EDM 35 + 89 = 124",
                    "Semenko EDM 4 + 12 = 16"]
        top5 = self.stats.top(4, SortBy.GOALS) 
        compare = [] 
        for one in top5: 
            compare.append(str(one))
        self.assertEqual(compare, top_list)

    def test_top_assists_toimii(self): 
        top_list = ["Gretzky EDM 35 + 89 = 124",
                    "Yzerman DET 42 + 56 = 98",
                    "Lemieux PIT 45 + 54 = 99",
                    "Kurri EDM 37 + 53 = 90",
                    "Semenko EDM 4 + 12 = 16"]
        top5 = self.stats.top(4, SortBy.ASSISTS) 
        compare = [] 
        for one in top5: 
            compare.append(str(one))
        self.assertEqual(compare, top_list)
