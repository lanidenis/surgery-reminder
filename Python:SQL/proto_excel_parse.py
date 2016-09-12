#!/usr/bin/env python

#----------------------------------------------------#
from twilio.rest import TwilioRestClient
import time
#test acccount credentials
#account="AC6f6b40fc7ee4488ab4d366c2f2a4b31f"
#token="f9143e8d7b96179fa51278513c1a4382"

#real account credentials
account="AC1b1336fbf0de2e1ccfe4bcdc5247e1e9"
token="98ce954f5ea9d91ae1dcda8c8b3f9aae"

client = TwilioRestClient(account, token)

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

	print(message.sid)

	time.sleep(3)

	return message.status

#----------------------------------------------------#

def phone(head, row):

	call = client.calls.create(url="http://demo.twilio.com/docs/voice.xml",
    to=number, from_="+19143713240")

	print(call.sid)

	return 1


#----------------------------------------------------#

def email(head, row):



	return 1

#----------------------------------------------------#
from xlrd import open_workbook
#from xlrd import sheet_by_index
import xlrd
from xlutils.copy import copy
from xlwt import easyxf 
import datetime

#open read only files
book = open_workbook('adt.xls')
sheet = book.sheet_by_index(0)

#make writable copy, (not readable)
book2 = copy(book)
sheet2 = book2.get_sheet(0)

#collect the header from top row of readable file
header = {}
for i in range(sheet.ncols):
	header[sheet.cell_value(0, i)] = i

#add raw date column for triage
header["Raw_Date"] = sheet.ncols
header["Age"] = sheet.ncols + 1

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
		if(j == header['Datetime']): #format date of appointment
			date = xlrd.xldate.xldate_as_datetime(cell, book.datemode)
			str_date = date.strftime("%D %I:%M %p")
			rows.append(str_date)
		elif (j == header["Date of Birth"]): #calculate and save age
			rows.append(cell)
			age = datetime.datetime.now() - xlrd.xldate.xldate_as_datetime(cell, book.datemode)
			age = divmod(age.total_seconds(), 3600)[0] #convert to hours
			age = divmod(age, 24)[0] #convert to days
			age = divmod(age, 365)[0] #convert to years
		else: rows.append(cell)
	rows.append(date) # save the appt datetime for triage
	rows.append(age) # save patient age for triage
	index.append(rows)

#handle each appointment (row) separately
len_index = len(index)

for i in xrange(1, len_index):
	myrow = index[i]

	current = datetime.datetime.now()
	diff = myrow[header["Raw_Date"]] - current #difference in datetime
	hours = divmod(diff.total_seconds(), 3600) 
	hours = hours[0] #convert to hours

	t = header['Text']; #index for text column
	e = header['Email']; #index for email column
	p = header['Phone']; #index for phone column

	#only send reminder if unconfirmed or pending reschedule
	if (hours <= 168): #7 days in advance
		if(myrow[header['Age']] < 50):
			status = text(header, myrow)
			print status
			#sheet2.write(i, sched, 2)
		
	elif (hours <= 72): #3 days in advance
		status = text(header, myrow)
		#sheet2.write(i, sched, 1)

	elif (hours <= 24): #1 day in advance
		status = text(header, myrow)
		#sheet2.write(i, sched, 0)

import os
book2.save('adt.xls') #overwrite the old copy

