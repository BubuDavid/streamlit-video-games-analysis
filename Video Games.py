import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

from tools.tools import *
from tools.plot_tools import *


# Description
st.image("./assets/cover.jpg")

st.title("Video Games Sales Dataset (1980-2016) 🎮")

with st.expander("🧾 Click to see the Dataset Description 🧾"):
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
st.sidebar.title("⚙️ Parameters ⚙️")

# Prep the sidebar
if not st.sidebar.checkbox("All years", value=True):
	year_of_release = st.sidebar.slider(
		label="Select a Release Year to deploy the data on the 🗺️ Initial exploration section",
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
	📝 There are {all_titles} unique video games title in the dataset.

	📝 If we get rid of the rows with no year of release we get **{len(complete_data["Name"].unique())}** titles, and this is usefull because all our stats are based on year of release **(From now on, we will only work with the video game titles that has non NaN registers in the Year_of_Release column)**.

	##### 👉 There are 31 different platforms of video games
""")

# Platform visualization
create_hist(data, 'Platform')

with st.expander("🎈 Click here to see the top 5 platforms 🎈"):
	# Top 5 platforms
	st.write("## 🔝 Top 5 Platforms")

	create_hist(
		data=data,
		column_name='Platform',
		top=5,
		color="#009A44"
	)

	st.write("""
		📝 Play Station is the most frequent through the years, followed by Xbox and the Ninendo Family.\\
		🎈 Fun fact: Before 1989 there was a platform called 2600 and it was dominating on video games platforms.
	""")

st.write(f"""
	##### 👉 There are {len(complete_data['Publisher'].unique())} Publishers. These are the top 10 👇
""")

create_hist(
	data=data,
	column_name='Publisher',
	top=10,
)

st.write(f"""
	##### 👉 There are {len(complete_data['Developer'].unique())} Developer Companies, top 10 👇
""")

create_hist(
	data=data,
	column_name='Developer',
	top=10,
)

st.write(f"""
	##### 👉 There are {len(complete_data['Genre'].unique())} different Genres
""")

count_variable = data['Genre'].value_counts()
fig = px.funnel(count_variable, x='Genre', y=count_variable.index, color_discrete_sequence = ["#087C01"])
fig.update_xaxes(title_text="Frequency of the Genre")
fig.update_yaxes(title_text=f"Genre")
st.plotly_chart(fig)

st.write(f"""
	🎈 Action is the one of the most popular video game genre on the market independent from the year.
""")

st.write(f"""
	##### 👉 There are {len(complete_data['Rating'].unique())} possible ratings for each game, if we ignore those rows that don't have rating or that are rated as rp (rating pending) we get 8. This rating distribution is:
""")

# Ratings visualization
rating_data = pd.read_csv('./data/Rating.csv')
fig = px.pie(rating_data, values='Distribution', names='Rating', title='Rating Distribution', hole=.3, color_discrete_sequence = ["#072700", "#004D00", "#087C01", "#00B30C", "#BAC6B9", "#A6ACA7", "#525751", "#000000"])

st.plotly_chart(fig)

st.write("""
	🎈 There are not some ratings for some years.\\
	📝 **E** is the most frequent Rating.
	📝 There are some ratings that we would not considerate
""")

# Deeper Analysis
st.title("🏢 Publisher Analytics")
# By Publisher Data
publisher_complete_data = pd.read_csv('./data/Sales por Publisher.csv')
games_per_publishers = pd.read_csv('./data/Recuento de Juegos por Publisher.csv')
st.write("### Select a publisher with the selector on the left sidebar 👈 to see some analysis")
st.sidebar.write("---")
selected_publisher = st.sidebar.selectbox(
	"Choose a publisher to see some analysis on the 🏢 Publisher section",
	complete_data['Publisher'].unique(),
	index=int(np.where(np.array(complete_data['Publisher'].unique()) == 'Nintendo')[0][0])
)

publisher_data = publisher_complete_data[
	publisher_complete_data["Publisher"] == selected_publisher
]

st.write(f""" 
	🎈 The total video games release (all years) for {selected_publisher} is: **`{
		int(games_per_publishers[games_per_publishers["Publisher"] == selected_publisher]["Recuento de Name"])
	}`** and the total sales are: **`{float(publisher_data.Sales)}`** million dollars
	##### 👉 The perfomance for {selected_publisher} through the years is:
""")


plot, max_year, max_sells = plot_simple_line(complete_data, 'Publisher', selected_publisher, f'Global sells per year for {selected_publisher}')

st.write(f""" 
	🎈 For {selected_publisher} the best year was on **`{max_year}`** with a total Global sells for **`{max_sells}`**

	##### 👉 Here we have their top 5 videogames that year
""")

selected_publisher_data = complete_data[
	complete_data["Publisher"] == selected_publisher
]
selected_publisher_year = selected_publisher_data[
	selected_publisher_data["Year_of_Release"] == max_year
]
selected_publisher_year.sort_values("Global_Sales", inplace=True, ascending=False)


fig = px.histogram(
	x=selected_publisher_year.Name[:6],
	y=selected_publisher_year.Global_Sales[:6],
	color_discrete_sequence = ["#86BC25"]
)

fig.update_xaxes(title_text="Video Game Name")
fig.update_yaxes(title_text=f"Global Sales for the year {max_year}")

st.plotly_chart(fig)


st.title("🦦 User Score Analytics")

# Sales por publisher por year
avg_usr_score_year_publisher_df = pd.read_csv(
	"./data/Avg User Score por Year y Publisher.csv"
)
fig = px.line(
	avg_usr_score_year_publisher_df,
	x='Year', 
	y='Promedio de User_Score', 
	color='Publisher', 
	title="Year by Average User Score for the Top 7 Publishers",
	color_discrete_sequence=["#072700", "#004D00", "#087C01", "#00B30C", "#BAC6B9", "#A6ACA7", "#525751", "#000000"]
)

st.plotly_chart(fig)


# Top 10 publishers with better user score
top10_publishers_user_score_df = pd.read_csv('./data/Top 10 Publishers with better user score.csv')

st.plotly_chart(px.histogram(
	top10_publishers_user_score_df,
	x="Publisher",
	y="User Score",
	color_discrete_sequence=["#86BC25"],
	title="Top 10 publishers with better user score"
))

# Top 10 Better Video Games per User Score
top10_videosgames_user_score = pd.read_csv('./data/Top 10 User Score.csv')
st.plotly_chart(px.histogram(
	top10_videosgames_user_score,
	x="Videogame Name",
	y="Average User Score",
	color_discrete_sequence=["#86BC25"],
	title="Top 10 video games with better user score"
))