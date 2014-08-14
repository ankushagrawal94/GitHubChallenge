#searchDBForCurrentStars.py is reponsible for getting the most recent entry for each repository

import MySQLdb
import time

conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "password")
cursor = conn.cursor()
#cursor.execute ("DROP DATABASE IF EXISTS githubDB")
##cursor.execute ("CREATE DATABASE githubDB")
cursor.execute ("USE githubDB")
cursor.execute("DROP TABLE IF EXISTS max_stars_two")
cursor.execute ("""
	CREATE TABLE max_stars_two
	(
		repo_name   VARCHAR(255),
		stars       INT(6),
		event_time	DATE
	)
""")
conn.commit()
print "succesfully created the DB"

cursor.close()
conn.close()
try:
	print "started"
	startTime = time.time()

	db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

	cur = db.cursor() 
	cur.execute(""" INSERT INTO max_stars_two
    SELECT y.repo_name, y.stars, y.event_time
	FROM event_table y 
	INNER JOIN (SELECT repo_name, max(event_time) as recent
			FROM event_table x
			GROUP BY repo_name) x
	ON y.repo_name = x.repo_name
	AND x.recent = y.event_time
	ORDER BY repo_name ASC""")
	db.commit()

	stopTime = time.time()
	elapsedTime = stopTime - startTime
	print elapsedTime
	# print all the first cell of all the rows
	for row in cur.fetchall() :
	    print str(row[0]) + '\t\t\t\t' + str(row[1])

	cur.close()
	db.close()
except Exception, e:
	print e
	raise e


