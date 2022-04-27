import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

def histogram(data, x, y, color):
	fig = px.histogram(
		data,
		x,
		y,
		color_discrete_sequence = [color]
	)

	fig.update_xaxes(title_text=y)
	fig.update_yaxes(title_text='Total')

	return fig

def create_hist(data, column_name, top=None, color="#86BC25"):
	count_variable = data[column_name].value_counts()[:top]
	return st.plotly_chart(histogram(
		count_variable, 
		count_variable.index, 
		column_name,
		color
	))


def plot_simple_line(data, column_name, entity, title, color="#86BC25"):
	selected_data = data[data[column_name] == entity]

	y = []
	x = []
	for i in range(int(selected_data["Year_of_Release"].min()), int(selected_data["Year_of_Release"].max()+1)):
		y.append(selected_data.loc[
			selected_data["Year_of_Release"] == i, 'Global_Sales'
		].sum())
		x.append(i)

	print(y)

	fig = px.line(
		x=x,
		y=y,
		title=title,
		color_discrete_sequence = [color],
		markers=True
	)


	fig.update_xaxes(title_text="Year of Release")
	fig.update_yaxes(title_text="Global Sells")

	for i, j in zip(x, y):
		if j == max(y):
			max_year = i

	return st.plotly_chart(fig), max_year, max(y)