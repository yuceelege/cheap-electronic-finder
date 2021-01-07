import tkinter as tk
import tkinter.font as font


class Window():
    def __init__(self,master,search=None):
        """
        Parameters
        ----------
        master : object
            tkinter master object.
        search : str
            searched product written in the entry box
        Returns
        -------
        None.

        """
        self.master = master
        self.search = search
        master.title('Cheapest Electronic Components')
        master.geometry('800x500')
        
        myFont = font.Font(family='Helvetica', size=18, weight='bold')
        label = tk.Label(master,text='Search an Electrical Component',font=myFont) 
        label.place(x =155,y =150)
        
        entry = tk.Entry(master,fg='black',bg='white',width=35)
        entry.place(x =255,y =250)
        
        def set_value():
            """
            Sets the entry box as search value
            Returns
            -------
            None.

            """
            self.search = entry.get()
            master.destroy()
        
        button = tk.Button(master,text='Show Results', command = set_value)
        button.place(x =330,y =350)
        
    def get_value(self):
        """
        Returns
        -------
        str
            value of the search parameter.
        """
        return self.search
    
    
