# Note (Example is valid for Python v2 and v3)
from __future__ import print_function

import sys

#sys.path.insert(0, 'python{0}/'.format(sys.version_info[0]))

import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'trusur_aqm'
}

cnx = mysql.connector.connect(**config)
cur = cnx.cursor(buffered=True)
cur.execute("SELECT * FROM aqm_data")
print(cur.fetchone())
cur.close()
cnx.close()