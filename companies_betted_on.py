import tkinter as tk
from tkinter import ttk
from data_utils import *
from base_frame import BaseFrame

class CompaniesBettedOn(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        self.controller = controller
        self.selected_person = None

    def select_person(self, person_name):
        self.selected_person = person_name
        self.companies_betted()
    def companies_betted(self):
        person_id = get_or_add_person(self.selected_person)
        # Set up the combobox with unbet companies
        self.bolag_combobox = ttk.Combobox(self, values=get_unbet_companies(person_id), width=30)
        self.bolag_combobox.grid(row=2, column=1, pady=5)
        self.bolag_combobox.bind("<<ComboboxSelected>>", self.on_company_selected)

        # Set up the label for 'Bolag'
        ttk.Label(self, text="Bolag").grid(row=2, column=0, pady=5, sticky=tk.E)

                # Home button to return to the main page
        self.home_button = ttk.Button(self, text="Home", command=self.go_to_home_page)
        self.home_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)  # Adjust the grid position as per your layout needs

        # Menu button to navigate to the Menu
        self.menu_button = ttk.Button(self, text="Menu", command=self.go_to_person_page)
        self.menu_button.grid(row=4, column=0, pady=10, padx=10, columnspan=2)  # Adjust the grid position as per your layout needs



    def on_company_selected(self, event):
        selected_company = self.bolag_combobox.get()
        if selected_company:  # to ensure that it's not an empty string
            person_id = get_or_add_person(self.selected_person)
            # Update the company status in the database
            update_company_status(selected_company, person_id)

            # Update the list in the Combobox
            self.bolag_combobox['values'] = get_unbet_companies(get_or_add_person(self.selected_person))

            # You might want to clear the current value in the combobox
            self.bolag_combobox.set('')
