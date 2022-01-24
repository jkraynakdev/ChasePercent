from swingCalculator import ChaseCalculator
from getPlayerStats import Get_Stats
import os
from csvFileEditor import filterOutIds
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy

'''
	# correlation between  delta chase % and 
	#print(stats.f_oneway(swingLess['Chase'], swingGreat['Chase']))


	#print(stats.mannwhitneyu(swingLess['Chase'], swingGreat['Chase']))
'''

def get_delta_chase(df_before, df_after) -> dict:
	calculator_before = ChaseCalculator(df_before)
	calculator_after = ChaseCalculator(df_after)

	delta_chase = {}

	dict1 = calculator_before.appendToDic()
	dict2 = calculator_after.appendToDic()

	# clumsy but still O(n)
	for key, value in dict2.items(): 
		delta_chase[key] = value

	for key, value in dict1.items():
		delta_chase[key] -= value

	return delta_chase


def get_wobas(filename: str, df) -> dict:
	# Does not matter which calculator we use since player ids are equal
	calculator_before = ChaseCalculator(df)
	dict1 = calculator_before.appendToDic()

	woba_calculator = Get_Stats(filename, dict1)

	# stores a dict of players wobas indexed by (id, woba)
	wobas = woba_calculator.get_player_woba()

	return wobas

def pair_up_ids(delta_chase: dict, wobas: dict) -> dict:
	paired_up_stats = []
	for key, value in delta_chase.items():
		paired_up_stats.append([value, wobas[key]])
	return paired_up_stats


def run_regression(delta_chase: dict, wobas: dict) -> None:
	paired_up_stats = pair_up_ids(delta_chase, wobas)
	x_values = []
	y_values = []

	for item in paired_up_stats:
		x_values.append(item[0])
		y_values.append(item[1])

	regression = sm.OLS(x_values, y_values, missing='drop').fit()
	print(regression.summary())



def build_graph(dict1, dict2) -> None:
	swingGreat = pd.DataFrame(dict1.items(), columns=['Battter', 'Chase'])
	swingLess = pd.DataFrame(dict2.items(), columns=['Battter', 'Chase'])

	plt.title('Batter Chase\% >= 3 Times Through')
	plt.hist(swingGreat['Chase'], bins=60)
	plt.axvline(swingGreat['Chase'].mean(), color='k', linestyle='dashed', linewidth=1)

	plt.xlabel('chase%')
	plt.ylabel('number of batters')

	plt.show()

filename1, filename2 = 'Data/lessThan2_sorted.csv', 'Data/greaterThan3_sorted.csv'

if __name__ == '__main__':


	df1, df2 = filterOutIds(filename1, filename2)[0], filterOutIds(filename1, filename2)[1]
	
	delta_chase = get_delta_chase(df1, df2)
	player_woba = get_wobas('Data/stats.csv', df1)
	#run_regression(delta_chase, player_woba)


	calculator1=ChaseCalculator(df1)
	calculator2 = ChaseCalculator(df2)


	dict1 = calculator1.appendToDic()
	dict2 = calculator2.appendToDic()

	print(scipy.stats.pearsonr(list(dict1.values()), list(dict2.values())))


