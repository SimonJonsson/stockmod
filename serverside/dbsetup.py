try:
    import urllib.request as urllib2
    import datetime
    import math
    import os
    import pymysql
    from time import sleep
    from bs4 import BeautifulSoup as BS
except ImportError:
    import urllib2
    

file = open('../htmls.txt','r')
passFile = open('passwd','r')
passwd = passFile.read()
passwd = passwd.replace("\n","")
os.system('cls' if os.name == 'nt' else 'clear')
print("\rStockmod setup")

db = pymysql.connect(host='95.80.53.172',port=3306,user='stockmod', passwd=passwd, db='stockmod')
cursor = db.cursor()

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
    name = name.strip()
    name = name.replace(" ","")
    name = name.replace(".","")
    name = name.replace("&","")
    return name

def main():
    for corp in corpList:
        name = fetchData(corp)
        sql = "CREATE TABLE " + name + " (time datetime, buy double, sell double);"
        try:
            cursor.execute(sql)
        except:
            print(name + " already exists")
        else:
            print(name + " created")
    db.close()

if __name__ == "__main__":
    main()
