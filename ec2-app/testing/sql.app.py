#!/usr/bin/python
import psycopg2

def main():
	#Define our connection string
	conn_string = "host='web-app-db.c7sus04aavaa.eu-west-2.rds.amazonaws.com' dbname='salt' user='postgres' password='SaltSecurity1235!'"

	# print the connection string we will use to connect
	print ("Connecting to database\n	->%s" % (conn_string))

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	print ("Connected!\n")

if __name__ == "__main__":
	main()