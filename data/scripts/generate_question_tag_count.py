import re
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types


# add more functions as necessary

def words_once(tags):
    wordsep = re.compile(r'\<(.*?)\>')
    for w in wordsep.split(tags["_Tags"]):
        yield ((w,tags["year"]), 1)

def add(x, y):
    return x + y

def get_key(kv):
    return kv[1]

def output_format(kv):
    (tag,year), count = kv
    return tag , count, year

def main():
    
    tags_schema = types.StructType([
    types.StructField('tag', types.StringType(), True),
    types.StructField('count', types.IntegerType(),True),
    types.StructField('year', types.IntegerType(),True)
    ])

    posts = spark.read.orc("../posts-per-year")

    posts_with_tag_rdd = posts.select("_Tags", "year").rdd
    
    tags = posts_with_tag_rdd.flatMap(words_once)

    reduced_tags = tags.reduceByKey(add)

    ##sortBy(get_key, False) use it while aggregating
    structured_tags = reduced_tags.map(output_format)

    tags_df = spark.createDataFrame(structured_tags, schema = tags_schema)

    tags_df.write.partitionBy("year").orc("../question-tags-count", mode='overwrite')


   



if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()