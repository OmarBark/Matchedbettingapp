import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import ttk, Text, Button
from data import df,data, df_data
from data_utils import * 
from base_frame import BaseFrame


class HomePage(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        
        # Creating the Treeview to show all bets
        columns = list(df.columns)
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.W, width=200)

        for _, row in df.iterrows():
            self.tree.insert('', 'end', values=list(row))

        self.tree.grid(row=0, column=0, columnspan=4,padx=60, pady=10)  # span across 4 columns for better layout

        # Dropdown menu (combobox) for saved persons
        self.saved_persons_combobox = ttk.Combobox(self, values=get_saved_persons(), state='readonly')
        self.saved_persons_combobox.grid(row=1, column=0, padx=10, pady=10)

        # Button to select a saved person
        self.select_saved_person_btn = ttk.Button(self, text="Select Saved Person", command=self.select_saved_person)
        self.select_saved_person_btn.grid(row=1, column=1, padx=10, pady=10)

        # Button to delete a person
        self.delete_person_btn = ttk.Button(self, text="Delete Person", command=self.delete_selected_person)
        self.delete_person_btn.grid(row=1, column=2, columnspan=2, pady=10)  # center align by spanning across 2 columns

        # Entry to create a new person
        self.new_person_entry = ttk.Entry(self)
        self.new_person_entry.grid(row=2, column=0, padx=10, pady=10)

        # Button to create a new person
        self.create_new_person_btn = ttk.Button(self, text="Create New Person", command=self.create_new_person)
        self.create_new_person_btn.grid(row=2, column=1, padx=10, pady=10)

        self.manage_companies_btn = ttk.Button(self, text="Manage Companies", command=self.go_to_manage_companies)
        self.manage_companies_btn.grid(row=2, column=2, padx=10, pady=10)
    def home_button(self):
        df,data = df_data()
        columns = list(df.columns)
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.W, width=200)

        for _, row in df.iterrows():
            self.tree.insert('', 'end', values=list(row))

        self.tree.grid(row=0, column=0, columnspan=4,padx=60, pady=10)  # span across 4 columns for better layout

        # Dropdown menu (combobox) for saved persons
        self.saved_persons_combobox = ttk.Combobox(self, values=get_saved_persons(), state='readonly')
        self.saved_persons_combobox.grid(row=1, column=0, padx=10, pady=10)

        # Button to select a saved person
        self.select_saved_person_btn = ttk.Button(self, text="Select Saved Person", command=self.select_saved_person)
        self.select_saved_person_btn.grid(row=1, column=1, padx=10, pady=10)

        # Button to delete a person
        self.delete_person_btn = ttk.Button(self, text="Delete Person", command=self.delete_selected_person)
        self.delete_person_btn.grid(row=1, column=2, columnspan=2, pady=10)  # center align by spanning across 2 columns

        # Entry to create a new person
        self.new_person_entry = ttk.Entry(self)
        self.new_person_entry.grid(row=2, column=0, padx=10, pady=10)

        # Button to create a new person
        self.create_new_person_btn = ttk.Button(self, text="Create New Person", command=self.create_new_person)
        self.create_new_person_btn.grid(row=2, column=1, padx=10, pady=10)

        self.manage_companies_btn = ttk.Button(self, text="Manage Companies", command=self.go_to_manage_companies)
        self.manage_companies_btn.grid(row=2, column=2, padx=10, pady=10)
            


    def create_new_person(self):
        new_person_name = self.new_person_entry.get().strip()

        if new_person_name:
            person_id = get_or_add_person(new_person_name)
            
            if person_id:
                print(f"{new_person_name} has been added with ID {person_id}")
                
                # Update combobox values to include the new person
                current_values = self.saved_persons_combobox["values"]
                self.saved_persons_combobox["values"] = (*current_values, new_person_name)
            else:
                print(f"There was an issue adding {new_person_name}. It might already exist!")
        else:
            print("Please enter a valid name to add!")

    def delete_selected_person(self):
        selected_person = self.saved_persons_combobox.get()

        if not selected_person:
            messagebox.showerror("Error", "Please select a person to delete!")
            return

        # Ask for confirmation
        answer = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {selected_person} and all their related bets?")

        if answer:
            delete_person(selected_person)
            messagebox.showinfo("Deleted", f"{selected_person} and their bets have been deleted!")

            # Update combobox values to remove the deleted person
            current_values = list(self.saved_persons_combobox["values"])
            current_values.remove(selected_person)
            self.saved_persons_combobox["values"] = tuple(current_values)


    def select_saved_person(self):
        selected_person = self.saved_persons_combobox.get()


        if selected_person:
            # Assuming you have some functionality to handle the selected person
            self.controller.selected_person = selected_person
            person_page_frame = self.controller.frames['PersonPage']
            person_page_frame.select_person(selected_person)
            self.controller.show_frame('PersonPage')  # Adjust the frame name accordingly


