#Author: Charles Mugwagwa
#Gened DB connection and Queries

import os
import urllib
#import urllib.parse as urlparse
import psycopg2

'''
def connect_db():
	conn = psycopg2.connect('postgres://pumgxjfkrvhnvr:2acf1e1d19c4660eaba9f7391d5e0fad70da99d41e8f4a188e86a3ab72c5fcc3@ec2-54-235-159-101.compute-1.amazonaws.com:5432/d3vcufbedpte6k')
	return conn
'''


def connect_db():
	print("In connect_db")
	if not 'DATABASE_URL' in os.environ:
		print("You must have DATABASE_URL in your environment variable. See documentation.")
		print("Execute 'source .env' to set up this environment variable if running locally.")
		return 
	try:
		urllib.parse.uses_netloc.append("postgres")
		url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
		conn = psycopg2.connect(
		   database=url.path[1:],
		   user=url.username,
		   password=url.password,
		   host=url.hostname,
		   port=url.port
		)

		return conn

	except Exception as ex:
		print(ex)
		print("Unable to connect to database on system.")
		return	


 

'''
def connect_db():
	url = urlparse.urlparse(os.environ['DATABASE_URL'])
	dbname = url.path[1:]
	user = url.username
	password = url.password
	host = url.hostname
	port = url.port

	con = psycopg2.connect(
            	dbname=dbname,
            	user=user,
            	password=password,
            	host=host,
            	port=port
           	 )
	return con 
'''

def exe_n_fetch(query):
	conn = connect_db()
	cur = conn.cursor()	
	cur.execute(query)
	conn.commit()
	return cur.fetchall()    

def extract_id(lst):
	course_id2 = []
	for x in lst:
		course_id2.append(x[0])
	return course_id2

def part_str(course_id2):
	req_str =""
	for x in course_id2:
		req_str = " or course = " + str(x)
	return req_str
