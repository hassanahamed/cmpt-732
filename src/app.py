import streamlit as st 
from wordcloud import WordCloud
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def main():

	st.title("Question Duplicacy")


	activities = ["Dashboard","Question Match","Question Search"]

	choices = st.sidebar.selectbox('Select Activities',activities)

	## Here we need to show the page according to the section selected in sidembar. Each if corresponds to one page


	## -------------------------------------------------------Dash board page start-------------------------------------------------------
	if choices == 'Dashboard':

		

		left_column, right_column = st.columns([1, 1])

		# Widgets: selectbox
		sources = ["All","2018","2019","2020"]
		energy = left_column.selectbox("Year for graph1", sources)

		fig4 = go.Figure()
		## for duplicate questions per tag
		fig4.add_trace(
			go.Bar(
				y=["one","two","three"],
				x=[1,2,3,],
				hovertemplate="%{x:.2f}",
				# showlegend=False,
				name="duplicate",
				orientation="h",
			),
		)
		## for total questions per tag
		fig4.add_trace(
			go.Bar(
				y=["one","two","three"],
				x=[3,4,1],
				hovertemplate="%{x:.2f}",
				# showlegend=False,
				name="original",
				orientation="h",
			),
		)

		fig4.update_layout(barmode="stack")
		fig4.update_layout(
			paper_bgcolor="#bcbcbc",
			plot_bgcolor="#f9e5e5",
			width=800,
			height=600,
			title="Questions to duplicate question ratio per tag",
		)
		st.plotly_chart(fig4)



		left_column1, right_column1 = st.columns([1, 1])
		# Widgets: selectbox
		sources1 = ["All","2018","2019","2020"]
		energy = left_column1.selectbox("Year for graph2", sources1)

## -------------------------------------------------------Dash board page ends-------------------------------------------------------


	## -------------------------------------------------------Question match page starts-------------------------------------------------------
	elif choices == 'Question Match':
		with st.form("my_form"):
			question1 = st.text_area('Question 1', '''
		''')
			question2 = st.text_area('Question 2', '''
			''')
			
			st.form_submit_button(label="Submit", on_click=None, kwargs={"question1": question1, "question2": question2}, type="secondary")


	## -------------------------------------------------------Question match page ends-------------------------------------------------------


## -------------------------------------------------------Question search page starts-------------------------------------------------------
	elif choices == 'Question Search':
		st.subheader("Question Search")

## -------------------------------------------------------Question search page ends-------------------------------------------------------
if __name__ == '__main__':
	main()