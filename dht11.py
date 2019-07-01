import sys
import Adafruit_DHT
import datetime as dt
import time
#File reads dht-11 external and internal
#Internal is just to keep tabs on pi-zeros operating temperature
#External is just to monitor environment
#The question for now is.. Do you need a database?
#While I wait for the answer lets just write to a google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#use creds to create a client to interact with the google drive api
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('../raspicam-c1df1d17a617.json',scope)
client = gspread.authorize(creds)

sheet = client.open('RaspiCamData').sheet1
#Before going into the while loop stamp the current hour
lastWrote = dt.datetime.now().hour
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