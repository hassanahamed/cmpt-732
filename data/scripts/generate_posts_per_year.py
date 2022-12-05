import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql.functions import year

from pyspark.sql import SparkSession, functions, types


# add more functions as necessary

def main():

    ## TODO check again with hardisk post folder
    
    posts = spark.read.orc("../post")

    posts = posts.filter(posts["_PostTypeId"] ==1)

    posts = posts.withColumn("year", year(posts["_CreationDate"]))

    posts.write.partitionBy("year").orc("../posts-per-year", mode='overwrite')



if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()