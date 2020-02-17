from __future__ import print_function

import sys
import time
import mysql.connector
from labjack import ljm


from mysql.connector.constants import ClientFlag

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="trusur_aqm"
)

mycursor = mydb.cursor()


while True:

    try:
        handle = ljm.openS("ANY", "ANY", "ANY")
        ain0 = ljm.eReadName(handle, "AIN0")
        ain1 = ljm.eReadName(handle, "AIN1")
        
        

        sql = "UPDATE aqm_data SET waktu=NOW(),pm10 = %s,pm25 = %s WHERE id = %s"
        val = (ain0,ain1,"1863")
        mycursor.execute(sql, val)
        mydb.commit()
        print("Val = %f ; %f" % (ain0,ain1))
    except:
        print("Labjack Error")
    
    time.sleep(1) 