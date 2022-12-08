import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types

# add more functions as necessary

def main():
    
    postLoc = "/mnt/d/Documents/GradSchool/Fall2022/CMPT732/Project/Data/post"
    dataLoc = "/mnt/d/Documents/GradSchool/Fall2022/CMPT732/Project/Data/processed_data/combined_data"

    data_schema = types.StructType([
        types.StructField('q1', types.StringType()),
        types.StructField('q2', types.StringType()),
        types.StructField('isDuplicate', types.BooleanType()),
    ])

    # # Create table of duplicate and non-duplicate single questions in the dataset -----------------------------------
    # # read in processed data with 'q1', 'q2' and flag 'isDuplicated'
    # data = spark.read.format("csv").option("header", "true").schema(data_schema).load(dataLoc)
    # data.cache()
    
    # # isDuplicate = True data
    # trueDup = data.filter(data['isDuplicate'] == True)
    # # combine the two columns of q1 and q2
    # trueQ1 = trueDup.select(trueDup['q1'])
    # trueQ2 = trueDup.select(trueDup['q2'])
    # trueQs = trueQ1.union(trueQ2).withColumnRenamed("q1", "TrueQ")
    # # only keep uniques
    # trueQs = trueQs.distinct()
    # # add the column of 'True'
    # trueQs_Final = trueQs.withColumn("isDuplicate", functions.lit("True"))    
    
    # # isDuplicate = False data
    # falseDup = data.filter(data['isDuplicate'] == False)
    # # combine the two columns of q1 and q2
    # falseQ1 = falseDup.select(falseDup['q1'])
    # falseQ2 = falseDup.select(falseDup['q2'])
    # falseQs = falseQ1.union(falseQ2).withColumnRenamed("q1", "FalseQ")
    # # only keep uniques
    # falseQs = falseQs.distinct()
    
    # # filter false - if a question is false and true (has a duplicate AND doesn't), its only true. Remove from False table.
    # falseQs_unique = falseQs.subtract(trueQs)
    # # add the column of 'False'
    # falseQs_Final = falseQs_unique.withColumn("isDuplicate", functions.lit("False"))

    # # combine True and False tables for the full filtered table of duplicate and non-duplicate single questions
    # data_final = trueQs_Final.union(falseQs_Final).withColumnRenamed('TrueQ', 'questions')
    # data_final.show()  

    # # Creating smaller post table of duplicates WITH postids and other necessary information ----------------------------------------------------------
    
    # # now import the original posts table and filter it to get the necessary details
    posts = spark.read.orc(postLoc)
    posts_filt = posts.select("_Title", "_Id", "_Tags")
    posts_filt.show()
    
    # posts_new = data_final.join(posts_filt, data_final["questions"] == posts_filt["_Title"])
    # # print(posts_new.count())
    # posts_new.show()

    # posts_new.write.json(saveTo, mode='overwrite')

    # # Using the filtered Posts table in json format and combining with the duplicate table ----------------------------------------------------------
    
    # # now import the original posts table and filter it to get the necessary details

    # posts = spark.read.json(saveTo)
    
            
    # joined = data_final.join(posts, data_final["questions"] == posts["_Title"])
    # # joined = joined.drop("_Title")
    # # print(joined.count())
    # joined.show()
    # # joined.write.json(save_full, mode='overwrite')

if __name__ == '__main__':

    spark = SparkSession.builder.appName('reddit_averages_df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()