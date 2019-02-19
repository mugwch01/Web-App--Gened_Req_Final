#Author: Charles Mugwagwa
#Gened DB connection and Queries

import os
import urllib
import psycopg2

#conn = psycopg2.connect('postgres://txjneaedtuizfq:4254d8b76dc8a5e5bbe3214d0536a11183b69471f15c1c77e6d262d3c2f7b0b1@ec2-54-235-210-115.compute-1.amazonaws.com:5432/d6m6em1pj5585r')
#cur = conn.cursor()

def connect_db():
	print("In connect_db")
	if not 'DATABASE_URL' in os.environ:
		print("You must have DATABASE_URL in your environment variable. See documentation.")
		print("Execute 'source .env' to set up this environment variable if running locally.")
		return 
	try:
		urllib.parse.uses_netloc.append("postgres")
		url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
		db = psycopg2.connect(
		   database=url.path[1:],
		   user=url.username,
		   password=url.password,
		   host=url.hostname,
		   port=url.port
		)

		return db

	except Exception as ex:
		print(ex)
		print("Unable to connect to database on system.")
		return	


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
