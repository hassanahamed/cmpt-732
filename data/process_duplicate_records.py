import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types


# add more functions as necessary

def main():
    # main logic starts here
    comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


    posts = spark.read.orc("post")
    postlinks = spark.read.orc("postlink")



    postlinks = postlinks.filter(postlinks._LinkTypeId == 3)

    join_value = postlinks.alias('postlinks1').join(posts.alias('posts'), functions.col("postlinks1._PostId")== functions.col("posts._Id"), "inner").select(functions.col("posts._Title"), functions.col("postlinks1._RelatedPostId"))


    join2 = join_value.alias('join_value2').join(posts.alias('posts'), functions.col("posts._Id") == functions.col("join_value2._RelatedPostId"), "inner").dropDuplicates(["_Id"]).select(functions.col("join_value2._Title").alias("question1"), functions.col("posts._Title").alias("question2"))

    join2 = join2.withColumn("is_duplicate", functions.lit(True))
    join2 = join2.sample(False, 0.72, seed=0)
    join2.write.csv("processed_data/is-duplicate-true", mode='overwrite')

    print(join2.count())

    
    # left_anti = posts.alias('posts').join(postlinks.alias('postlinks1'), functions.col("postlinks1._PostId")== functions.col("posts._Id"), "leftanti")

    

    # left_anti = left_anti.sample(False, 0.38, seed=0)

    # left_anti_join =  left_anti.alias('left_anti1').join(left_anti.alias('left_anti2'),None , "outer")

    

    # print("hello hassan 2", join2.count())


    

   


    # join2_value = join1_value.join(postlinks, functions.col("join1_value._PostId")== functions.col("posts._Id"), "inner")

    

    # for x in post_links_group_by.count().collect():
    #     if x.count>3:
    #         print(x)




if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()