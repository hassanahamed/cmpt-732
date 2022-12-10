import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import dashboard_graph_helper as dh
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components


def main():

    st.header("Duplicate question analysis and inference on \
        Stackoverflow data")

    activities = ["Dashboard", "Question Match", "Tableau Visualization"]

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
			value = 64155,
			title= {'text': "Total tags"},
			domain = {'row': 1, 'column': 0}))

        indicators.add_trace(go.Indicator(
			value = 19307021,
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

        st.write("While our model was trained on a balanced subset of the data, the full dataset, acquired from StackOverflow is heavily skewed. Only 3% of the posts are duplicate. \
        The dataset is distributed over 19 million users with 64,000 unique question tags.")
        st.markdown("##")
        st.markdown("##")

		# ------------------------------- Stats widget end----------------------------------------------


        # ------------------------------- chart 1 start----------------------------------------------

        left_column2, right_column = st.columns([1, 1])


        sources1 = ["Big Data", "Facebook", "Image Processing", "Machine Learning", "Python"]
        tag = left_column2.selectbox("Tags", sources1)

        top_5_df = dh.get_top_5_questions(tag)
        st.table(top_5_df)
        st.write("The table represent the top 5 questions for each selected tags: Facebook, Big Data, Image Processing, Machine Learning, Python based on view count.")
        st.markdown("##")
        st.markdown("##")

        # ------------------------------- chart 1 ends----------------------------------------------

        # ------------------------------- chart 2 starts----------------------------------------------

        
        left_column, right_column = st.columns([1, 1])

        # Widgets: selectbox
        sources = ["All", 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008]
        year = left_column.selectbox("Year", sources)

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

        st.write("In the full dataset, the Javascript tag was present in the largest number of questions. However, the C++ tag had the largest ratio of duplicate questions to questions asked - 5.3% of questions associated with C++ were duplicate. Over the last 3 years, PHP, Java and HTML have consistently been in the top 4 most duplicated tags. The percentage of duplicate questions for each of those three tags has been increasing over the last three years, further demonstrating the necessity of an automated system for detecting duplicate questions")

        st.markdown("##")
        st.markdown("##")
        st.markdown("##")
        

        # ------------------------------- chart 2 ends----------------------------------------------

        # ------------------------------- chart 3 starts----------------------------------------------

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
            width=800,
            height=600,
            title="Rate of marking question duplicate",
        )
        st.plotly_chart(fig)

        st.write("This time series chart demonstrates the rate at which questions are marked as duplicate. The outliers in the dataset (time to flagged duplicate > 400 hours) have grown more frequent between May 2019 and May 2020. It would be interesting to see if this increase in frequency continues over the upcoming years and keeps pace with the increased volume of duplicate questions.")

        st.markdown("##")
        st.markdown("##")


            # ------------------------------- chart 3 ends----------------------------------------------

            # ------------------------------- chart 4 starts----------------------------------------------
        

        left_column1, right_column1 = st.columns([1, 1])
        # Widgets: selectbox
        
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

        st.write("The USA, Germany and India are standouts for the volume of questions asked under the tags: ‘big data’ and ‘machine learning’. Each country is the leader in their respective continents for the number of questions asked. Accounting for the number of users in each country, (USA = 28312, India = 105626, Germany = 46966), we can see that the USA leads in the number of questions per user, followed by India and then Germany.")

        st.markdown("##")
        st.markdown("##")

     # ------------------------------- chart 4 ends----------------------------------------------

        

    ## -------------------------------------------------------Dash board page ends-------------------------------------------------------

    ## -------------------------------------------------------Question match page starts-------------------------------------------------------
    

        
    elif choices == "Question Match":
      
        question1 = st.text_input(
            "Question 1"
        )
        question2 = st.text_input(
            "Question 2"
        )
        if st.button("Submit"):  
            is_duplicate = dh.check_similarity(question1,question2)
            if is_duplicate:
                st.success("Both questions are similar")
            else:
                st.error("Both questions are different")
        
        st.markdown("##")
        st.markdown("##")

        test_qs = [["how to use transformers models","how to train hugging face transformers"],["What is derivative of Sigmoid function","how to differentiate sigmoid"],["What is derivative of Sigmoid function","how to differentiate tanh"],["how to live a healty life","where does heath ledger live"],["how to handle exception in java","heapoverflow exception occured in java"],["how to handle exception in java","heapoverflow exception occured in python"],["How does map reduce work","explain map reduce in hadoop"],["how to store data in s3","error while storing data in postgress"]]
        st.subheader("Example questions for inference")
        test_qs = pd.DataFrame(test_qs, columns = ['Question 1', 'Question 2'])
        st.table(test_qs)
           

    elif choices == "Tableau Visualization":
        st.text(" ")
        html_temp="""<script type='module' src='https://10az.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js'></script><tableau-viz id='tableau-viz' src='https://10az.online.tableau.com/t/nagendra1816/views/wordcloud_tags/Dashboard1' width='1000' height='700' hide-tabs toolbar='bottom' ></tableau-viz>"""
    #html_temp="""https://10az.online.tableau.com/t/bigdatasfu/views/Big_Data/Dashboard1"""
        components.html(html_temp,width=1000,height=780)


            


## -------------------------------------------------------Question search page ends-------------------------------------------------------


if __name__ == "__main__":
    main()
