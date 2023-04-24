from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.datastream.util import OutputTag
from pyflink.dataset import ExecutionEnvironment
from pyflink.table import TableConfig, DataTypes
from pyflink.table.descriptors import Kafka, Schema
from pyflink.table.window import Tumble
from pyflink.table import StreamTableEnvironment, DataTypes, Schema
import pyarrow.parquet as pq

env = StreamExecutionEnvironment.get_execution_environment()

# Enable checkpointing every 5 seconds for fault tolerance
env.enable_checkpointing(5000, CheckpointingMode.EXACTLY_ONCE)

# Set up Kafka consumer
kafka_props = {
    'bootstrap.servers': 'localhost:19092',
    'group.id': 'flink-consumer-group',
    'auto.offset.reset': 'earliest'
}

input_schema = Schema.new_builder() \
    .column("user_id", DataTypes.INT()) \
    .column("transaction_timestamp_millis", DataTypes.BIGINT()) \
    .column("amount", DataTypes.FLOAT()) \
    .column("currency", DataTypes.STRING()) \
    .column("counterpart_id", DataTypes.INT()) \
    .build()

# create a Kafka consumer and read data from 'transaction' topic
kafka_consumer = FlinkKafkaConsumer(
    'transactions',
    input_schema,
    properties=kafka_props
    # use flink buffer size for optimization
    max_num_records=1000
)

# Add Kafka consumer as a data source
input_stream = env.add_source(kafka_consumer)

# Define schema for the output data
output_schema = SimpleStringSchema()

transaction_stream = env.add_source(kafka_consumer)


# process data to calculate the total number of transactions for each user
transaction_stream \
    .map(lambda x: (int(x.split(',')[0]), 1)) \
    .key_by(lambda x: x[0]) \
    .sum(1) \
    .map(lambda x: {"user_id": x[0], "total_transactions_count": x[1]}) \

# # Define file sink for output data
# file_sink = transaction_stream\
#     .for_row_format('/', output_schema)\
#     .with_bucket_check_interval(60000)\
#     .build()

# Write the stream to Parquet format
output_path = '/ouputkv/'
transaction_stream.add_sink(pq.ParquetWriter(output_path, transaction_stream.schema()))

# write data to redis for a key value search

env.execute("transaction_aggregation")
