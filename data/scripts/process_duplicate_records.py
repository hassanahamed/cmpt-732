import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types


# add more functions as necessary

def main():
   
    posts = spark.read.orc("../post")
    postlinks = spark.read.orc("../postlink")



    postlinks = postlinks.filter(postlinks._LinkTypeId == 3)

    join_value = postlinks.alias('postlinks1').join(posts.alias('posts'), functions.col("postlinks1._PostId")== functions.col("posts._Id"), "inner").select(functions.col("posts._Title"), functions.col("postlinks1._RelatedPostId"))


    join2 = join_value.alias('join_value2').join(posts.alias('posts'), functions.col("posts._Id") == functions.col("join_value2._RelatedPostId"), "inner").dropDuplicates(["_Id"]).select(functions.col("join_value2._Title").alias("question1"), functions.col("posts._Title").alias("question2"))

    join2 = join2.withColumn("is_duplicate", functions.lit(True))
    join2 = join2.sample(False, 0.72, seed=0)
    join2.write.csv("../processed_data/is-duplicate-true", mode='overwrite')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()