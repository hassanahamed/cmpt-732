import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import pandas as pd

from pyspark.sql import SparkSession, functions, types

from pyspark.sql.functions import row_number,lit
from pyspark.sql.window import Window


# add more functions as necessary

def main():
    # main logic starts here


    posts_f = spark.read.orc("post")

    posts_f = posts_f.filter(posts_f._Title.isNotNull())
    emp_RDD = sc.emptyRDD()
    columns = types.StructType([types.StructField('question1', types.StringType(), False),
                        types.StructField('question2', types.StringType(), False),
                        types.StructField('question1Id', types.LongType(), False),
                        types.StructField('question2Id', types.LongType(), False)])
    


    posts = posts_f.sample(False, 0.2, seed=None).limit(200000)
    

    w = Window().orderBy(lit('A'))
    posts = posts.withColumn("row_num", row_number().over(w))
    posts = posts.select(posts["_Title"].alias("question1"), posts["_Id"].alias("id1"), posts["row_num"].alias("row1"))

    posts2 = posts_f.sample(False, 0.2, seed=None).limit(200000)

    w = Window().orderBy(lit('A'))
    posts2 = posts2.withColumn("row_num", row_number().over(w))
    posts2 = posts2.select(posts2["_Title"].alias("question2"), posts2["_Id"].alias("id2"), posts2["row_num"].alias("row2"))


    final = posts.join(posts2, posts["row1"] == posts2["row2"])

    final = final.withColumn("is_duplicate", functions.lit(False))
    final.write.csv("processed_data/is-duplicate-false", mode='overwrite')

    # posts.show()

    # postlinks = postlinks.filter(postlinks._LinkTypeId == 3)

    
   
    



if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()