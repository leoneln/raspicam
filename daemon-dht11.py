#Fo reference look at https://github.com/thesharp/daemonize
#The idea here is the detach dht11 script from a controlling terminal
# and makeit a process that runs on the background..

import sys
import Adafruit_DHT
import datetime as dt
import time
from daemonize import Daemonize
import gspread
from oauth2client.service_account import ServiceAccountCredentials

pid = "/tmp/dht11.pid"
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('../raspicam-c1df1d17a617.json',scope)
client = gspread.authorize(creds)
sheet = client.open('RaspiCamData').sheet1
lastWrote = dt.datetime.now().hour

def main():
  while True:
    #Compare to current hour and if now another hour write
    if lastWrote != dt.datetime.now().hour:
      hInternal, tInternal = Adafruit_DHT.read(11,24)
      hExternal, tExternal = Adafruit_DHT.read(11,27)
      if hInternal is None or tInternal is None or hExternal is None or tExternal is None:
        time.sleep(2)
        continue
      timestamp = dt.datetime.now().isoformat()
      rowInternal = ['Internal',timestamp,tInternal,hInternal]
      rowExternal = ['External',timestamp,tExternal,hExternal]
      try: 
        sheet.insert_row(rowInternal,2)
        sheet.insert_row(rowExternal,2)
      except:
        time.sleep(2)
        continue
      #push current hour after write
      lastWrote = dt.datetime.now().hour

daemon = Daemonize(app="dht11",pid=pid,action=main)
daemon.start()