import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import *

class GuiComponent:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("WakaAma Program")
        self.label = tk.Label(self.window, text="WakaAma Program")
        self.label.pack()
    
    # util methods
    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            print(f"Selected folder: {folder_path}")
            self.selectYear(folder_path)

    # screens
    def home_screen(self):
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()
        # add button
        button = tk.Button(
            self.window,
            text="Open Folder",
            width=25,
            height=5,
            bg="blue",
            fg="yellow",
            command=self.open_folder  # Link the button to the function
        )
        button.pack()
        
        self.window.mainloop()
    
    # second page
    def selectYear(self, folder_path):
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Add a label
        self.label = tk.Label(self.window, text=f"Selected folder: {folder_path}")
        self.label.pack()

        # create lower_frame    




        # Create a listbox frame
        year_listbox_frame = Frame(self.window)
        year_listbox_frame_scrollbar = Scrollbar(year_listbox_frame, orient=VERTICAL)

        
        # Create a Listbox 
        year_listbox_font = tkFont.Font(family="Helvetica",size="30")
        year_listbox = tk.Listbox(year_listbox_frame,width=15,height=5,yscrollcommand=year_listbox_frame_scrollbar.set,font=year_listbox_font)

        # configure scrollbar
        year_listbox_frame_scrollbar.config(command=year_listbox.yview)
        year_listbox_frame_scrollbar.pack(side=RIGHT, fill=Y)
        year_listbox_frame.grid()




        # Add items to the Listbox 
        years = ['2017','2018','2019','2020','2021','2022','2023','2024']
        

        for i in years:
            year_listbox.insert(tk.END, i)
        
        year_listbox.pack()


        
        
        
    def second_page(self):
        # Add functionality for the second page here
        pass
        
win = GuiComponent()
win.home_screen()



































class gui_c():
    def __init__(self):
        pass

    def show_HomeScreen(self):
        pass

    def show_SelectYearScreen(self):
        pass

    def show_ErrorScreen(self):
        pass

    def show_LoadingScreen(self):
        pass

    def show_ExitConfirmation(self):
        pass

    def show_HelpScreen(self):
        pass

    def show_Successful_SaveResultsScreen(self):
        pass

    def show_LogsScreen(self):
        pass

    def show_ResultsScreen(self):
        pass