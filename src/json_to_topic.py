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

def send_message(key_info, value_info):
    #producer.send(TOPIC, bytes(data, encoding='utf-8'))
    producer.send(TOPIC, key=bytes(str(key_info), encoding='utf-8'), value=bytes(str(value_info), encoding='utf-8'))
    producer.flush()
    print("SENT")

with open(filename,'r') as f:
    try: 
        data = json.loads(f.read())
        for info in data:
            print(type(data[info]))
            send_message(info, data[info])

    except Exception as e:
        print('Exception in publishing message')
        print(str(e))

   
