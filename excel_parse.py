
#!/usr/local/bin/python2.7.exe

#----------------------------------------------------#
import config
import sys

import twilio.rest
from twilio.rest import TwilioRestClient
import time

import mysql.connector

#----------------------------------------------------#

client = TwilioRestClient(config.account, config.token) #boot up Twilio

print config.configuration
db = mysql.connector.connect(config.configuration) #boot up 
if (db.is_connected() != true):
	sys.exit()
cur = db.cursor()

#----------------------------------------------------#

def text(head, row):

	#retrieve indexes
	date_dex = head["Datetime"]
	num_dex = head["Mobile Phone"]

	datetime = row[date_dex].split(" ")

	date = datetime[0]
	clock = datetime[1] + datetime[2]
	number = "+1" + str(int(row[num_dex]))
	str_body = "{0}, you have an appt with Dr. Smith at {1} on {2}. Reply 1 to confirm, 2 to cancel, or 3 to reschedule. Reply STOP to opt out."
	str_body = str_body.format(row[0], clock, date)

	message = client.messages.create(to=number, from_="+19143713240",
 	body=str_body, media_url="http://www.twilio-responder.com/mnt-slide1.jpg")

	return message.sid
	#message.status

#----------------------------------------------------#

def phone(head, row):

	#retrieve patient phone number
	num_dex = head["Mobile Phone"]
	number = "+1" + str(int(row[num_dex]))

	call = client.calls.create(url="http://twilio-responder.com/phone.xml",
    to=number, from_="+19143713240", )

	return call.sid
	#call.status
#----------------------------------------------------#

def email(head, row):
	

	return 1

#----------------------------------------------------#

def update_sql(myrow):
	global header, cur, db

	sql = (
		"SELECT *"
		"FROM patient_records"
		"WHERE (MRN == '" + myrow[header["MRN"]] + "')"
	)

	try:
		cur.execute(sql)
	except (mysql.connector.errors.Error, TypeError) as exc:
		print "failed sql select for" + myrow[0]
		#sys.exit()

	patient = cur.fetchall() #returns a list of tuples
	if not patient: #patient record does not exist
		sql = (
			"INSERT INTO patient_records ("
		)

		cursor.execute("SHOW columns FROM patient_records")
		columns = cursor.fetchall()
		for index in range(len(columns) - 1):
				sql += columns[index][0] + ", "

		sql += columns[len(columns) - 1][0] + ") VALUES ("

		for index in range(len(columns)):
			sql += "%s"
		
		sql += ")"

		data = ()
		for index in range(len(header) - 2):
			data[index] = myrow[index]

		try:
			cur.execute(sql, data)
		except (mysql.connector.errors.Error, TypeError) as exc:
			print "failed sql insert for" + myrow[0]
			#sys.exit()

	else: #patient records do exist, update accordingly
		data = ()
		marker = 0 
		insert = (
			"INSERT INTO patient_records ("
		)

		rows = patient[0]
		for index in range(len(rows)):
			if (rows[index] == ""): #empty column
				data[marker] = myrow[index]
				marker += 1  
				insert += rows[index] + ", "
		if marker != 0:
			insert = insert[:-2] #strip junk comma
			insert += ") VALUES ("
			for i in range(marker):
				insert += "%s"
			insert += ")"
			
		try:
			cur.execute(insert, data)
		except (mysql.connector.errors.Error, TypeError) as exc:
			print "failed sql insert for" + myrow[0]
			#sys.exit()

	#----------------------------------------------------#

def triage(myrow):
	#send the appropriate amount of phone, email, or text 
	#reminders
	global header, cur, db

	current = datetime.datetime.now()
	diff = myrow[header["raw_date"]] - current #difference in datetime
	hours = divmod(diff.total_seconds(), 3600) 
	hours = hours[0] #convert to hours

	mode = ('phone', 'email', 'text')

	for index in range(1): 
		#send the appropriate reminder
		if (hours <= 168): #7 days in advance
			if(myrow[header['age']] < 50):
				id = mode[index](header, myrow)

		elif (hours <= 72): #3 days in advance
			if(myrow[header['age']] < 50):
				id = mode[index](header, myrow)		

		elif (hours <= 24): #1 day in advance
			if(myrow[header['age']] < 50):
				id = mode[index](header, myrow)

		print id
		sql = (
				"INSERT INTO patient_records (" + mode[index] +")"
				"VALUES (" + id + ") "
				"WHERE (MRN == '" + myrow[header["MRN"]] + "')"
		)

		try:
			cur.execute(sql)
		except (mysql.connector.errors.Error, TypeError) as exc:
			print "failed sql insert for" + myrow[0]
			#sys.exit()

		db.commit() #permanently save all changes to mysql

		#print tid
		#print eid

	return 0
#----------------------------------------------------#

	#excel scrap = START of program
import xlrd 
from xlutils.copy import copy
from xlwt import easyxf 
import datetime

#open read only files
book = xlrd.open_workbook('adt.xls')
sheet = book.sheet_by_index(0)

#collect the header from top row of readable file
header = {}
for i in range(sheet.ncols):
	header[sheet.cell_value(0, i)] = i

#add raw date column for triage
header["raw_date"] = sheet.ncols
header["age"] = sheet.ncols + 1

#input into index
index = []
index.append(list(header.keys()))
date = ""
age = 0

#scrap data row by row
for i in xrange(1, sheet.nrows): 
	rows = []
	for j in range(sheet.ncols):
		cell = sheet.cell_value(i, j)
		if(j == header['date_time']): #format date of appointment
			date = xlrd.xldate.xldate_as_datetime(cell, book.datemode)
			str_date = date.strftime("%D %I:%M %p")
			rows.append(str_date)
		elif (j == header["dob"]): #calculate and save age
			rows.append(cell)
			age = datetime.datetime.now() - xlrd.xldate.xldate_as_datetime(cell, book.datemode)
			age = divmod(age.total_seconds(), 3600)[0] #convert to hours
			age = divmod(age, 24)[0] #convert to days
			age = divmod(age, 365)[0] #convert to years
		else: rows.append(cell)
	rows.append(date) # save the appt datetime for triage
	rows.append(age) # save patient age for triage
	index.append(rows)

#update mysql database if necessary
len_index = len(index)

for i in xrange(1, len_index):
	myrow = index[i]
	update_sql(myrow)

db.commit() #permanently save all changes to mysql

#send appropriate reminders
for i in xrange(1, len_index):
	myrow = index[i]
	if(myrow[header['status']] == 'Unconfirmed'):
		triage(myrow)

#----------------------------------------------------#

	#in case I ever need to make a writable copy
#book2 = copy(book)
#sheet2 = book2.get_sheet(0)
#sheet2.write(row, col, value)
#import os
#book2.save('adt.xls') #overwrite the old copy

#----------------------------------------------------#