import json
import sys
from pathlib import Path
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import year,col, asc,desc


# add more functions as necessary

spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
assert spark.version >= '3.0' # make sure we have Spark 3.0+
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext

def get_question_tag_count_data(year="All"):
   
    question_tags = spark.read.orc("../data/question-tags-count")
    duplicate_question_tags = spark.read.orc("../data/duplicate-question-tags-count")

    if year!="All":
        print("inside")
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



   




if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    get_duplicate_posts()

