import os
import glob
import pandas as pd

def concatenate(dir: str) -> None:
	os.chdir(dir)
	extension = 'csv'
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


	#combine all files in the list
	combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

	#export to csv
	combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

	print('Done concatinating')

def sortCSV(filename: str):
	csvData = pd.read_csv(filename)
	sortedData = csvData.sort_values(by=["batter"], 
	                    ascending=False)

	sortedData.to_csv(''+filename[:-4]+'_sorted.csv', index=False)

	print('Done sorting')

# Function to filter out the ids that do not shop up in filename 1
def filterOutIds(filename1: str, filename2: str) -> list:
	df1 = pd.read_csv(filename1, encoding="utf-8-sig")
	df2 = pd.read_csv(filename2, encoding="utf-8-sig")

	file1Ids = df1['batter'].unique()
	new_df1 = df1[df1['batter'].isin(df2['batter'])]
	new_df2 = df2[df2['batter'].isin(df1['batter'])]
	
	# Remove bad whitespace
	new_df1.columns = new_df1.columns.str.strip()
	new_df2.columns = new_df2.columns.str.strip()

	return [new_df1, new_df2]



if __name__ == '__main__':
	sortCSV('lessThan2.csv')
	sortCSV('greaterThan3.csv')
