#!/usr/bin/python
import email, imaplib, os, sys, re, pdb
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
import transaction

db_file = FileStorage('emails.fs')
db = DB(db_file)
connection = db.open()
root = connection.root()

def lenr(object):
    agg = []
    for x in object:
        if type(object) == type({}):
            x = object[x]
        if type(x) == type([]):
            agg.append(lenr(x))
        if type(x) == type({}):
            agg.append(lenr(x))
    if type(object) == type({}):
        total_length = len(object)
    else:
	total_length = len(object) - len(agg)
    for item in agg:
        total_length += item
    return total_length

def text_analysis():
    pass

total_messages = lenr(dict(root))

print str(total_messages) + " Emails to Analyze"

daylist = [0,0,0,0,0,0,0]
hourlist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
userlist = {}
newuser = {}
# Calculate Day Prevelance:

for year in root.keys():
    for month in root[year].keys():
        # Messages per month
        print str(year)+"\t"+str(month)+"\t"+str(lenr(dict(root[year][month])))
        for day in root[year][month].keys():
            for message in root[year][month][day]:
                daylist[message.datetime.weekday()] += 1
                hourlist[message.datetime.hour] += 1
                try:
                    userlist[message['X-Original-Sender']] += 1
                except:
                    try:
                        newuser[year][month] += 1
                    except:
                        if year in newuser.keys():
                            newuser[year][month] = 1
                        else:
                            newuser[year] = {month:1}

                    userlist[message['X-Original-Sender']] = 1
                #pdb.set_trace()
                #text_analysis(message.message)


print "Day of week prevelance:"                
for day in daylist:
    print day

print "Time in hour prevelance:"
for hour in hourlist:
    print hour

print "New posters per month:"

for year in newuser.keys():
    for month in newuser[year].keys():
        print newuser[year][month]

print "Busiest Users:"
user_placeholder = ['None',0]
for user in userlist.keys():
    for placeholder in user_placeholder:
        if user_placeholder[1]<userlist[user]:
            user_placeholder = [user,userlist[user]]

print user_placeholder
print "Accounts for " + str(((user_placeholder[1]+0.0)/total_messages)*100) + "% of mailing list"

