#!/usr/bin/python

import email, imaplib, os, sys, pdb, datetime, settings
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
import transaction

monthnum = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
daynum = {'Mon':1,'Tue':2,'Wed':3,'Thu':4,'Fri':5,'Sat':6,'Sun':7}


# Use a storage file
db_file = FileStorage('emails.fs')
db = DB(db_file)
connection = db.open()

root = connection.root()

mail = imaplib.IMAP4_SSL(settings.SERVER)
mail.login(settings.USERNAME,settings.PASSWORD)
mail.select(settings.FOLDER)
result, data = mail.search(None,"ALL")
ids = data[0]
id_list = ids.split()


i = 0
for id in id_list:
    result, data = mail.fetch(id,"(RFC822)")
    raw_message = data[0][1]
    print "got message " + str(id) + " of " + str(len(id_list))		
    message = email.message_from_string(raw_message)

    if 'Received' in message.keys():
        timestamp = message['Received']
        splitstamp = timestamp.split(',')[1].split()

    if 'Received' not in message.keys() or timestamp == '':
        timestamp = message['Date']
        splitstamp = timestamp.split(',')[1].split()

    #print splitstamp

    #Get the timestamp organized correctly
    splittime = map(lambda a:int(a),splitstamp[3].split(':'))
    splitstamp[1] = monthnum[splitstamp[1]]
    splitstamp = map(lambda a:int(a),splitstamp[:3])

    emailtime = datetime.datetime(splitstamp[2],splitstamp[1],splitstamp[0],splittime[0],splittime[1],splittime[2],0)

    message.datetime = emailtime

    if emailtime.year not in root.keys():
        root[emailtime.year] = {}

    if emailtime.month not in root[emailtime.year].keys():
        root[emailtime.year][emailtime.month] = {}

    if emailtime.day not in root[emailtime.year][emailtime.month].keys():
        root[emailtime.year][emailtime.month][emailtime.day] = [message]
    else:
	root[emailtime.year][emailtime.month][emailtime.day].append(message)

print "Committing batch to database..."
transaction.commit()
print "Done"
