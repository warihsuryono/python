from __future__ import print_function

import sys
import time
import mysql.connector
from labjack import ljm
import serial


from mysql.connector.constants import ClientFlag
from pyvantagepro import VantagePro2

AIN0 = 0
AIN1 = 0
AIN2 = 0
AIN3 = 0
PM10 = ""
PM25 = ""
WS = ""
is_labjack = False
is_COM_PM10 = False
is_COM_PM25 = False
is_COM_WS = False



try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="trusur_aqm")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM aqm_sensor_values WHERE id=1")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_sensor_values (id) VALUES (1)")
        mydb.commit()
    print("[V] Database CONNECTED")
except Exception as e: 
    print("    [X] " + e)
    
try:
    labjack = ljm.openS("ANY", "ANY", "ANY")
    is_labjack = True
    print("[V] Labjack CONNECTED")
except:
    print("    [X] Labjack not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm10'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pm10'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    COM_PM10 = serial.Serial(serial_port, serial_rate)
    is_COM_PM10 = True
    print("[V] COM_PM10 CONNECTED")
except:
    print("    [X] COM_PM10 not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm25'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pm25'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    COM_PM25 = serial.Serial(serial_port, serial_rate)
    is_COM_PM25 = True
    print("[V] COM_PM25 CONNECTED")
except:
    print("    [X] COM_PM25 not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_ws'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_ws'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    # COM_WS = serial.Serial()
    # COM_WS.port = serial_port
    # COM_WS.baudrate = serial_rate
    # COM_WS.timeout = 1
    # COM_WS.setDTR(True)
    # COM_WS.open()
    COM_WS = VantagePro2.from_url("serial:%s:%s:8N1" % (serial_port,serial_rate))
    is_COM_WS = True
    print("[V] COM_WS CONNECTED")
except:
    print("    [X] COM_WS not connected")
    
    
while True:
    try:
        if is_labjack:
            AIN0 = ljm.eReadName(labjack, "AIN0")
            AIN1 = ljm.eReadName(labjack, "AIN1")
            AIN2 = ljm.eReadName(labjack, "AIN2")
            AIN3 = ljm.eReadName(labjack, "AIN3")
        
        if is_COM_PM10:
            PM10 = str(COM_PM10.readline());
            
        if is_COM_PM25:
            PM25 = str(COM_PM25.readline());
            
        if is_COM_WS:
            ws_data = COM_WS.get_current_data()
            WS = ws_data.to_csv(';',False)
        
        sql = "UPDATE aqm_sensor_values SET AIN0 = %s, AIN1 = %s, AIN2 = %s, AIN3 = %s, PM25 = %s, PM10 = %s, WS = %s WHERE id = 1"
        val = (AIN0,AIN1,AIN2,AIN3,PM25,PM10,WS)
        mycursor.execute(sql, val)
        mydb.commit()
        
        print("AIN0 = %f ; AIN1 = %f ; AIN2 = %f ; AIN3 = %f ; PM10 = %s;  PM25 = %s ; WS = %s ; " % (AIN0,AIN1,AIN2,AIN3,PM10,PM25,WS))
        print("=========================================================================================================================");
        
    except Exception as e: 
        print(e)

    time.sleep(1) 