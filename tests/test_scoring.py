import unittest

from prediction_framework.scoring import MatchContext, outsider_bonus_from_odds, score_prediction


class FootballScoringTest(unittest.TestCase):
    def setUp(self):
        self.context = MatchContext(
            home="Home",
            away="Away",
            outsider_team="Away",
            bonus_outsider=9,
            bonus_draw=4,
        )

    def test_exact_score(self):
        result = score_prediction(2, 0, 2, 0, self.context)

        self.assertEqual(result.base_points, 6)
        self.assertEqual(result.total_points, 6)
        self.assertTrue(result.exact_score)

    def test_correct_result_goal_difference(self):
        result = score_prediction(2, 0, 3, 1, self.context)

        self.assertEqual(result.base_points, 4)
        self.assertTrue(result.correct_goal_difference)

    def test_correct_result_winner_goals(self):
        result = score_prediction(2, 1, 2, 0, self.context)

        self.assertEqual(result.base_points, 4)
        self.assertTrue(result.correct_winner_goals)

    def test_correct_result_only(self):
        result = score_prediction(3, 0, 2, 0, self.context)

        self.assertEqual(result.base_points, 3)

    def test_outsider_bonus(self):
        result = score_prediction(0, 1, 0, 1, self.context)

        self.assertEqual(result.base_points, 6)
        self.assertEqual(result.bonus_points, 9)
        self.assertEqual(result.bonus_reason, "outsider")

    def test_draw_bonus(self):
        result = score_prediction(1, 1, 1, 1, self.context)

        self.assertEqual(result.base_points, 6)
        self.assertEqual(result.bonus_points, 4)
        self.assertEqual(result.bonus_reason, "draw")

    def test_multiplier(self):
        result = score_prediction(0, 1, 0, 1, self.context, multiplier=2)

        self.assertEqual(result.total_before_multiplier, 15)
        self.assertEqual(result.total_points, 30)

    def test_outsider_bonus_from_odds(self):
        bonus = outsider_bonus_from_odds(2.08, 3.75)

        self.assertEqual(bonus.outsider_side, "away")
        self.assertEqual(bonus.bonus_outsider, 5)
        self.assertEqual(bonus.bonus_draw, 2)


if __name__ == "__main__":
    unittest.main()

