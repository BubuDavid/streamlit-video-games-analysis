import plotly.express as px
import plotly.figure_factory as ff

def histogram(data, x, y, color="#86BC25"):
	fig = px.histogram(
		data,
		x,
		y,
		color_discrete_sequence = [color]
	)

	fig.update_xaxes(title_text=y)
	fig.update_yaxes(title_text='Count')

	return fig