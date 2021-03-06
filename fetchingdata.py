from win32com.client import Dispatch
import os
import csv
import MySQLdb

from datetime import datetime
abc = []
check = (os.path.getsize("/enter your directory where you want this/last_datetime.txt"))
if check:
    file = open("/enter your directory where you want this/last_datetime.txt",'r') 
    last_entry = file.read()
    if last_entry:
        last_entry_datetime = datetime.strptime(last_entry, "%Y-%m-%d %H:%M:%S")
    file.close()

#connect device
try:
     zk=Dispatch("zkemkeeper.ZKEM")
     ip="enter the ip address for device" # Ip address of the device
     port=4370 # default port. Please check in the device Communication settings
     connect_dev=zk.Connect_Net(ip,port)
     print "Device 1 Connected successfully",connect_dev
except:
     pass


#enable device
enable_dev=zk.EnableDevice(1,1)

db = MySQLdb.connect("ip of device","db name","password","your password")
cursor = db.cursor()
cursor.execute("SELECT * from admins")
results = cursor.fetchall()
for item in results:
    print item
cursor.close()
db.close()

c = []

#read log data
temp=zk.ReadAllGLogData(1)

while 1:
                done=zk.SSR_GetGeneralLogData(1)
                if done and isinstance(done,tuple) and not done[0]:
                    break
                if not done[3]:
                    x="sign_in"
                else:
                    x="sign_out"      
                tup=done[4],"-",done[5],"-",done[6]       
                date=''.join(str(i) for i in tup)       
                tup1=done[7],":",done[8],":",done[9]       
                time1=''.join(str(i) for i in tup1)    
                dt = date + " " + time1
                a = []
                a.append(done[1])
                a.append(x)
                a.append(dt)
                if check:
                    if datetime.strptime(dt, "%Y-%m-%d %H:%M:%S") > last_entry_datetime:
                        c.append(a) 
                else:
                    c.append(a)


dd = open("/enter your directory where you want this/unsorted_entries.csv",'w')
fieldnames = ['id', 'signin/signout','datetime']                
a = csv.DictWriter(dd,fieldnames=fieldnames)
a.writeheader        
for data in c:
        if c: 
            if data:
        	    a.writerow({'id':data[0],'signin/signout':data[1],'datetime':data[2]})
        
