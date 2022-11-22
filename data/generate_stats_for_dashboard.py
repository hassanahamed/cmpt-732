import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types


# add more functions as necessary

def main():
    
    # todo write later

    data = []
    dict_schema = types.StructType([
    types.StructField('name', types.StringType(), True),
    types.StructField('count', types.IntegerType(),True)
    ])
    posts = spark.read.orc("posts")
    data.append(("question", posts.count()))


    postlinks = spark.read.orc("postlink")

    postlinks = postlinks.filter(postlinks._LinkTypeId == 3)

    duplicate_posts = postlinks.alias('postlinks1').join(posts.alias('posts'), functions.col("postlinks1._PostId")== functions.col("posts._Id"), "inner").select(functions.col("posts._Title"), functions.col("postlinks1._RelatedPostId"))

    data.append(("duplicate_question", duplicate_posts.count()))








    writing_df = spark.createDataFrame(data=data, schema = dict_schema)
    writing_df.write.json("dashboard_stats", mode='overwrite')

    # posts = posts.filter


    # result = posts.select("question1","question2","is_duplicate").union(postlinks.select("question1","question2","is_duplicate"))

    # result.write.csv("processed_data/combined_data", mode='overwrite')



   



if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()