import pandas_datareader.data as web
from datetime import datetime, timedelta
import urllib
#encoding-utf-8

#quotation checker
#-------------------------------------------------------------------------------------
#checking the internet connection. If connection return -True, else False
def network_try(reference):
    try:
        urllib.request.urlopen(reference, timeout=1)
        return True
    except urllib.request.URLError:
        return False

#writes the last quotes to file
def write_to_file(list_with_quotations,ticker):
    file = open("kurser.txt", "w")
    i = 0
    for quotations in list_with_quotations:
        if i == 0:
            i = 0
        else:
            file.write("\n")
        file.write(str(ticker[i])+"\n")
        for dates_quotes in quotations:
            quote = ','.join(str(day) for day in dates_quotes)
            file.write(quote)
            file.write("\n")

        i +=1    
    file.close()



def quotation_creator2(quotation_list_position):
    check_connection = network_try("http://www.yahoo.com/finance")
    if check_connection == False:
        list_with_quotations = quotation_creator(quotation_list_position)

    elif check_connection == True:
        list_with_stocks = ('brk-a', 'goog', 'aapl', 'yhoo')
        list_with_quotations = stock_fundamenta_scraper(list_with_stocks)
        write_to_file(list_with_quotations,list_with_stocks)
        
    
    return list_with_quotations

#-------------------------------------------------------------------------------------
#importing stockinfo from a website with the module Pandas

def stock_fundamenta_scraper(list_with_stocks):
    list_with_fundamenta = []
    year = int(datetime.now().strftime('%Y'))
    month = int(datetime.now().strftime('%m'))
    day = int(datetime.now().strftime('%d'))
    for stock in list_with_stocks:
        dataread = web.DataReader(stock,  'yahoo', datetime(year,month-2,day), datetime(year,month,day))
        z = (list(reversed(dataread.index)))
        close_list = (dataread['Close'])
        close_list2 = reversed(close_list)
        z2 = reversed(z)
        stock_quote = []
        i = 0
        for stock in close_list2:
            temp_list = []
            temp_list.append(z[i])
            temp_list.append(stock)
            stock_quote.append(temp_list)
            i+=1
        list_with_fundamenta.append(stock_quote)
            
    return list_with_fundamenta

#----------------------------------------------------------------------------------
#insert functions

#takes input from user in the undermenu where you wanna chose the stock to analyze.
def insertation(stocks):
    below_menu = True
    while below_menu == True:
        try:
            stock_choice = int(input())
            if 0 <= stock_choice <=len(stocks)+1:
                return stock_choice
            else:
                print ("You did not pic a number between 1 and " + str(len(stocks)))
                
        except:
            print ("Please type a number again")

#takes user input from the head menu.
def head_menu_input():
    head_menu = True
    while head_menu == True:
        try:
            choice = int(input())
            if 1 <= choice <=4:
                return choice
                head_menu = False
            else:
                head_menu = True
                print ("You did not pic a number between 1 and 4")
                
        except:
            print ("Please type a number again")
            head = True
#----------------------------------------------------------------------------------
#calculating functions

#calculating omx development over a 30 day period
def omx_development(omx_list):
    growth_with_dates = omx_list[0:29]     
    only_omx_quotes = []
    list_with_omxfloats = []
    for element in growth_with_dates:
        only_omx_quotes.append(element[1])
        for list_quote in only_omx_quotes:
            transform_to_float = float(list_quote)
            list_with_omxfloats.append(transform_to_float)
   
    ratio = list_with_omxfloats[0]/list_with_omxfloats[29]
    return ratio

#calculating beta-value (omx ratio/stock ratio)
def betavalue_calc(omx_ratio, list_stocks):
    list_with_betavalues = []
    for stock_ratio in list_stocks:   
        calculated_betavalue=omx_ratio/stock_ratio
        list_with_betavalues.append(round(calculated_betavalue,2))
    return list_with_betavalues

#calculating the course development over a period of 30 days
def course_development(quotation_list):
    all_changes = []
    for stocks in quotation_list:
        i = 0
        changes = []
        for change in stocks[i:i+29]:
            changes.append(change[1])
            i +=29

        ratio =  float(changes[0])/float(changes[20])
        all_changes.append(round(ratio,2))

    return all_changes
