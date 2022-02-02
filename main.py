from swingCalculator import ChaseCalculator
from stats_helper import Stats
from csvFileEditor import filterOutIds
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy

# Function that takes to dataframes and returns the change in
# chase percent for each id
def get_delta_chase(df_before, df_after) -> dict:
	calculator_before = ChaseCalculator(df_before)
	calculator_after = ChaseCalculator(df_after)

	delta_chase = {}

	dict1 = calculator_before.append_to_dic()
	dict2 = calculator_after.append_to_dic()

	# clumsy but still O(n)
	for key, value in dict2.items(): 
		delta_chase[key] = value

	for key, value in dict1.items():
		delta_chase[key] -= value

	return delta_chase


# Returns a dictionary containing wobas for player IDs
def get_wobas(df) -> dict:
	# Does not matter which calculator we use since player ids are equal
	calculator_before = ChaseCalculator(df)
	dict1 = calculator_before.append_to_dic()

	woba_calculator = Stats(df, list(dict1.keys()))

	# stores a dict of players wobas indexed by (id, woba)
	wobas = woba_calculator.get_player_woba()

	return wobas

# Returns a list with [chase%, wOBA]
def pair_up_ids(delta_chase: dict, wobas: dict) -> list:
	paired_up_stats = []
	for key, value in delta_chase.items():
		paired_up_stats.append([value, wobas[key]])
	return paired_up_stats

# career_chase is smaller, so start with that, but fix this later
def weighted_delta_chase(delta_chase: dict, career_chase: dict) -> dict:
	weighted_chase = {}
	for key, value in career_chase.items():
		weighted_chase[key] = delta_chase[key]/career_chase[key]

	return weighted_chase

def run_regression(delta_chase: dict, wobas: dict) -> None:
	paired_up_stats = pair_up_ids(delta_chase, wobas)
	x_values = []
	y_values = []

	for item in paired_up_stats:
		x_values.append(item[0])
		y_values.append(item[1])

	regression = sm.OLS(x_values, y_values, missing='drop').fit()
	print(regression.summary())


# Data visualization function
def build_graph(dict1, dict2) -> None:
	swingGreat = pd.DataFrame(dict1.items(), columns=['Battter', 'Chase'])
	swingLess = pd.DataFrame(dict2.items(), columns=['Battter', 'Chase'])

	plt.title('Batter Chase\% >= 3 Times Through')
	plt.hist(swingGreat['Chase'], bins=60)
	plt.axvline(swingGreat['Chase'].mean(), color='k', linestyle='dashed', linewidth=1)

	plt.xlabel('chase%')
	plt.ylabel('number of batters')

	plt.show()


# Testing purposes
if __name__ == '__main__':

	filename1, filename2 = 'Data/lessThan2_sorted.csv', 'Data/greaterThan3_sorted.csv'

	df1, df2 = filterOutIds(filename1, filename2)[0], filterOutIds(filename1, filename2)[1]
	
	delta_chase = get_delta_chase(df1, df2)
	player_woba = get_wobas(df1)


	calculator1 = ChaseCalculator(df1)
	calculator2 = ChaseCalculator(df2)




	dict1 = calculator1.append_to_dic()
	dict2 = calculator2.append_to_dic()

	df3 = pd.read_csv('Data/fangraphs_stats.csv')
	stats = Stats(df3, list(dict1.keys()))
	stats.get_chase()
	chase_dic = stats.chase



	#print(weighted_delta_chase(delta_chase, chase_dic))
	#print(run_regression(weighted_delta_chase(delta_chase, chase_dic),player_woba))


	# Run pearson R test
	#print(scipy.stats.pearsonr(list(delta_chase.values()), list(player_woba.values())))

	# Run wilcoxon		
	#print(scipy.stats.wilcoxon(list(dict1.values()), list(dict2.values())))

