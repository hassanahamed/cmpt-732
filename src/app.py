from datetime import date
import json
from urllib.request import urlopen
import streamlit as st
from wordcloud import WordCloud
import plotly.graph_objects as go
import pandas as pd
import dashboard_graph_helper as dh
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components

def main():

    st.title("Question Duplicacy")

    activities = ["Dashboard", "Question Match", "Question Search"]

    choices = st.sidebar.selectbox("Select Activities", activities)

    ## Here we need to show the page according to the section selected in sidembar. Each if corresponds to one page

    ## -------------------------------------------------------Dash board page start-------------------------------------------------------
    if choices == "Dashboard":
        
        
        stats = dh.get_dashboard_stats()

        

		# ------------------------------- Stats widget start----------------------------------------------
        indicators = go.Figure()

        indicators.add_trace(go.Indicator(
			value = stats[stats["name"] == "question"].values[0][0],
			title= {'text': "Total questions"},
			domain = {'row': 0, 'column': 0}))

        indicators.add_trace(go.Indicator(
			value = stats[stats["name"] == "duplicate_question"].values[0][0],
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
                x=tag_pd['tag'],
                y=tag_pd["count"],
                hovertemplate="%{y:.2f}",
                # showlegend=False,
                name="questions",
                # marker_color='#d0a9d9'
                
            ),
        )
        ## for total questions per tag
        fig4.add_trace(
            go.Bar(
                x=tag_pd["tag"],
                y=tag_pd["duplicate_count"],
                hovertemplate="%{y:.2f}",
                # showlegend=False,
                name="duplicate questions",
                # marker_color='#ebd43f'
            ),
        )

        fig4.update_layout(barmode="stack")
        fig4.update_layout(
            autosize=False,
            paper_bgcolor="#1f1d1d",
            plot_bgcolor="#1f1d1d",
            width=800,
            height=600,
            title="Questions to duplicate question ratio per tag",
        )
        st.plotly_chart(fig4)

        st.markdown("##")
        st.markdown("##")

        # ------------------------------- chart 1 ends----------------------------------------------

        # ------------------------------- chart 2 starts----------------------------------------------

        duplicate_posts = dh.get_duplicate_posts()
       
        
        fig = go.Figure(go.Scatter(x=duplicate_posts["closing_date_converted"], y=duplicate_posts["time_for_closure"]))

        fig.update_xaxes(
            rangeslider_visible=True,
            # tickformatstops=[
            #     # dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
            #     # dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
            #     # dict(dtickrange=[60000, 3600000], value="%H:%M m"),
            #     # dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
            #     dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
            #     dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
            #     dict(dtickrange=["M1", "M12"], value="%b '%y"),
            #     dict(dtickrange=["M12", None], value="%Y Y"),
            # ],
            rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
            )
        )

        fig.update_layout(
            xaxis_rangeselector_font_color='black',
                  xaxis_rangeselector_activecolor='red',
                  xaxis_rangeselector_bgcolor='green',
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

       

        countries_goe_json = dh.get_countries_goe_json()

        # data = [['France', 10], ['Germany', 22], ['Italy', 5], ['Poland',7], ['Spain',8], ['United Kingdom',21], ['India',21], ['Pakistan',21]] 
        # df_map = pd.DataFrame(data, columns = ['Country', 'count']) 

        df_map = dh.get_choroplethmapbox_data()


        fig9 = go.Figure(go.Choroplethmapbox(
            geojson=countries_goe_json,
            locations=df_map['country'],
            z=df_map['count'],
            colorscale="Viridis",
            # zmin=0,
            # zmax=500000,
            marker_opacity=0.5,
            marker_line_width=0,
            reversescale = True
            ))



        fig9.update_layout(
            mapbox_style="stamen-toner",
            mapbox_center={"lat": 46.8, "lon": 8.2},
            width=800,
            height=600,
            margin={"r": 0, "t": 0, "l": 0, "b": 0})
        
        st.plotly_chart(fig9)
	st.title("Tags_dashboard")
	st.text(" ")
	html_temp="""<script type='module' src='https://10az.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js'></script><tableau-viz id='tableau-viz' src='https://10az.online.tableau.com/t/nagendra1816/views/wordcloud_tags/Dashboard1' width='1000' height='800' hide-tabs toolbar='bottom' ></tableau-viz>"""
#html_temp="""https://10az.online.tableau.com/t/bigdatasfu/views/Big_Data/Dashboard1"""
	components.html(html_temp,width=1000,height=780)

	html_temp2="""<script type='module' src='https://10az.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js'></script><tableau-viz id='tableau-viz' src='https://10az.online.tableau.com/t/nagendra1816/views/wordcloud_tags/Sheet2' width='1000' height='800' hide-tabs toolbar='bottom' ></tableau-viz>"""
#html_temp="""https://10az.online.tableau.com/t/bigdatasfu/views/Big_Data/Dashboard1"""
	components.html(html_temp2,width=1000,height=780)

	html_temp3="""<script type='module' src='https://10az.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js'></script><tableau-viz id='tableau-viz' src='https://10az.online.tableau.com/t/nagendra1816/views/wordcloud_tags_dps/Sheet3' width='1000' height='800' hide-tabs toolbar='bottom' ></tableau-viz>"""
#html_temp="""https://10az.online.tableau.com/t/bigdatasfu/views/Big_Data/Dashboard1"""
	components.html(html_temp3,width=1000,height=780)

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
