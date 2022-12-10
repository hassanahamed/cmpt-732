import json
import sys
from pathlib import Path
# sys.path.insert(0, 'D:\courses\big data\project\repo\cmpt-732\models\infer.py')
# sys.path.insert(1, 'D:\courses\big data\project\repo\cmpt-732\models\weaviate_search.py')
# sys.path.insert(1, '../models/weaviate_search.py')

import sys
sys.path.append('..')
from models.infer import setup,is_similar

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F

from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import year,col, asc,desc


spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
assert spark.version >= '3.0' # make sure we have Spark 3.0+
spark.sparkContext.setLogLevel('WARN')

# add more functions as necessary

def get_question_tag_count_data(year="All"):
   
    question_tags = spark.read.orc("../data/question-tags-count")
    duplicate_question_tags = spark.read.orc("../data/duplicate-question-tags-count")

    if year!="All":
        question_tags = question_tags.filter(question_tags["year"] == year)
        duplicate_question_tags = duplicate_question_tags.filter(duplicate_question_tags["year"] == year)
    

    top_question_tags = question_tags.groupBy("tag").sum("count").withColumnRenamed("sum(count)", "count").orderBy(col("count").desc()).limit(10)
    top_question_tags = top_question_tags.filter(top_question_tags["tag"]!="")
    duplicate_question_tags = duplicate_question_tags.groupBy("tag").sum("count").withColumnRenamed("sum(count)", "duplicate_count")

    return top_question_tags.join(duplicate_question_tags, top_question_tags["tag"]== duplicate_question_tags["tag"]).drop(duplicate_question_tags["tag"]).toPandas()

def get_dashboard_stats():

    stats = spark.read.json("../data/dashboard_stats")
    return stats.toPandas()


def get_duplicate_posts():

    posts = spark.read.orc("../data/duplicate-posts-closing-time")
    posts = posts.orderBy("closing_date_converted").withColumnRenamed("avg(time_for_closure)", "time_for_closure")
    return posts.toPandas()


def get_countries_goe_json():
     
    f = open('../data/countries.geojson')
    countries = json.load(f)

    for i in range(0,len(countries['features'])):
                countries['features'][i]['id'] = countries['features'][i]['properties']['ADMIN']
    
    return countries



def get_choroplethmapbox_data():

    countries = pd.read_json("../data/country_df.json")
    countries = countries.groupby('country')['count'].sum().reset_index()
    return countries

def get_top_5_questions(tag):

    top5 = spark.read.json("../data/top5/")
    top5= top5.filter(top5.New_Tags == tag).select(col("_Title").alias("Question"), col("_ViewCount").alias("ViewCount"))
    
    return top5.toPandas()



embed,sbert_model,nlp,fuzzy_scaler,wr_scaler,model=setup()

def check_similarity(question1,question2):
    pass
    is_duplicate = is_similar(question1,question2,embed,sbert_model,nlp,fuzzy_scaler,wr_scaler,model)
    return is_duplicate

   




if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    get_choroplethmapbox_data()

