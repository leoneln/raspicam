import sys
import Adafruit_DHT
#File reads dht-11 external 
#The question for now is.. Do you need a database?
#While I wait for the answer lets just write to a google sheet

while True:
  humidity, temperature = Adafruit_DHT.read_retry(11,27)
  print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature,humidity)