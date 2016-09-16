try:
    import urllib.request as urllib2
    import sqlite3
    from time import sleep
    from bs4 import BeautifulSoup as BS
except ImportError:
    import urllib2

file = open('htmls.txt','r')

corpList = [] # Should be kept global so we don't get alot of calls, saves memory
# Adds each html in htmls.txt as a corporation
for line in file:
    corpList.append(line)
    
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
    value = soup.find('span', {'class':'pushBox'}).text
    value = value.strip()
    return [name, value]

# Stores stock price, name and timestamp in db
def storeData(data): # Fix SQL shit l8r
    for x in data:
        print(x)
    
# To reinforce that each link is fetched over a period T of time
def planner():
    length = len(corpList)
    cycle = 60/length # So we split each download to a cycle, fetches per minute

    while True:
        temp = []
        for corp in corpList:
            data = fetchData(corp)
            temp.append(data)
            sleep(cycle)
        storeData(temp)
        del temp # Release memory, prevent leakage

def main():
    planner()

if __name__ == "__main__":
    main()
