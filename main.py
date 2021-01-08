import search
import tkinter as tk
import requests
from bs4 import BeautifulSoup
import numpy as np
import sys
import os

try:
    os.makedirs('images')
except:
    d = 'images'
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))

root = tk.Tk()
page = search.Window(root)
root.mainloop()
wait = True
target = page.get_value()

img_count = 0
p_name = []
prices = []
image_list = []
links = []

def image_downloader(lst): 
    """
    Parses the image file from html code and downloads it
    Parameters
    ----------
    lst : list
        html code.
    Returns
    -------
    None.
    """
    global img_count
    for img in lst:
        response = requests.get(img)
        file = open("images\{}.jpg".format(img_count+1), "wb")
        file.write(response.content)
        file.close()
        img_count +=1
        
def price_fixer(price):
    """
    Removes the unnecessary strings from the price tag
    Parameters
    ----------
    price : str
        raw price decription taken from the website.

    Returns
    -------
    float
        filtered price .
    """
    price = price.replace('KDV',"")
    price = price.replace('TL',"")
    price = price.replace('+',"")
    price = price.replace('.',"")
    price = price.replace(',',".")
    price = price.replace('\n',"")
    price = price.replace(' ',"")
    return float(price)


try:
    if len(target.strip().split()) !=1:
        target = target.strip().replace(" ","+")
except:
    sys.exit()
 
url = 'https://www.robotistan.com/arama?q={}'.format(target)

r = requests.get(url)
soup = BeautifulSoup(r.text,'html5lib')
lst = soup.find_all("div",{"class":"col col-3 col-md-4 col-sm-4 col-xs-6 productItem ease"})


#Parsing information from https://www.robotistan.com
for p in lst:
    link = "robotistan.com"+p('a',{'class':'col col-12 productDescription'})[0].get('href')
    links.append(link)
    name = p('a',{'class':'col col-12 productDescription'})[0].get('title')
    name += ' -Robotistan'
    name = name.replace(","," ")
    price = p('div',{'class':'currentPrice'})[0].text
    p_name.append(name)
    try:
        prices.append(price_fixer(price))
    except:
        prices.append('unknown')
        
    image = p('img',{'class':"active"})[0].get('src')
    image_list.append(image)

  
r.close()


#Parsing information from https://www.direnc.net
url2 = 'https://www.direnc.net/arama?q={}'.format(target)

r2 = requests.get(url2)
soup2 = BeautifulSoup(r2.text,'html5lib')

lst2 = soup2.find_all("div",{"class":"fl col-3 col-md-4 col-sm-6 col-xs-12 productItem ease"})

for p in lst2:
    link = "direnc.net"+p.find_all('a',{'class':'col col-12 productDescription'})[0].get('href')
    links.append(link)
    name = p.find_all('a',{'class':'col col-12 productDescription'})[0].get('title')
    name += ' - Direnc'
    name = name.replace(","," ")
    price = p('span',{'class':'currentPrice'})[0].text
    p_name.append(name)
    try:
        prices.append(price_fixer(price))
    except:
        prices.append('unknown')
        print('hey',price)
    image = p('span',{'class':'imgInner'})[0]('img')[0].get('data-src')
    image_list.append(image)

r2.close()


image_downloader(image_list) 

#Gathers all the data into single multidimendional numpy array
final_p = np.column_stack((np.array(p_name),np.array(prices).astype(np.object)
,np.arange(1,len(image_list)+1).astype(np.object),np.array(links)))

#Sorts the data according price in an ascending order
final_sorted = final_p[np.argsort(final_p[:, 1])]

#Saves the final data into a csv file
np.savetxt('results.csv',final_sorted,delimiter=',',fmt='%s')

#This is a flag for the next script (app.py)
wait = False
