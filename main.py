from swingCalculator import ChaseCalculator
import os
from csvFileEditor import filterOutIds
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


filename1, filename2 = 'Data/lessThan2_sorted.csv', 'Data/greaterThan3_sorted.csv'

if __name__ == '__main__':
	df1, df2 = filterOutIds(filename1, filename2)[0], filterOutIds(filename1, filename2)[1]
	calculator1=ChaseCalculator(df1)
	calculator2 = ChaseCalculator(df2)


	dict1 = calculator1.appendToDic()
	dict2 = calculator2.appendToDic()

	print(np.array(list(dict1.values())).mean())
	print(np.array(list(dict2.values())).mean())

	swingGreat = pd.DataFrame(dict1.items(), columns=['Battter', 'Chase'])
	swingLess = pd.DataFrame(dict2.items(), columns=['Battter', 'Chase'])


	#print(stats.f_oneway(swingLess['Chase'], swingGreat['Chase']))


	#print(stats.mannwhitneyu(swingLess['Chase'], swingGreat['Chase']))