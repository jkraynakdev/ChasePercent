import pandas as pd

class ChaseCalculator:
	def __init__(self, df):
		# setup the data frame
		self.df = df

		# Dict to connvert 'description' into swing/take
		self.SWINGCONVERTER = {'hit_into_play': 'swing',
						'foul': 'swing',
						'ball': 'take',
						'called_strike': 'take',
						'blocked_ball': 'take',
						'swinging_strike': 'swing',
						'swinging_strike_blocked': 'swing'}

	# Return a list of batter taking/swinging at pitch
	def get_swings(self, start: int, stop: int) -> list:
		swingList = []
		self.df['description'].iloc[start:stop].apply(lambda x: swingList.append(self.SWINGCONVERTER.get(x)))

		return swingList

	# Returns a list of strike zones for elements in start-stop inclusive
	def get_zone(self, start: int, stop: int) -> list:
		results = [[-.71, .71] for i in range(start, stop)]
		hor = []
		ver = []
		hor.append(self.df['sz_bot'].iloc[start:stop].apply(lambda x: x).values)
		ver.append(self.df['sz_top'].iloc[start:stop].apply(lambda x: x).values)
		for i in range(len(hor[0])):
			results[i].append(hor[0][i])
			results[i].append(ver[0][i])

		return results

	# returns wether a pitch should be called a strike or not
	def check_in_zone(self, x_cord: float, z_cord: float, zone: list) -> str:
		if((zone[0] <= x_cord) 
			and (zone[1] >= x_cord)
			and (zone[2] <= z_cord) 
			and (zone[3] >= z_cord)):

			return 'strike'
		else:

			return 'noStrike'

	# Itereates over start, stop and returns a list wether those pitches are in 
	# the zone or not
	def get_in_zone(self, start: int, stop: int) -> list:
		answers = []
		zones = self.get_zone(start, stop)
		x_cords = []
		z_cords = []


		x_cords.append(self.df['plate_x'].iloc[start:stop].apply(lambda x: x).values)
		z_cords.append(self.df['plate_z'].iloc[start:stop].apply(lambda x: x).values)

		x_cords, z_cords = x_cords[0], z_cords[0]

		for index in range(len(zones)):
			answers.append(self.check_in_zone(x_cords[index], z_cords[index], zones[index]))

		return answers

	# Returns the chase% 
	def chase_calc(self, swings: list, strikes: list) -> int:
		chaseList = []

		for i in range(len(swings)):
			if(swings[i] == 'swing' and strikes[i] == 'noStrike'):
				chaseList.append(1)
			else: 
				chaseList.append(0)

		return sum(chaseList)/len(chaseList)

	# Returns a list that describes were the batters change
	def get_len_id(self) -> list:
		lengths = self.df['batter'].value_counts().values
		for i in range(1, len(lengths)):		# mark
			lengths[i] = lengths[i] + lengths[i-1]

		return lengths

	# Returs the list of batter IDs
	def get_list_id(self) -> list:
		return self.df['batter'].unique()

	# Packages the data nicely into a dictionary
	def appendToDic(self) -> dict:
		listOfIds = self.get_list_id()
		lengthOfIds = self.get_len_id()

		start = 0
		playerChasePercent = {}

		for i in range(len(lengthOfIds)):
			swings = self.get_swings(start, lengthOfIds[i]-1)
			strikes = self.get_in_zone(start, lengthOfIds[i]-1)
			playerChasePercent[listOfIds[i]] = self.chase_calc(swings, strikes)
			start = lengthOfIds[i]-1

		return playerChasePercent

if __name__ == '__main__':
	df1 = pd.read_csv('Data/greaterThan3_sorted.csv', encoding="utf-8-sig")
	print(df1)
	#lessThanThree = ChaseCalculator(df1)