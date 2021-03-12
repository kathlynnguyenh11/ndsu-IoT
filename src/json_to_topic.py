import json 
from kafka import KafkaProducer
import sys, json
import time

TOPIC = "topic_by_json"
INTERVAL = 3

producer = KafkaProducer(bootstrap_servers='localhost:9092')
filename = "/home/ubuntu/apps/ndsu-IoT/data/json/test2.json"

def send_message(key_info, value_info):
    #producer.send(TOPIC, bytes(data, encoding='utf-8'))
    producer.send(TOPIC, key=bytes(str(key_info), encoding='utf-8'), value=bytes(str(value_info), encoding='utf-8'))
    producer.flush()
    print("SENT")

with open(filename,'r') as f:
    try: 
        data = json.loads(f.read())
        while True:
            print(str(INTERVAL) + " passed")
            for info in data:
                send_message(info, data[info])
            time.sleep(INTERVAL)

    except Exception as e:
        print('Exception in publishing message')
        print(str(e))

   
