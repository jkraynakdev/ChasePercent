import pandas as pd

class Get_Stats:
	def __init__(self, stats_filename, swing_dict):
		self.stat_df = pd.read_csv(stats_filename, encoding="utf-8-sig")
		self.swing_dict = swing_dict

	def get_player_woba(self) -> dict:
		player_woba = {}


		for player_id in self.swing_dict.keys():
			player_woba[player_id] = self.stat_df[self.stat_df['player_id'] == player_id].apply(lambda x: x)['woba'].values[0]

		return player_woba
