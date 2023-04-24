# #%%
# import findspark
# findspark.init()

#%%
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, FloatType, StringType

#%%
spark = SparkSession.builder \
    .appName("transactions-job-backup") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
    .getOrCreate()
#%%
# define input schema
inputSchema = StructType([
    StructField("user_id", IntegerType()),
    StructField("transaction_timestamp_millis", LongType()),
    StructField("amount", FloatType()),
    StructField("currency", StringType()),
    StructField("counterpart_id", IntegerType())
])

#%%
# define kafka source
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:19092") \
    .option("subscribe", "transactions") \
    .load()

# convert value column from binary to string
kafka_df = kafka_df.selectExpr("CAST(value AS STRING)")

# parse json data
parsed_df = kafka_df.select(from_json(col("value"), inputSchema).alias("data"))

# select columns and write to parquet file
query = parsed_df.select("data.*") \
    .writeStream \
    .format("parquet") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .option("path", "/output/") \
    .start()

# wait for query to terminate
query.awaitTermination()
# %%
