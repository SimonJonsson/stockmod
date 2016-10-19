try:
    import urllib.request as urllib2
    import sqlite3
    import datetime
    import math
    import pymysql
    from time import sleep
    from bs4 import BeautifulSoup as BS
except ImportError:
    import urllib2

file = open('../htmls.txt','r')

corpList = [] # Should be kept global so we don't get alot of calls, saves memory
# Adds each html in htmls.txt as a corporation
for line in file:
    corpList.append(line)

file.close()

def fetchData(corp):
    # Reads html and fetches corp name and stock price
    # Will later be used to put into SQL DB
    response = urllib2.urlopen(corp)
    html = response.read()
    html = html.decode('utf-8') #So we can handle it as string
    response.close()
    soup = BS(html,'lxml')

    name = soup.find('div', {'class':'displayName'}).text
    name = name.replace("\r\n\t\t\t","")
    name = name.replace(" ","")
    name = name.replace(".","")
    name = name.replace("&","")
    value = soup.find('span', {'class':'pushBox'}).text
    value = value.strip()
    value = value.replace("\xa0", "") # Avanza uses \xa0 as space, therefore the replace
    value = value.replace(",",".")
    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now());
    return [name, time, value]

# Stores stock price, name and timestamp in db
def storeData(data): # Fix SQL shit l8r
    db = pymysql.connect(host='95.80.53.172',port=3306,user='Schill', passwd='Stockmod', db='stockmod')
    cursor = db.cursor()
    for x in data:
        sql = "INSERT INTO " + x[0] + " (time,value) VALUES (CURRENT_TIMESTAMP()," + x[2] +")"
        cursor.execute(sql)
        db.commit()
    db.close()
    
# To reinforce that each link is fetched over a period T of time
def planner():
    length = len(corpList)
    cycle = math.ceil(length/60) + 1 # Round to nearest upper minute
    cycle = cycle*60/length # So we split each download to a cycle, fetches per minute
    end = datetime.time(17, 30, 00)
    start = datetime.time(9,00,00)
    while True:
        mydate = datetime.datetime.today()
        now = datetime.time(mydate.hour,mydate.minute,mydate.second)
        temp = []
        
        if (mydate.weekday() != 5 and mydate.weekday() != 6 and start < now and now < end): # If market is open
            for corp in corpList:
                data = fetchData(corp)
                temp.append(data)
                sleep(cycle)
            storeData(temp)
            del temp # Release memory, prevent leakage
        else:
            while not (start < now and now < end): # Lowers CPU usage at closed hours
                sleep(30)
                mydate = datetime.datetime.today()
                now = datetime.time(mydate.hour,mydate.minute,mydate.second)

def main():
    planner()

if __name__ == "__main__":
    main()
