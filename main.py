import streamlit as st
import streamlit.components.v1 as components

from tools.tools import *
from tools.plot_tools import *


# Description
st.image("./assets/cover.jpg")

st.title("Video Games Sales Dataset (1980-2016) 🎮")

with st.expander("Click to see the Dataset Description 🧾"):
	st.write(f"""
	## Dataset Description 🧾
	👉 There are **16 variables** in this dataset:
	*   **6 categorical** variables,
	*   **9 continuous** variables, and
	*   **1** variable to accomodate video game name.
	\\
	👉 The following is the **structure of the data set**.

	| Variable Name   | Description                                       | Sample Data                        |
	|-----------------|---------------------------------------------------|------------------------------------|
	| Name            | Title of video games                              | Super Mario Bros.; Wii Sports; ... |
	| Platform        | The platform of video games released              | 3DO; 3DS; ...                      |
	| Year_of_Release | Year of video games released                      | 1980 ; 2020; ...                   |
	| Genre           | Genre of video games                              | Action; Adventure; ...             |
	| Publisher       | Publisher of video games                          | Nintendo; Activision; ...          |
	| NA_Sales        | Video game sales in North America (in millions)   | 41.36; 29.08; ...                  |
	| EU_Sales        | Video game sales in Europe (in millions)          | 28.96; 3.58; ...                   |
	| JP_Sales        | Video game sales in Japan (in millions)           | 3.77; 6.81; ...                    |
	| Other_Sales     | Video game sales in other countries (in millions) | 8.45; 0.77; ...                    |
	| Global_Sales    | Total of worldwide sales                          | 82.53; 40.24; ...                  |
	| Critic_Score    | Score given by the media                          | 76; 82; ...                        |
	| Critic_Count    | Number of critics given by media                  | 51; 73; ...                        |
	| User_Score      | Score given by the video games user               | 8; 8.3; ...                        |
	| User_Count      | Number of critics given by the user               | 322; 709; ...                      |
	| Developer       | Video games developer                             | Nintendo; Ubisoft; ...             |
	| Rating          | Rating of video games based on ESRB ratings       | AO; E10+; ...                      |

	\\
	Dataset: https://www.kaggle.com/datasets/sidtwr/videogames-sales-dataset?datasetId=189386
""")

# Load the data
complete_data, all_years, all_titles = initial_config(
	"./data/Video_Games_Sales_as_at_22_Dec_2016.csv"
)

# Prep the sidebar
if not st.sidebar.checkbox("All years", value=True):
	year_of_release = st.sidebar.slider(
		label="Select a Release Year to deploy the data",
		min_value=1980,
		max_value=2016,
		value=2001
	)
else:
	year_of_release = "all"

# Clean the data
data = get_data_by_year(complete_data, year_of_release)
styled_data = format_df(data)

# Initial exploration
st.title("🗺️ Initial exploration ")
st.write("##### 🎈 You can use the slider in the sidebar section 👈 to change the year or to see the results of all years!")

# Database pre-visualization
st.write("""
	### 👀 Database pre-visualization
	This is an interactive table where you can see the latest 30 video games releases per year
""")
st.dataframe(styled_data)

st.write(f"""
	👉 There are {all_titles} unique video games title in the dataset.\\
	👉 If we get rid of the rows with no year of release we get {len(complete_data["Name"].unique())} titles, and this is usefull because all our stats are based on year of release (From now on, we will only work with the video game titles that has non NaN registers in the Year_of_Release column).\\
	👉 There are 31 different platforms of video games. And the distribution of these platforms is as follows
""")

# Platform visualization
count_platforms = data["Platform"].value_counts()
st.plotly_chart(histogram(count_platforms, count_platforms.index, 'Platform'))

st.write(f"""
	🎈 **PS2** is the most frequent Platform.

	👉 There are {len(complete_data['Publisher'].unique())} Publishers.\\
	👉 There are {len(complete_data['Developer'].unique())} Developer Companies.\\
	👉 There are {len(complete_data['Rating'].unique())} possible ratings for each game. This rating distribution is:
"""
)

# Ratings visualization
count_ratings = data["Rating"].value_counts()
st.plotly_chart(histogram(count_ratings, count_ratings.index, 'Rating'))
st.write("""
	🎈 There are not some ratings for some years.\\
	👉 **E** is the most frequent Rating.
""")

# Deeper Analysis
st.title("🦦 Deeper Analysis")
st.write("Here we develop some insights... 👀")

# Top 5 genres
st.write("## 🔝 Top 5 Genres")

genre_data = data['Genre'].value_counts()[:5]
st.plotly_chart(histogram(genre_data, genre_data.index, "Genre", color="#009A44"))
st.write("""
	👉 Action is the one of the most popular video game genre on the market independent from the year.
""")

# Top 5 platforms
st.write("## 🔝 Top 5 Platforms")

platform_data = data['Platform'].value_counts()[:5]
st.plotly_chart(histogram(platform_data, platform_data.index, "Platform", color="#009A44"))
st.write("""
	👉 Play Station is the most frequent through the years, followed by Xbox and the Ninendo Family.\\
	🎈 Fun fact: Before 1989 there was a platform called 2600 and it was dominating on video games platforms.
""")

# Top 10 Developers
st.write("## 🔝 Top 10 Developers \n.....")