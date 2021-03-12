import json 
from kafka import KafkaProducer

TOPIC = "topic_by_json"


producer = KafkaProducer(bootstrap_servers='localhost:9092')
#filename = "/home/ubuntu/apps/ndsu-IoT/data/json/test.json"
filename = "/home/ubuntu/apps/ndsu-IoT/data/json/test2.json"

import sys, json
struct = {}

import time

def foo():
  print(time.ctime())

#while True:
#  foo()
#  time.sleep(1)

def send_message(data):
    producer.send(TOPIC, bytes(data, encoding='utf-8'))
    producer.flush()
    print("SENT")

with open(filename,'r') as f:
    try: 
        #data = json.loads(f.read())
        send_message(f.read())

    except Exception as e:
        print('Exception in publishing message')
        print(str(e))

    #producer = KafkaProducer(
    #    bootstrap_servers='localhost:9092',
    #    value_serializer=lambda v: json.loads(f.read()).encode('utf-8')
    #)
   
