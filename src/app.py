import streamlit as st
from wordcloud import WordCloud
import plotly.graph_objects as go
import pandas as pd
import dashboard_graph_helper as dh

import matplotlib.pyplot as plt


def main():

    st.title("Question Duplicacy")

    activities = ["Dashboard", "Question Match", "Question Search"]

    choices = st.sidebar.selectbox("Select Activities", activities)

    ## Here we need to show the page according to the section selected in sidembar. Each if corresponds to one page

    ## -------------------------------------------------------Dash board page start-------------------------------------------------------
    if choices == "Dashboard":
		

		# ------------------------------- Stats widget start----------------------------------------------
        indicators = go.Figure()

        indicators.add_trace(go.Indicator(
			value = 1200,
			title= {'text': "Total questions"},
			domain = {'row': 0, 'column': 0}))

        indicators.add_trace(go.Indicator(
			value = 300,
			title= {'text': "Duplicate Questions"},
			domain = {'row': 0, 'column': 1}))

        indicators.add_trace(go.Indicator(
			value = 400,
			title= {'text': "Total tags"},
			domain = {'row': 1, 'column': 0}))

        indicators.add_trace(go.Indicator(
			value = 500,
			title= {'text': "Total Users"},
			domain = {'row': 1, 'column': 1}))

        indicators.update_layout(
			grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
			template = {'data' : {'indicator': [{
				'mode' : "number+gauge"}]
								}},
			grid_xgap=0.4,
    		grid_ygap=0.5)
        
        st.plotly_chart(indicators)

		# ------------------------------- Stats widget end----------------------------------------------


        # ------------------------------- chart 1 start----------------------------------------------
        left_column, right_column = st.columns([1, 1])

        # Widgets: selectbox
        sources = ["All", 2018, 2019, 2020]
        year = left_column.selectbox("Year for graph1", sources)

        tag_pd = dh.get_question_tag_count_data(year)


        fig4 = go.Figure()
        ## for duplicate questions per tag
        fig4.add_trace(
            go.Bar(
                y=tag_pd['tag'],
                x=tag_pd["count"],
                hovertemplate="%{x:.2f}",
                # showlegend=False,
                name="questions",
                orientation="h",
            ),
        )
        ## for total questions per tag
        fig4.add_trace(
            go.Bar(
                y=tag_pd["tag"],
                x=tag_pd["duplicate_count"],
                hovertemplate="%{x:.2f}",
                # showlegend=False,
                name="duplicate questions",
                orientation="h",
            ),
        )

        fig4.update_layout(barmode="stack")
        fig4.update_layout(
            autosize=False,
            paper_bgcolor="#1f1d1d",
            plot_bgcolor="#1f1d1d",
            width=1800,
            height=1600,
            title="Questions to duplicate question ratio per tag",
        )
        st.plotly_chart(fig4)

        st.markdown("##")
        st.markdown("##")

        # ------------------------------- chart 1 ends----------------------------------------------

        # ------------------------------- chart 2 sratrs----------------------------------------------

        df = pd.read_csv(
            "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv"
        )

        fig = go.Figure(go.Scatter(x=df["Date"], y=df["mavg"]))

        fig.update_xaxes(
            rangeslider_visible=True,
            tickformatstops=[
                dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
                dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
                dict(dtickrange=[60000, 3600000], value="%H:%M m"),
                dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
                dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
                dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
                dict(dtickrange=["M1", "M12"], value="%b '%y M"),
                dict(dtickrange=["M12", None], value="%Y Y"),
            ],
        )

        fig.update_layout(
            autosize=False,
            paper_bgcolor="#1f1d1d",
            # plot_bgcolor="#1f1d1d",
            width=1500,
            height=900,
            title="Rate of marking question duplicate",
        )
        st.plotly_chart(fig)

        st.markdown("##")
        st.markdown("##")

        # ------------------------------- chart 2 ends----------------------------------------------

        left_column1, right_column1 = st.columns([1, 1])
        # Widgets: selectbox
        sources1 = ["All", "2018", "2019", "2020"]
        energy = left_column1.selectbox("Year for graph2", sources1)

    ## -------------------------------------------------------Dash board page ends-------------------------------------------------------

    ## -------------------------------------------------------Question match page starts-------------------------------------------------------
    elif choices == "Question Match":
        with st.form("my_form"):
            question1 = st.text_area(
                "Question 1",
                """
		""",
            )
            question2 = st.text_area(
                "Question 2",
                """
			""",
            )

            st.form_submit_button(
                label="Submit",
                on_click=None,
                kwargs={"question1": question1, "question2": question2},
                type="secondary",
            )

    ## -------------------------------------------------------Question match page ends-------------------------------------------------------

    ## -------------------------------------------------------Question search page starts-------------------------------------------------------
    elif choices == "Question Search":
        st.subheader("Question Search")


## -------------------------------------------------------Question search page ends-------------------------------------------------------
if __name__ == "__main__":
    main()
