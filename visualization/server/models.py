import json
from pymongo import *
import json
import pymysql
import sys
from server.logger import *
from server.config import *
import os

logger = config_logger("SERVER.MODELS", "INFO")


def init():
	conn = pymysql.connect(
			host = '192.168.1.76',
			port = 3306,
			user = "root",
			password = "1234",
			charset ='utf8',
			db = 'aihistory')
	cursor = conn.cursor()
	return conn, cursor

aihistory_sql = """select* from (select * from relation JOIN person where relation.id1=person.id) ai Join person where ai.id2=person.id;"""
def execute(conn, cursor, attr):
    js = {}
    edges, secondary_nodes, secondary_edges = [], [], []
    try:
        cursor.execute(aihistory_sql)
        results = cursor.fetchall()
        print(results)
        for row in results:
            edges.append({"source": row[4], "target": row[6], "relation": row[2], "label": ''})  
    except:
        logger.error("ERROR: " + sql)
        conn.rollback()
    js["edges"] = edges
    js["secondary_edges"] = secondary_edges
    mydata = json.dumps(js, ensure_ascii=False).encode("utf8")
    return mydata