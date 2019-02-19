#My name is Charles Mugwagwa.
#This script creates 3 tables in my sql database and populates those 3 tables with the information from gened.json.

import psycopg2
import json
import os

#helper function
def req_formatting(requirement):
    if requirement == 'Human Expression—Primary Texts':
        requirement = 'Human Expression-Primary Texts'
    if requirement == 'Natural World—Nonlab':
        requirement = 'Natural World-Nonlab'
    if requirement == 'Human Behavior—Social Science Methods':
        requirement = 'Human Behavior-Social Science Methods'
    if requirement == 'Natural World—Lab':
        requirement = 'Natural World-Lab'
    return requirement

#conn = psycopg2.connect('postgres://txjneaedtuizfq:4254d8b76dc8a5e5bbe3214d0536a11183b69471f15c1c77e6d262d3c2f7b0b1@ec2-54-235-210-115.compute-1.amazonaws.com:5432/d6m6em1pj5585r')
conn = psycopg2.connect('postgres://pumgxjfkrvhnvr:2acf1e1d19c4660eaba9f7391d5e0fad70da99d41e8f4a188e86a3ab72c5fcc3@ec2-54-235-159-101.compute-1.amazonaws.com:5432/d3vcufbedpte6k')
cur = conn.cursor()

#getting data(list) from gened.json
with open('static/data/gened.json') as gened_file:
    data = json.load(gened_file)

c_t_course = '''
create table course (
id serial unique,
number varchar(50),
description text,
title varchar(100)
);'''
c_t_requirement = '''
create table requirement (
id serial unique,
requirement varchar(100)
) '''
c_t_course_requirement = '''
create table course_requirement (
course int references course(id),
requirement int references requirement(id),
Primary Key (course,requirement)
);'''
#creating the tables. drops old tables if they exist
cur.execute("drop table if exists course_requirement cascade;")
cur.execute("drop table if exists course cascade;")
cur.execute("drop table if exists requirement cascade;")
conn.commit()
cur.execute(c_t_course)
cur.execute(c_t_requirement)
cur.execute(c_t_course_requirement)
conn.commit()

#generating list of distinct requirements
outfile = open('static/data/list_of_requirements.txt','w')
requirements_lst = []
for entry in data:
    for requirement in entry['fulfills']:
        requirement = req_formatting(requirement)
        if requirement not in requirements_lst:
            requirements_lst.append(requirement)
            outfile.write("'"+requirement+"',")
outfile.close()
#populating requirement table and mapping 'requirement description' : id
req_dic = {}
count = 1
for req in requirements_lst:
    x = "insert into requirement (requirement) values ('%s')" %(req)
    cur.execute(x)
    conn.commit()
    req_dic[req] =  count
    count += 1

#populating both the course table and the course_requirement table.
outfile2 = open('static/data/list_of_course_titles.txt','w')
outfile3 = open('static/data/list_of_course_numbers.txt','w')
course_titles = []
course_numbers = []
course_id = 1
for entry in data:
    if entry["number"] not in course_numbers:
        course_numbers.append(entry["number"])
        outfile3.write("'"+entry["number"]+"',")
    if entry["title"] not in course_titles:
        course_titles.append(entry["title"])
        outfile2.write("'"+entry["title"]+"',")
    cur.execute("insert into course (number,description,title) values (%s,%s,%s)",(entry["number"],entry["description"],entry["title"]))
    for each_req in entry["fulfills"]:
        each_req = req_formatting(each_req)
        cur.execute("insert into course_requirement (course,requirement) values (%s,%s)" % (course_id,req_dic[each_req]))
        conn.commit()
    course_id += 1
conn.commit()
outfile2.close()
outfile3.close()
print("Done!")
