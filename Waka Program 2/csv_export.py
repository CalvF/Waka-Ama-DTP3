import tkinter as tk
from tkinter import filedialo
import csv
from tkinter import filedialog


def export(regional_association_results):

  
    file_route = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV files", "*.csv")])
    
    if file_route:

        with open(file_route, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
           
            csv_writer.writerow(["Regional Association", "Score"])
            

            for association, score in regional_association_results.items():
                csv_writer.writerow([association, score])
        
        return file_route
    else:
        return False