#calculating the ratio
def ratio_calculation(ratio_list):
    ratio_calc_list = []
    for value in ratio_list:
        calculated_value = round((1-value)*100,2)
        ratio_calc_list.append(calculated_value)
    return ratio_calc_list
        
 

#returns the second key in a list. Very usable when you want to sort a list with list where you don't want to sort the first element.
def get_key(key):
    return key[1]#chooses the second element in a list.

#calculating the lowest value with help of get_key
def lowest_value(quotation_list):
    lowest_values = []
    for stocks in quotation_list:
        sorted_list = sorted(stocks, key = get_key)
        date_value = sorted_list[0]
        value = date_value[1]
        lowest_values.append(round(value,2))
    return lowest_values

#calculating the higest value
def highest_value(quotation_list):
    highest_values = []
    for stocks in quotation_list:
        sorted_list = sorted(stocks, key = get_key)
        date_value = sorted_list[28]
        value = date_value[1]
        highest_values.append(round(value,2))
    return highest_values

#function that sorts the beta value that's been calculated
def beta_value_sort(beta_list, stock_object_list):
    name_beta_list = []
    i = 0
    while i < len(beta_list):
        attribute_list = []
        attribute_list.append(stock_object_list[i].name)
        attribute_list.append(beta_list[i])
        i +=1 
        name_beta_list.append(attribute_list)  
    sorted_list = sorted(name_beta_list, key = get_key)
    return sorted_list

#--------------------------------------------------------
#Print functions
def undermenu_print(stock_list):
    n = 0
    a = 0
    print("\nWich stock would you like to choose?")
    for stocks in stock_list:
        print("\n"+str(n+1)+". " + stocks.name, end="")
        n +=1
    print("\n"+str(len(stock_list)+1)+". "+"Go back")

#prints the head menu
def head_menu_print():
    print("\nWhat type of analysis would you like to do?\n\n"+ "1. Fundamental analysis\n" + "2. Technical analysis\n" + "3. Sort against beta-value\n"+"4. Quit")
    print("\npic a choice")

#prints the fundamental analysis results that has been calculated
def fundamental_analysis(current_stock):
    print ("\n"+"#*#*#*#*#*#*#*#*#*#*"*2)
    print(str(current_stock))
    print ("\n"+"#*#*#*#*#*#*#*#*#*#*"*2)


#prints out the results from the tech. analysis
def technical_analysis(current_stock):
    print ("\n"+"#*#*#*#*#*#*#*#*#*#*"*2)
    print(current_stock.tech_analysis())
    print ("\n"+"#*#*#*#*#*#*#*#*#*#*"*2)
    
#.......................................................
# Menu functions
def top_head_menu():
    head_menu = True
    while head_menu == True:
        head_menu_print()
        choice = head_menu_input()
        head_menu = False
        
        return choice

#.............................................................................................
#functions that read from files

def amount_stocks():
    with open("kurser.txt") as f:
        lines = f.readlines()
        i = 1
        amount_stocks_number = []
        for line in lines:
            if line != "" and line[0].isalpha():
                amount_stocks_number.append(i)
            i+=1    
        return (amount_stocks_number)

#create a quotation list for numerous stocks, read those from a file
def quotation_creator(number_in_list):
    with open("kurser.txt") as f:
        
        lines = f.readlines()
        list_quotations = []
        for number in number_in_list:
            list_quotation = []
            for line in lines[number+1:number+30]:
                line = line.strip()
                line = line.split(",")
                list_quotation.append(line)
            list_quotations.append(list_quotation)   
        return list_quotations

#reads the fundamental stock input and creates a list with the input of those.
def read_fundamental():
    with open('fundamenta.txt') as f:
        result = ', '.join(f.read().split(' '))
        string = result.split()
        list_fundamental = []
        for x in string:
            list_fundamental.append(x.split(","))
        return list_fundamental

#reads the omx-index and return the values(dates and imx-value) as a list
def read_omx():
    with open('omx.txt') as f:
        i = 0
        dictionary = {}
        lista_omx = []
        alla_rader = []
        f = []
        while i < 30: 
            for line in reversed(open("omx.txt").readlines()):
                line = line.strip()
                line = line.split("\t")
               
                lista_omx.append(line)
                i +=1
            
        return (lista_omx)
