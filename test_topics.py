import os

from pyspark import SparkConf, SparkContext 
from kafka import KafkaConsumer, KafkaProducer
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

KAFKA_TOPICS = "solar-module-raw"
KAFKA_BROKERS = "localhost:9092"
ZOOKEEPER = "localhost:2181"

OUTPUT = "spark_out"

sc = SparkContext.getOrCreate()

ssc = StreamingContext(sc,60)
kafkaStream = KafkaUtils.createStream(ssc, ZOOKEEPER, "spark-streaming", {KAFKA_TOPICS:1})
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def remove_existing_log():
	if os.path.exists("logs.txt"):
  		os.remove("logs.txt")
		
	else:
		print("No log")
		
def get_type(data):
	return data

def get_power(data):
	#data = json.loads(data)
	return data["power"]

def calculate(data):
	data = json.loads(data)
	return data["powers"]*2

def handler(message):
	records = message.collect()
	for record in records:
		producer.send('spark_out', str(record))
		producer.flush()

def main():
    remove_existing_log()

	lines = kafkaStream.map(lambda x: "old value: {}".format(get_type(x[1])))

	#lines = kafkaStream.map(lambda x: "Initial value: {}, New value: {}".format(get_type(x[1]), calculate(x[1])))
	
	lines.pprint()

	ssc.start()
	ssc.awaitTermination()	

if __name__== "__main__":
   main()