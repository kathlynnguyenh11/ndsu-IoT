import os
import re

from pyspark import SparkConf, SparkContext 
from kafka import KafkaConsumer, KafkaProducer
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

KAFKA_TOPICS = "solar-module-raw"
KAFKA_BROKERS = "localhost:9092"
ZOOKEEPER = "localhost:2181"
OUTPUT = "topic_for_testing"

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def get_power(data):
	data = json.loads(data)
	return data["power"]

def calculate(data):
	data = json.loads(data)
	return data["powers"]*2

#Replaced by get_power func
def clean_data(data):
	data = re.sub('["\'{}]', '',   data)
	print(data)

	output = {}

	lst = data.split(",")
	print(lst)

	for item in lst:
		info = item.split(":")
		output[info[0]] = info[1]

	return output

def handler(message):
	records = message.collect()
	for record in records:
		power = get_power(record[1])
		processed_power = power*2

		producer.send(OUTPUT, bytes(str(processed_power).encode('utf-8')))
		producer.flush()

def main():
	sc = SparkContext.getOrCreate()
	ssc = StreamingContext(sc,60)

	#kafkaStream = KafkaUtils.createStream(ssc, ZOOKEEPER, "spark-streaming", {KAFKA_TOPICS:1})
	#lines = kafkaStream.map(lambda x: "type: {}, old data: {}, new data type {}".format(get_type(x[1]), x[1], get_type(clean_data(x[1]))))
	#lines.pprint()

	#Send data to thingsBoard topic
	kvs = KafkaUtils.createDirectStream(ssc, [KAFKA_TOPICS], {"metadata.broker.list": KAFKA_BROKERS})
	kvs.foreachRDD(handler)

	ssc.start()
	ssc.awaitTermination()	

if __name__== "__main__":
   main()