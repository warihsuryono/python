from __future__ import print_function

import sys
import time
import mysql.connector
from labjack import ljm


from mysql.connector.constants import ClientFlag

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="trusur_aqm")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM aqm_show WHERE id=1")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_show (id) VALUES (1)")
        mydb.commit()
except Exception as e: 
    print(e)
    
try:
    labjack = ljm.openS("ANY", "ANY", "ANY")
except:
    print("Labjack Error")

while True:
    try:
        # labjack = ljm.openS("ANY", "ANY", "ANY")
        v_ain0 = ljm.eReadName(labjack, "AIN0")
        v_ain1 = ljm.eReadName(labjack, "AIN1")
        
        sql = "UPDATE aqm_show SET pm10 = %s,pm25 = %s WHERE id = 1"
        val = (v_ain0,v_ain1)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Val = %f ; %f" % (ain0,ain1))
        
    except Exception as e: 
        print(e)

    time.sleep(1) 