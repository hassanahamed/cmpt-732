# WSL environment variable setup
    # $ export PYSPARK_PYTHON=python3
    # $ export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
    # $ export SPARK_HOME=/mnt/c/spark-3.3.0-bin-hadoop3

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

spark = SparkSession.builder.appName('feature_analysis').getOrCreate()
assert spark.version >= '3.0' # make sure we have Spark 3.0+
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext

dataLoc = "/mnt/d/Documents/GradSchool/Fall2022/CMPT732/Project/Data/processed_data/combined_data"
plotDir = "/mnt/d/Documents/GradSchool/Fall2022/CMPT732/Project/Code/ProcessedDataPlots"

data_schema = types.StructType([
types.StructField('q1', types.StringType()),
types.StructField('q2', types.StringType()),
types.StructField('isDuplicate', types.BooleanType()),
])

data = spark.read.format("csv").option("header", "true").schema(data_schema).load(dataLoc)
data.cache()

# # Ratio of duplicated to non-duplicated questions -----------------------------------------------------------------------------------------------------
# count_type = data.groupby(data['isDuplicate']).count()
# duplicate_q = count_type.where(count_type['isDuplicate'] == 'true').collect()[0][1]
# only_q = count_type.where(count_type['isDuplicate'] == 'false').collect()[0][1]

# fig = plt.figure(figsize=(6,5))
# ax = fig.add_axes([0,0,1,1])
    
# dup_color = '#F8B195'
# unq_color = '#F67280'

# a = ax.bar('isDuplicate = true', duplicate_q, color=dup_color)
# b = ax.bar('isDuplicate = false', only_q, color=unq_color)

# ratio = duplicate_q/only_q

# ax.bar_label(a, [str(duplicate_q)])
# ax.bar_label(b, [str(only_q)])

# ax.bar_label(a, [str(round(ratio,3))], label_type='center')
# ax.bar_label(b, [str(1)], label_type='center')

# ax.set_ylabel('Number of entries')
# ax.set_title('Distribution of isDuplicate question pairs')

# plt.savefig(plotDir + '/isDuplicateDistribution.jpg', bbox_inches='tight')


# # Number of unique questions (are any questions repeated in any of the pairings?) ----------------------------------------------------------------------

# only_q1 = data.select(data['q1'])
# only_q2 = data.select(data['q2'])

# joined_qs = only_q1.union(only_q2).withColumnRenamed('q1', 'q1_q2')

# unique_qs = joined_qs.groupby(joined_qs['q1_q2']).count()
# unique_qs = unique_qs.orderBy(unique_qs['count'].desc()).withColumnRenamed('count', 'num_repeats')

# total_unique = unique_qs.count()

# repeats_count = unique_qs.groupby(unique_qs['num_repeats']).count()
# repeats_count = repeats_count.orderBy(repeats_count['num_repeats'].asc())
# repeats_count.cache()

# num_repeats = repeats_count.rdd.map(lambda x: x['num_repeats']).collect()
# count = repeats_count.rdd.map(lambda x: x['count']).collect()

# percent_of_total = [x*100/total_unique for x in count]
# percent_of_total = list(map(lambda x: "{:.3f}%".format(round(x,3)), percent_of_total))

# fig = plt.figure(figsize=(6,5))
# ax = fig.add_axes([0,0,1,1])

# bars = ax.bar(num_repeats, count, color=["#A8E6CE", "#DCEDC2", "#FFD3B5", "#FFAAA6", "#FF8C94"])
# ax.bar_label(bars, count, label_type='edge')

# iter = 0
# for bar in bars:
#     ax.annotate(
#         percent_of_total[iter],
#         xy=(0.5, 0.5),
#         xycoords=lambda r, b=bar: Bbox.intersection(b.get_window_extent(r), b.get_clip_box()),
#         xytext=(0, 0), textcoords='offset points',
#         ha='center', va='center')
#     iter += 1

# ax.set_yscale('log')
# ax.set_xlabel('Times question is repeated')
# ax.set_ylabel('Number of questions')
# ax.set_title('Histogram of Occurences of Questions in Datasets')

# plt.savefig(plotDir + '/QuestionRepeatsCount.jpg', bbox_inches='tight')

# # Number of unique pairs ---------------------------------------------------------------------------------------------------------------

# qs_concat = data.select(functions.concat(data['q1'], data['q2'], data['isDuplicate']).alias('concat_qs'), data['isDuplicate'])
# qs_concat = qs_concat.groupby(qs_concat['concat_qs']).count()
# qs_concat = qs_concat.orderBy(qs_concat['count'].desc()).withColumnRenamed('count', 'repeats')

# repeats_pairs = qs_concat.groupby(qs_concat['repeats']).count()
# repeats_pairs.show()