import pybaseball
import pandas as pd
import numpy as np


class Stats:
	def __init__(self, df, ids: list):
		self.df = df
		self.chase = {}
		self.ids = ids

		# df that contains the WOBA stuff
		self.stat_df = pd.read_csv('Data/stats.csv', encoding="utf-8-sig")

	# MLB player id to fangraphs player id
	def playerID_convertor(self) -> dict:
		id_convertor = pd.read_csv('Data/playerID_map.csv')
		id_map = {}

		# Not the cleanest solution, TODO fix later
		fangraph_ids = list(id_convertor[id_convertor['MLBID'].isin(self.ids)]['IDFANGRAPHS'].apply(lambda x: x))
		mlb_ids = list(id_convertor[id_convertor['MLBID'].isin(self.ids)]['MLBID'].apply(lambda x: x))

		for i in range(len(mlb_ids)):
			id_map[mlb_ids[i]] = fangraph_ids[i]

		return id_map 

	def get_chase(self) -> None:
		id_map = self.playerID_convertor()
		for id in list(id_map.keys()):
			# if there is an issue with data, i.e. empy chase percent, remove it
			cur_chase = self.df.loc[self.df['playerid'] == int(id_map[id])]['O-Swing%'].values.tolist()
			if len(cur_chase) != 0:
				# remove %, flatten, make into a float
				self.chase[id] = (float(cur_chase[0][:-1]) / 100)		

	def get_player_woba(self) -> dict:
		player_woba = {}

		for player_id in self.ids:
			player_woba[player_id] = self.stat_df[self.stat_df['player_id'] == player_id].apply(lambda x: x)['woba'].values[0]

		return player_woba


