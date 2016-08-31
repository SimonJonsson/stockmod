from tkinter import *
from aktiekop import *
from functools import partial
#encode(utf-8)


LARGE_FONT= ("Arial", 12)
BIG_FONT = ("Arial", 10)


def main():
    omx_list = read_omx()
    omx_value = omx_development(omx_list)
    quotation_list_position = amount_stocks()
    fundamental_list = read_fundamental()
    omx_value = omx_development(omx_list)
    list_with_quotations = quotation_creator2(quotation_list_position)
    ratio_list = course_development(list_with_quotations)
    beta_value = betavalue_calc(omx_value, ratio_list)
    highest_v = highest_value(list_with_quotations)
    lowest_v = lowest_value(list_with_quotations)
    stockobject_list = stockobject_creator(fundamental_list,list_with_quotations,beta_value, highest_v, lowest_v, ratio_list)
    root = Tk()
    root.title("Stock buying programme")
    app = StockGui(root,stockobject_list,beta_value)
    root.mainloop()

#------Main menu
class StockGui:
    def __init__(self, root,stockobject_list,beta_value):
        frame = Frame(root,width=200,height=100)
        frame.pack()
        #checking the internet connection. A label is showing the connection level
        if network_try("http://www.google.com/") == True:
            label3 = Label(frame, text="You are currently online", font=BIG_FONT, fg="green")
            label3.pack()
        elif network_try("http://www.yahoo.com/finance") == False:
            label3 = Label(frame, text="You are currently Offline", font=BIG_FONT,fg="red")
            label3.pack()
        #adds a nice photo in the frame
        photo = PhotoImage(file="leotoast.gif")
        leophoto = Label(frame, image=photo)
        leophoto.photo = photo
        leophoto.pack()

        techbutton = Button(frame, text="Technical analysis",
                        command=lambda: self.tech_method(frame, root,stockobject_list, beta_value))
        techbutton.pack()
        fundabutton = Button(frame, text="Fundamental",
                        command=lambda: self.fund_method(frame, root,stockobject_list, beta_value))
        fundabutton.pack()
        betabutton = Button(frame, text="Sort by beta value",
                        command=lambda: self.beta_method(frame, root,stockobject_list, beta_value))
        betabutton.pack()
        quitbutton = Button(frame, text="Quit",
                        command=frame.quit)
        quitbutton.pack()
    
#those below functions acts like a terminal to the next frames
    def tech_method(self, frame, root, stockobject_list, beta_value):
        frame.pack_forget()
        frame = Frame(root)
        frame.pack()
        lala = Techanalysis(root,stockobject_list, beta_value) 

    def fund_method(self, frame, root,stockobject_list, beta_value):
        frame.pack_forget()
        frame = Frame(root)
        frame.pack()
        lala = Fund_analysis(frame,stockobject_list, beta_value) 

    def beta_method(self, frame, root,stockobject_list,beta_value):
        frame.pack_forget()
        frame = Frame(root)
        frame.pack()
        lala = Beta_analysis(frame, stockobject_list, beta_value) 

#-----Technical analysis
class Techanalysis(Frame):
    def __init__(self, root, stockobject_list, beta_value):
        frame = Frame(root)
        frame.pack()
        for stock in stockobject_list:
            
            stockbutton = Button(frame, text=str(stock.name),command= self.create_method(frame, root,stock))
            stockbutton.pack()

        gobackbutton2 = Button(frame, text="Go back",
                 command=lambda: self.go_back(frame, root,stockobject_list, beta_value))
        gobackbutton2.pack()

        quitbutton = Button(frame, text="Quit",
                command=frame.quit)
        quitbutton.pack()
        

    def go_back(self, frame, root, stockobject_list, beta_value):
        frame.pack_forget()
        frame = Frame(root,width=200,height=100) 
        frame.pack()
        Stockgraph = StockGui(root, stockobject_list, beta_value)

    def create_method(self,frame,root,stock):
            return lambda: self.tech_method2(frame,root,stock)

    def tech_method2(self, frame, root, value):
        frame.root.pack_forget()
        frame = Frame(root,width=200,height=100) 
        frame.pack()
        lala2 = Tech_print(frame,value)

class Tech_print(Frame):
    def __init__(self, master, value):
        frame = Frame(width=200,height=100)
        frame.pack_forget()
        frame.pack()
        labbe = Label(frame, text="Technical analysis", font=LARGE_FONT)
        labbe.pack()
        label3 = Label(frame, text=str(value.tech_analysis()), font=BIG_FONT)
        label3.pack()
        quitbutton = Button(frame, text="Quit",
                        command=frame.quit)
        quitbutton.pack()


#------Fundamental analysis
class Fund_analysis(Frame):
    def __init__(self, master,stockobject_list,beta_value):
        frame = Frame(master,width=200,height=100)
        frame.pack()
        for stock in stockobject_list:
            
            stockbutton = Button(frame, text=str(stock.name),command= self.create_method(frame, master, stock))
            stockbutton.pack()



        gobackbutton2 = Button(frame, text="Go back",
                 command=lambda: self.go_back(frame, master,stockobject_list, beta_value))
        gobackbutton2.pack()

        quitbutton = Button(frame, text="Quit",
                 command=frame.quit)
        quitbutton.pack()

    def go_back(self, frame, master, stockobject_list, beta_value):
        frame.master.pack_forget()
        frame = Frame(width=200,height=100) 
        frame.pack()
        Stockgraph = StockGui(frame, stockobject_list, beta_value)

    def create_method(self,frame,master,stock):
            return lambda: self.fund_method2(frame,master,stock)

    def fund_method2(self, frame, master, value):
        frame.master.pack_forget()
        frame = Frame() 
        frame.pack()
        fundamental_print = Fund_print(frame, value)

class Fund_print(Frame):
    def __init__(self, master, value):
        frame = Frame(master,width=200,height=100)
        frame.pack_forget()
        frame.pack()
        labbe = Label(frame, text="Fundamental analysis", font=LARGE_FONT)
        labbe.pack()
        label3 = Label(frame, text=value, font=BIG_FONT)
        label3.pack()
        gobackbutton2 = Button(frame, text="Go back",
                 command=lambda: self.go_back(frame, master,stockobject_list, beta_value))
        gobackbutton2.pack()

        quitbutton = Button(frame, text="Quit",
                 command=frame.quit)
        quitbutton.pack()

    def go_back(self, frame, master, stockobject_list, beta_value):
        frame.master.pack_forget()
        frame = Frame(width=200,height=100) 
        frame.pack()
        Stockgraph = StockGui(frame, stockobject_list, beta_value)
#--------Beta analysis
class Beta_analysis(Frame):
    def __init__(self, master,stockobject_list,beta_value):
        frame = Frame(master)
        frame.pack_forget()
        frame.pack()
        labbe = Label(frame, text="Stocks sorted after Beta-value", font=LARGE_FONT)
        labbe.pack()
        sorted_values = beta_value_sort(beta_value, stockobject_list)
        for values in reversed(sorted_values):
            label3 = Label(frame, text=values, font=BIG_FONT)
            label3.pack()
        
        gobackbutton2 = Button(frame, text="Go back",
                 command=lambda: self.go_back(frame, master,stockobject_list, beta_value))
        gobackbutton2.pack()

        quitbutton = Button(frame, text="Quit",
                 command=frame.quit)
        quitbutton.pack()

    def go_back(self, frame, master, stockobject_list, beta_value):
        frame.master.pack_forget()
        frame = Frame() 
        frame.pack()
        Stockgraph = StockGui(frame, stockobject_list, beta_value)

#Main program
if __name__ == "__main__":
    main() 


