import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import year


# add more functions as necessary

def main():
   
    posts = spark.read.orc("posts")
    postlinks = spark.read.orc("postlink")

    posts = posts.filter(posts["_PostTypeId"] ==1)
    posts = posts.withColumn("year", year(posts["_CreationDate"]))

    postlinks = postlinks.filter(postlinks._LinkTypeId == 3)

    join_value = postlinks.alias('postlinks1').join(posts.alias('posts'), functions.col("postlinks1._PostId")== functions.col("posts._Id"), "inner").select('posts.*')

    join_value.write.partitionBy("year").orc("duplicate-posts", mode='overwrite')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()