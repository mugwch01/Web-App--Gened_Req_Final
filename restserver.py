from flask import Flask,render_template
from json import dumps
from gened_queries import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('%s.html' % 'home')

@app.route('/home')
def home():
	return render_template('%s.html' % 'home')

@app.route('/base')
def base():
	return render_template('%s.html' % 'base')

@app.route('/courses')
def courses():
	return render_template('%s.html' % 'courses')

@app.route('/api/v1/sql/<query>', methods=['GET'])
def sql(query):
	print("executing this query")
	print(query)
	return dumps(exe_n_fetch(query))

@app.route('/api/v1/sqlcoursetitle/<query>', methods=['GET'])
def sql3(query):
	print("executing this query3")
	print(query)	
	n_query = "select id from course where course.title like '%%%s%%'"%(query)
	course_id = exe_n_fetch(n_query)
	course_id2 =extract_id(course_id)
	req_str = part_str(course_id2)
	query2 = "select title,number,requirement.requirement from (select * from course_requirement where "+req_str[4:]+") as B join course on (B.course = course.id) join Requirement on (B.requirement = requirement.id)"#%(course_id2[0]) #5 works
	return dumps(exe_n_fetch(query2))

@app.route('/api/v1/sqlcoursenumber/<query>',methods=['GET'])
def sql4(query):
	print("executing this query4")
	print(query)	
	n_query = "select id from course where course.number like '%%%s%%'"%(query)
	course_id = exe_n_fetch(n_query)
	course_id2 =extract_id(course_id)
	req_str = part_str(course_id2)
	query2 = "select title,number,requirement.requirement from (select * from course_requirement where "+req_str[4:]+") as B join course on (B.course = course.id) join Requirement on (B.requirement = requirement.id)"#%(course_id2[0]) #5 works
	return dumps(exe_n_fetch(query2))

@app.route('/api/v1/sqlreq/<query>', methods=['GET'])
def sql2(query):
	print("executing this query2")
	print(query)	
	lst = query.split(",")
	if len(lst) > 1:
		dummy = []
		req_str =""
		for x in lst:
			cur_qry = "select id from requirement where requirement.requirement like '%%%s%%'"%(x)
			ide = exe_n_fetch(cur_qry)[0][0]
			req_str = req_str + " or "
			req_str = req_str + "requirement = " + str(ide)
		final_q = "select title,number from (select course,count(requirement) as cout from course_requirement where %s group by course having count(requirement)= %s) as B join course on (B.course = course.id);"%(req_str[4:],len(lst))
    
	else:
		final_q = "select title,number from requirement join course_requirement on (requirement.id = course_requirement.requirement) join course on (course.id = course_requirement.course) where requirement.requirement like '%%%s%%'"%(query)
		pass
	return dumps(exe_n_fetch(final_q))


if __name__ == '__main__':	
	app.run(debug=True)
