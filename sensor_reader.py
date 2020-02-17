from __future__ import print_function

import sys
import time
import mysql.connector
from labjack import ljm
import serial


from mysql.connector.constants import ClientFlag

AIN0 = 0
AIN1 = 0
AIN2 = 0
AIN3 = 0
PM10 = 0
PM10_flow = 0
PM25 = 0
PM25_flow = 0
is_labjack = False
is_COM_PM10 = False
is_COM_PM25 = False



try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="trusur_aqm")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM aqm_sensor_values WHERE id=1")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_sensor_values (id) VALUES (1)")
        mydb.commit()
except Exception as e: 
    print(e)
    
try:
    labjack = ljm.openS("ANY", "ANY", "ANY")
    is_labjack = True
except:
    print("Labjack not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm10'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pm10'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    COM_PM10 = serial.Serial(serial_port, serial_rate)
    is_COM_PM10 = True
except:
    print("COM_PM10 not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm25'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pm25'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    COM_PM25 = serial.Serial(serial_port, serial_rate)
    is_COM_PM25 = True
except:
    print("COM_PM25 not connected")

while True:
    try:
        if is_labjack:
            AIN0 = ljm.eReadName(labjack, "AIN0")
            AIN1 = ljm.eReadName(labjack, "AIN1")
            AIN2 = ljm.eReadName(labjack, "AIN2")
            AIN3 = ljm.eReadName(labjack, "AIN3")
        
        if is_COM_PM10:
            temp = str(COM_PM10.readline());
            PM10 = float(temp[2:9])
            PM10_flow = float(temp[10:13])
            
        if is_COM_PM25:
            temp = str(COM_PM25.readline());
            PM25 = float(temp[2:9])
            PM25_flow = float(temp[10:13])
        
        sql = "UPDATE aqm_sensor_values SET pm10 = %s, pm10_flow = %s, pm25 = %s, pm25_flow = %s, AIN0 = %s, AIN1 = %s, AIN2 = %s, AIN3 = %s WHERE id = 1"
        val = (PM10,PM10_flow,PM25,PM25_flow,AIN0,AIN1,AIN2,AIN3)
        mycursor.execute(sql, val)
        mydb.commit()
        print("AIN0 = %f ; AIN1 = %f ; AIN2 = %f ; AIN3 = %f ; PM10 = %f / %f;  PM25 = %f / %f ; " % (AIN0,AIN1,AIN2,AIN3,PM10,PM10_flow,PM25,PM25_flow))
        
    except Exception as e: 
        print(e)

    time.sleep(1) 