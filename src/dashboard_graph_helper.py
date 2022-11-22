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
   




if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    get_question_tag_count_data()