#.............................................................................................
#creates stock-objects from input derived from functions
def stockobject_creator(fundamental_list, quotation_list, beta_value, highest_v, lowest_v, ratio_list):
    stockobject_list = []
    i = 0
    for stockinfo in fundamental_list:#[0:length_quotation]:
        created_object = Stocks(stockinfo[0], stockinfo[1], stockinfo[2],stockinfo[3], highest_v[i], lowest_v[i], beta_value[i], ratio_list[i])
        stockobject_list.append(created_object)
        i +=1
    return stockobject_list

#----------------------------------------------------------------------------------------------
#Creates a class called Stocks
class Stocks(): 
    def __init__(self, name, solidity, p_e_number, p_s_number, highest_value = None, lowest_val = None, beta_value = None, price_trend = None, stock_quote = None,):
        self.name = name
        self.solidity = solidity 
        self.p_e_number = p_e_number
        self.p_s_number = p_s_number
        self.stock_quote = stock_quote if stock_quote != None else  []  
        self.beta_value = beta_value if beta_value != None else  [] 
        self.price_trend = price_trend if price_trend != None else  [] 
        self.highest_value = highest_value if highest_value != None else  [] 
        self.lowest_val = lowest_val if lowest_val != None else  [] 

    @property
    def name_function(self):
        return self
    
    def beta_val(self):
        return str(self.beta_value)

    def __str__(self):
        return self.name+"\nSolidity:"+self.solidity+"\nP/E-number:"+self.p_e_number+"\nP/S-number:"+self.p_s_number

    def tech_analysis(self):
        return self.name+"\nBeta value:"+str(self.beta_value)+"\nPrice trend:"+str(self.price_trend)+"%"+"\nLowest value:"+str(self.lowest_val)+"\nHighest value:"+str(self.highest_value)
#----------------------------------------------------------------------------------------------

#the main program
def main():
    program = True
    omx_list = read_omx()
    omx_value = omx_development(omx_list)
    quotation_list_position = amount_stocks()
    fundamental_list = read_fundamental()
    omx_value = omx_development(omx_list)
    list_with_quotations = quotation_creator2(quotation_list_position)
    ratio_list = course_development(list_with_quotations)
    ratio_calc = ratio_calculation(ratio_list)
    beta_value = betavalue_calc(omx_value, ratio_list)
    highest_v = highest_value(list_with_quotations)
    lowest_v = lowest_value(list_with_quotations)
    stockobject_list = stockobject_creator(fundamental_list,list_with_quotations,beta_value, highest_v, lowest_v, ratio_calc)

    while program == True:
        choice = top_head_menu()
        if choice == 1:
            print ("\n"+"####################"*2)
            undermenu_print(stockobject_list)
            undermenu_choice = insertation(stockobject_list)-1
            if undermenu_choice == len(stockobject_list):
                program == False
            elif 0 <= undermenu_choice <= len(stockobject_list):
                current_stock = stockobject_list[undermenu_choice]
                fundamental_analysis(current_stock)
            
            else:
                print("Between "+"0 and "+str(len(stockobject_list))+ " please")

        elif choice == 2:
            print ("\n"+"####################"*2)
            undermenu_print(stockobject_list)
            undermenu_choice = insertation(stockobject_list)-1
            if undermenu_choice == len(stockobject_list):
                program == True
            elif 0 <= undermenu_choice <= len(stockobject_list)-1:
                current_stock = stockobject_list[undermenu_choice]
                technical_analysis(current_stock)
            else: 
                print("Between"+"0 and "+str(len(stockobject_list)))
        
        elif choice == 3:
            print ("\n"+"####################"*2)
            sorted_values = beta_value_sort(beta_value, stockobject_list)
            i = 1
            
            for betavalues in reversed(sorted_values):
                print(str(i)+".", end="")
                for values in betavalues:
                    print (str(values))
                i+=1 
            program = True

        elif choice == 4:
            print("You have choosen to quit. It's been a pleasure so far")
            program = False

#Huvudprogrammet
if __name__ == "__main__":
    main() 
