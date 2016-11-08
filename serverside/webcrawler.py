try:
    import urllib.request as urllib2
    import os
    import sys
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
passwd = input("Password: ")
os.system('cls' if os.name == 'nt' else 'clear')
print("Stockmod")
file.close()

def fetchData(corp):
    # Reads html and fetches corp name and stock price
    # Will later be used to put into SQL DB
    conn = False
    # Here we will need a try-except-catch block for response
    while (conn == False):
        try:
            response = urllib2.urlopen(corp)
            html = response.read()
            conn = True
        except: 
            conn = False
            print("No connection to website. Trying to reconnect in 10 seconds.")
            sleep(10)

    html = html.decode('utf-8') #So we can handle it as string
    response.close()
    soup = BS(html,'lxml')

    name = soup.find('div', {'class':'displayName'}).text
    name = name.replace("\r\n\t\t\t","")
    name = name.replace(" ","")
    name = name.replace(".","")
    name = name.replace("&","")
    # value = soup.find('span', {'class':'pushBox'}).text
    buyValue = soup.find('span', {'class':'buyPrice'}).text
    buyValue = buyValue.strip()
    buyValue = buyValue.replace("\xa0", "")
    buyValue = buyValue.replace(",", ".")
    buyValue = buyValue.replace("-","0")
    sellValue = soup.find('span', {'class':'sellPrice'}).text
    sellValue = sellValue.strip()
    sellValue = sellValue.replace("\xa0", "")
    sellValue = sellValue.replace(",", ".")
    sellValue = sellValue.replace("-","0")

    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now());
    print(name + " " + buyValue +  " " + sellValue)
    return [name, buyValue, sellValue]
    # return [name, time, value]

# Stores stock price, name and timestamp in db
def storeData(data): # Fix SQL shit l8r
    conn = False
    while (conn == False):
        #try:
        db = pymysql.connect(host='localhost',port=3306,user='root', passwd=passwd, db='stockmod')
        cursor = db.cursor()
        conn = True
        #except:
        #    conn = False
        #    print("No connection to database. Trying to reconnect in 10 seconds.")
        #    sleep(10)
            
        
    for x in data:
        conn = False
        #sql = "INSERT INTO " + x[0] + " (time,value) VALUES (CURRENT_TIMESTAMP()," + x[2] +")"
        sql = "INSERT INTO " + x[0] + " (time,buy,sell) VALUES (CURRENT_TIMESTAMP()," + x[1] +"," + x[2] +  ")"
        print(sql)
        cursor.execute(sql)
        db.commit() # Needs try-except-catch
        db.close()
       
# To reinforce that each link is fetched over a period T of time
def planner():
    length = len(corpList)
    cycle = math.ceil(length/60) + 1 # Round to nearest upper minute
    cycle = cycle*60/length # So we split each download to a cycle, fetches per minute
#    end = datetime.time(17, 30, 00)
    end = datetime.time(23, 50, 00)
    start = datetime.time(9,00,00)
    while True:
        mydate = datetime.datetime.today()
        now = datetime.time(mydate.hour,mydate.minute,mydate.second)
        temp = []
        if (mydate.weekday() != 5 and mydate.weekday() != 6 and start < now and now < end): # If market is open
            print("Open: " + str(now))

            for corp in corpList:
                data = fetchData(corp)
                temp.append(data)
                sleep(cycle)
                storeData(temp)
            del temp # Release memory, prevent leakage
        else:
            while not (start < now and now < end): # Lowers CPU usage at closed hours
                print("Closed")
                sleep(30)
                mydate = datetime.datetime.today()
                now = datetime.time(mydate.hour,mydate.minute,mydate.second)

def main():
    planner()

if __name__ == "__main__":
    main()
