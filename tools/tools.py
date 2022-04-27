from distutils.log import error
import os
import glob
import pandas as pd
from prometheus_client import delete_from_gateway

def initial_config(file_name):
	# Read the data
	df = pd.read_csv(file_name)
	all_titles = len(df['Name'].unique())
	# Sort the data by year
	df = df.sort_values("Year_of_Release")
	#Drop rows out of the range 1980-2016
	df.drop(df.index[
		df["Year_of_Release"] > 2016
	], inplace=True)
	df.dropna(
		subset=['Year_of_Release', "Name", "Genre"],
		inplace=True
	)
	# Get all the years in the data
	all_years = df["Year_of_Release"].unique()
	all_years = tuple(map(int, filter(
		lambda x: x in range(1000, 3000),
		all_years
	)))

	return df, all_years, all_titles

def merge_csv_files(in_name, out_name):
	extension = 'csv'
	all_filenames = [i for i in glob.glob('./data/{}/*.{}'.format(in_name, extension))]
	#combine all files in the list
	df = pd.concat([pd.read_csv(
		f,
		names=["name", "platform", "year_of_release", "gendre", "publisher", "developer", "rating"],
		engine="python", 
		sep=',', 
		quotechar='"', 
		error_bad_lines=False,
	) for f in all_filenames ])
	#export to csv
	df.to_csv( "merged_csv.csv", index=False, encoding='utf-8-sig')
	
	return df

def get_data_by_year(df, release_year):
	if release_year != "all":
		return df[df["Year_of_Release"] == release_year]
	else:
		return df

def format_df(df, n=100):
	return df.tail(n).style.format(subset=['Year_of_Release'], formatter="{:.0f}")