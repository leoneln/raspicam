import os
import sys
import Adafruit_DHT
import datetime as dt
import time
#file reads vitals from external and internal dht sesors
#internal sensor is inside the case of the rapicam
#external is outside. Just to check temp difference between two
#then loads data to google big query
from google.cloud import bigquery
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../zippy-avatar.json'

#set variables
hInternal,tInternal = Adafruit_DHT.read(11,24)
hExternal,tExternal = Adafruit_DHT.read(11,27)
if hInternal is None or tInternal is None or hExternal is None or tExternal is None:
  time.sleep(2)
  quit()
timestamp = dt.datetime.now().isoformat()

client = bigquery.Client()
query = (
  "INSERT INTO `raspicamData.raspicamVitals` "
  "VALUES('%s',%8.2f,%8.2f,%8.2f,%8.2f)" % (timestamp,tInternal,hInternal,tExternal,hExternal)
)
query_job = client.query(query)

results = query_job.result()  # Waits for job to complete.

 