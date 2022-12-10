import random
import sys
from threading import Thread
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import geocoder
from geopy.geocoders       import GoogleV3
from pyspark.sql.functions import year, datediff, col, udf
import pycountry
from pyspark.sql.types import StringType

import geograpy
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')




from pyspark.sql import SparkSession, functions, types

@udf(returnType=StringType()) 
def extract_country(address):
    try:
        places = geograpy.get_place_context(text=address)
        return str(places.countries[0])
    except:
        return ""


   

# add more functions as necessary

def main():
    
    posts = spark.read.orc("../posts-per-year")

    posts = posts.filter(col("_Tags").contains("bigdata") | col("_Tags").contains("machine-learning"))

    posts_grp_by = posts.groupBy("_OwnerUserId").count()

    users = spark.read.orc("../users-with-location")
    
    users = users.filter(col("_Location").isNotNull())
    users = users.filter(users["_Location"] != '')

    posts_with_users = posts_grp_by.join(users, posts_grp_by._OwnerUserId == users._Id)

    posts_with_users.write.json("../users-with-country", mode='overwrite')
    

    # posts_with_users_location = posts_with_users.withColumn("country", extract_country(col("_Location")))

    # posts_with_users_location.show()

    

    # posts_grp_by = posts.groupBy("_OwnerUserId").count()

    
    
    
    
    
    # users = spark.read.orc("../users-with-location")
    
    # users = users.filter(col("_Location").isNotNull())
    # users = users.filter(users["_Location"] != '')
    # print(users.count())
    # users = users.withColumn("country", extract_country(col("_Location")))

    # users = users.select('_AccountId', '_Id', '_Location', 'country')

    # users.write.orc("../users_with_country", mode='overwrite')

    # users.write.orc("../users-with-locationsss", mode='overwrite')

    # text = "United States (New York), United Kingdom (London)"
    # for country in pycountry.countries:
    #     if country.name in text:
    #         print(country.name)


   
    # places = geograpy.get_place_context(text="El Cerrito, CA")
    # print(places.countries[0])




if __name__ == '__main__':
    spark = SparkSession.builder.appName('reddit averages df').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()