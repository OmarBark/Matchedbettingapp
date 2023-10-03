import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import ttk, Text, Button
from data import df,data
from data_utils import * 
from data import add_company,delete_company
from base_frame import BaseFrame

class ManageCompanies(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.manage_companies()

    def manage_companies(self):
        df,data = df_data()

        ttk.Label(self, text="Company").grid(row=0, column=0, pady=5, sticky=tk.E)
        self.bolag_combobox = ttk.Combobox(self, values=df_data()[1]['Bolag'], width=30)
        self.bolag_combobox.grid(row=0, column=1, pady=5)
        self.delete_company_btn = ttk.Button(self, text="Delete Company", command=self.delete_company, width=30)
        self.delete_company_btn.grid(row=0, column=2, pady=5)

        ttk.Label(self, text="New Company").grid(row=1, column=0, pady=5, sticky=tk.E)
        self.new_bolag_entry = ttk.Entry(self, width=30)
        self.new_bolag_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Bonus Information").grid(row=2, column=0, pady=5, sticky=tk.E)
        self.bonusinformation_entry = ttk.Entry(self, width=30)
        self.bonusinformation_entry.grid(row=2, column=1, pady=5)

        instruction_frame = ttk.Frame(self)
        instruction_frame.grid(row=2, column=2, rowspan=3, padx=10)  # rowspan to cover multiple rows

        instruction_text = tk.Text(instruction_frame, height=5, width=30, wrap='word')
        instruction_text.pack()
        instruction_text.insert(tk.END, "Write like this 500 min 1.8 odds 6xbonus\n"
                                      "If it is a free bet write:\n"
                                      "500 free bet min 1.8 odds 6xbonus")
        instruction_text.config(state='disabled')  # To make it read-only

        # Optionally, you can adjust fonts, background, etc., as needed
        instruction_text.config(font=("Arial", 15), bg="#F0F0F0")

        ttk.Label(self, text="Koncern").grid(row=3, column=0, pady=5, sticky=tk.E)
        self.koncern_entry = ttk.Entry(self, width=30)
        self.koncern_entry.grid(row=3, column=1, pady=5)

        self.add_company_ = ttk.Button(self, text="Add Company", command=self.add_company_btn, width=30)
        self.add_company_.grid(row=4, column=1, pady=5)

                # Home button to return to main page
        self.home_button = ttk.Button(self, text="Home", command=self.go_to_home_page)
        self.home_button.grid(row=5, column=1,  pady=10, padx=(5, 0))  # Added padx to the left side of the button
        
    def add_company_btn(self):
        bolag = self.new_bolag_entry.get()
        bonusinformation = self.bonusinformation_entry.get()
        koncern = self.koncern_entry.get()
        if bolag and bonusinformation and koncern:
            add_company(bolag, bonusinformation, koncern)
            messagebox.showinfo('Success', 'Company added successfully')
        else:
            messagebox.showerror('Error', 'All fields are required')
            
    def delete_company(self):
        bolag = self.bolag_combobox.get()
        if bolag:
            delete_company(bolag)
            messagebox.showinfo('Success', 'Company deleted successfully')
        else:
            messagebox.showerror('Error', 'Please select a company to delete')

class DummyController:
    def show_frame(self, frame_name):
        print(f"Switching to frame: {frame_name}")
        
    def go_to_home_page(self):
        print("Going to home plöage")


if __name__ == "__main__":
    root = tk.Tk()
    controller = DummyController()  # Dummy controller to avoid errors
    frame = ManageCompanies(root, controller)
    frame.pack(fill="both", expand=True)
    frame.manage_companies()  # Call the method to create widgets
    root.mainloop()