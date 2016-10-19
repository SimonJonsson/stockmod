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
    #outputFile = open("data.dat",'a')
    db = pymysql.connect(host='95.80.53.172',port=3306,user='Schill', passwd='', db='stockmod')
    cursor = db.cursor()
    for x in data:
        #outputFile.write(x[0] + "," + x[1]+ "," + x[2] + "\n")
        #sql = "INSERT INTO " + x[0] + " (time,value) VALUES (" + x[1] + "," + x[2] +")"
        sql = "INSERT INTO " + x[0] + " (time,value) VALUES (CURRENT_TIMESTAMP()," + x[2] +")"
        print(sql)
        cursor.execute(sql)
        db.commit()
    #outputFile.close()
    db.close()
    
# To reinforce that each link is fetched over a period T of time
def planner():
    length = len(corpList)
    cycle = math.ceil(length/60) + 1 # Round to nearest upper minute
    cycle = cycle*60/length # So we split each download to a cycle, fetches per minute

    while True:
        temp = []
        for corp in corpList:
            data = fetchData(corp)
            temp.append(data)
            #sleep(cycle)
        storeData(temp)
        sleep(cycle)
        del temp # Release memory, prevent leakage

def main():
    planner()

if __name__ == "__main__":
    main()
