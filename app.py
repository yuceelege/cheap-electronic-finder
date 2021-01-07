import main
import tkinter as tk
import tkinter.font as font
import os
import sys
import pandas as pd
from PIL import ImageTk, Image
import webbrowser 

#Confirms that main.py ended
while main.wait:
    pass

#Extracts the data of products
df = pd.read_csv('results.csv', delimiter=',',encoding = "unicode_escape")



class Option():
    def __init__(self,name,price,img_index,link):
        """
        Parameters
        ----------
        name : str
            name of the product.
        price : str
            price of the product.
        img_index : str
            number of the image of product in images file.
        link : str
            link of the product.
        Returns
        -------
        None.
        """
        self.__name = name
        self.__price = price
        self.__index = img_index
        self.__link = link
        
    def get_name(self):
        """
        Returns
        -------
        str
            name of the product object.
        """
        return self.__name
    
    def get_price(self):
        """
        Returns
        -------
        str
            price of the product object.
        """
        return self.__price
    
    def get_img(self):
        """
        Returns
        -------
        str
            img index of the product object.
        """
        return self.__index
    
    def get_link(self):
        """
        Returns
        -------
        str
            link of the product object.
        """
        return self.__link

    
#Creates a list consisting of product objects
option = []
for row in range(len(df)):
    option.append(Option(df.iloc[row][0],df.iloc[row][1],df.iloc[row][2],df.iloc[row][3]))
    
display = tk.Tk()
display.geometry('1800x900')
display.title('Best Results')

myfont = font.Font(family='Helvetica', size=15)
positions = [x for x in range(0,800,200)]


class Frame():
    def __init__(self,obj,position):
        """
        Parameters
        ----------
        obj : object
            product .
        position : int
            order of the products on display page.
        Returns
        -------
        None.
        """
        self.obj = obj
        self.position = position
    def create_frame(self):
        """
        Generates a frame that consists the product object

        Returns
        -------
        None.

        """
        frame = tk.Frame(display, bg='white', width=1800, height=200)
        frame.place(x = 0,y = int(self.position))
        l1 = tk.Label(frame,text = self.obj.get_name(),font = myfont)
        l1.place(x =20,y = 80)
        l2 = tk.Label(frame,text = "Price: "+str(self.obj.get_price()),font = myfont)
        l2.place(x =1200,y = 80)
        label = tk.Label(frame)
        img = Image.open(r"images\{}.jpg".format(str(self.obj.get_img())))
        img = img.resize((150, 150), Image.ANTIALIAS)
        label.img = ImageTk.PhotoImage(img)
        label['image'] = label.img
        label.place(x = 850, y = 0)
        
        def callback():
            """
            Goes to the website to buy the product by using hyperlink
            Returns
            -------
            None.

            """
            webbrowser.open_new(str(self.obj.get_link()))
            
        button = tk.Button(frame,text='Buy', command = callback)
        button.place(x =1600,y =80)


page = 1
page_max = len(option)//4+int(bool(len(option)%4))

def frame_display(pg):
    """
    Initiates the create_frame function for the appropriate page
    Parameters
    ----------
    pg : int
        Current page number
    Returns
    -------
    None.

    """
    try:
        for n,i in enumerate([p+(pg-1)*4 for p in range(4)]):
            x = Frame(option[i],positions[n]).create_frame()
    except:
        pass
   
def pg_forward():
    """
    Moves to the following page
    Returns
    -------
    None.

    """
    global page
    if not page == page_max:
        page += 1
    frame_display(page)

    
def pg_back():
    """
    Moves to the back page
    Returns
    -------
    None.

    """
    global page
    if not page == 1:
        page -= 1
    frame_display(page)
    
def quit_page():
    """
    Quits the page and deletes the unnecessary files

    Returns
    -------
    None.

    """
    d = 'images'
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    os.remove('results.csv')
    display.destroy()
    os.rmdir('images')
        

frame_display(page)
    
button2 = tk.Button(display,text='Forward', command = pg_forward)
button2.place(x =1650,y =800)

button3 = tk.Button(display,text='Back', command = pg_back)
button3.place(x =1600,y =800)

button3 = tk.Button(display,text='Quit', command = quit_page)
button3.place(x =1730,y =800)


display.mainloop()