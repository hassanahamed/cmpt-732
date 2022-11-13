from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from decimal import Decimal
appName = "Python Example - PySpark Read XML"
master = "local"

# Create Spark session
spark = SparkSession.builder \
    .appName(appName) \
    .master(master) \
    .getOrCreate()

schema = StructType([
    StructField('_id', IntegerType(), False),
    StructField('Count', StringType(), False),
    StructField('TagName', IntegerType(), False)
])

df = spark.read.format("xml") \
    .option("rowTag","tags").load("Tags.xml", schema = schema)

df.show()