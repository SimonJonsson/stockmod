try:
    import urllib.request as urllib2
    from bs4 import BeautifulSoup as BS
except ImportError:
    import urllib2

file = open('htmls.txt','r')

corpList = []
# Adds each html in htmls.txt as a corporation
for line in file:
    corpList.append(line)

# Reads each html and fetches corp name and stock price
# Will later be used to put into SQL DB
for corp in corpList:
    response = urllib2.urlopen(corp)
    html = response.read()
    html = html.decode('utf-8') #So we can handle it as string
    response.close()
    soup = BS(html,'lxml')

    name = soup.find('div', {'class':'displayName'}).text
    name = name.strip()
    value = soup.find('span', {'class':'pushBox'}).text
    value = value.strip()
    print(name, end=' : ')
    print(value)

    
