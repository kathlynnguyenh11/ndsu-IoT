from kafka import KafkaConsumer
from pyspark import SparkContest
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

#import simplejson as json
KAFKA_TOPICS = "solar-module-raw"
KAFKA_BROKERS = "localhost:9092"
ZOOKEEPER = "localhost:2181"

sc = SparkContext.getOrCreate()

ssc = StreamingContext(sc,60)
kafkaStream = KafkaUtils.createStream(ssc, ZOOKEEPER, "spark-streaming", {KAFKA_TOPIC:1})

def get_power(data):
	#data = json.loads(data)
	return data["power"]

def calculate(data):
	data = json.loads(data)
	return data["powers"]*2

lines = kafkaStream.map(lamda x: "Initial value: {}, New value: {}".format(get_power(x[1]), calculate(x[1])))
lines.pprint()

ssc.start()
ssc.awaitTermination()

