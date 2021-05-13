from datetime import datetime

with open( "/mnt/tax_co/cron/test/python.txt", "a" ) as f:
  f.write( "Hello, the time is " + str( datetime.now() ) + "\n" )
