import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import year, datediff, col, to_date


# add more functions as necessary

def main():
   
    posts = spark.read.orc("posts")
    postlinks = spark.read.orc("postlink")

    posts = posts.filter(posts["_PostTypeId"] ==1)
    posts = posts.withColumn("year", year(posts["_CreationDate"]))

    postlinks = postlinks.filter(postlinks._LinkTypeId == 3)

    join_value = postlinks.alias('postlinks1').join(posts.alias('posts'), functions.col("postlinks1._PostId")== functions.col("posts._Id"), "inner").select('posts.*', col('postlinks1._CreationDate').alias("closing_date") )
    
    join_value = join_value.withColumn("time_for_closure", datediff(join_value["closing_date"], join_value["_CreationDate"]))

    join_value = join_value.withColumn("closing_date_converted", to_date(join_value["closing_date"]))

    join_value.select("closing_date_converted", "time_for_closure").groupBy("closing_date_converted").avg("time_for_closure").write.orc("duplicate-posts-closing-time", mode='overwrite')


    join_value.write.partitionBy("year").orc("duplicate-posts", mode='overwrite')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()