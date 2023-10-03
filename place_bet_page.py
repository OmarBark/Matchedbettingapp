import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import ttk, Text, Button
from data import df,data
from data_utils import * 
from base_frame import BaseFrame

class PlaceBetPage(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent,controller)

        self.controller = controller
        self.selected_person = None

    def select_person(self, person_name):
        self.selected_person = person_name
        self.place_bet()

    def place_bet(self):
        df,data = df_data()

        ttk.Label(self, text="Place New Bet for {}".format(self.selected_person)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Game Name").grid(row=1, column=0, pady=5, sticky=tk.E)
        self.game_name_entry = ttk.Entry(self, width=30)
        self.game_name_entry.grid(row=1, column=1, pady=5)


        # Label for 'Bolag'
        ttk.Label(self, text="Bolag").grid(row=2, column=0, pady=5, sticky=tk.E)

        # Create a Combobox for 'Bolag'
        self.bolag_combobox = ttk.Combobox(self, values=data['Bolag'], width=30)
        self.bolag_combobox.grid(row=2, column=1, pady=5)



    
        ttk.Label(self, text="Total Amount").grid(row=3, column=0, pady=5, sticky=tk.E)
        self.amount_entry = ttk.Entry(self, width=30)
        self.amount_entry.grid(row=3, column=1, pady=5)


        ttk.Label(self, text="Back Odds").grid(row=4, column=0, pady=5, sticky=tk.E)
        self.back_odds_entry = ttk.Entry(self, width=30)
        self.back_odds_entry.grid(row=4, column=1, pady=5)

        ttk.Label(self, text="Lay Odds").grid(row=5, column=0, pady=5, sticky=tk.E)
        self.lay_odds_entry = ttk.Entry(self, width=30)
        self.lay_odds_entry.grid(row=5, column=1, pady=5)

        submit_button = ttk.Button(self, text="Calculate Bet", command=self.calculate_bet)
        submit_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Add labels for the results
        self.lay_stake_label = ttk.Label(self)
        self.lay_stake_label.grid(row=7, column=0, columnspan=2, pady=5)

        self.required_liability_label = ttk.Label(self)
        self.required_liability_label.grid(row=8, column=0, columnspan=2, pady=5)

        self.loss_if_back_wins_label = ttk.Label(self)
        self.loss_if_back_wins_label.grid(row=9, column=0, columnspan=2, pady=5)

        self.loss_if_lay_wins_label = ttk.Label(self)
        self.loss_if_lay_wins_label.grid(row=10, column=0, columnspan=2, pady=5)

        
        # Save button to save the bets
        save_button = ttk.Button(self, text="Save", command=self.save_bet)
        save_button.grid(row=12, column=0, columnspan=2, pady=10, padx=(0, 0))  # Added padx to the right side of the button

        self.menu_button = ttk.Button(self, text="Menu", command=self.go_to_person_page)
        self.menu_button.grid(row=12, column=1, pady=10, padx=10, columnspan=2)  # spans across two columns for center alignment
        # Check previous bets button
        check_bets_button = ttk.Button(self, text="Check Previous Bets", command=self.go_to_check_previous_bets)
        check_bets_button.grid(row=12, column=2, columnspan=2, pady=10, padx=(0, 0))  # Added padx to both sides of the button

        # Home button to return to main page
        self.home_button = ttk.Button(self, text="Home", command=self.go_to_home_page)
        self.home_button.grid(row=12, column=4, columnspan=2, pady=10, padx=(5, 0))  # Added padx to the left side of the button


    def calculate_bet(self):
        # Placeholder for matched_betting_calculator
        game_name = self.game_name_entry.get()
        bolag = self.bolag_combobox.get()
        amount_str = self.amount_entry.get()
        
        # Check if the string "Amount" is in the entry and remove it
        if "Amount" in amount_str:
            amount_str = amount_str.replace("Amount", "").strip()

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return

        back_odds = float(self.back_odds_entry.get())
        lay_odds = float(self.lay_odds_entry.get())

        lay_commission = 0.02  # For instance, 5% commission

        outcomes = self.matched_betting_outcomes(back_odds, lay_odds, lay_commission, amount)

        # Update the result labels
        self.lay_stake_label.config(text="Lay Stake: {:.2f}".format(outcomes['lay_stake']))
        self.required_liability_label.config(text="Required Liability: {:.2f}".format(-1*outcomes['required_liability']))
        self.loss_if_back_wins_label.config(text="Loss if Back Wins: {:.2f}".format(-1*outcomes['loss_if_back_wins']))
        self.loss_if_lay_wins_label.config(text="Loss if Lay Wins: {:.2f}".format(-1*outcomes['loss_if_lay_wins']))

    def save_bet(self):
        person_id = get_or_add_person(self.selected_person)
        game_name = self.game_name_entry.get()
        bolag = self.bolag_combobox.get()
        amount_str = self.amount_entry.get()

        if "Amount" in amount_str:
            amount_str = amount_str.replace("Amount", "").strip()

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return

        back_odds = float(self.back_odds_entry.get())
        lay_odds = float(self.lay_odds_entry.get())

        lay_commission = 0.02  # For instance, 5% commission

        outcomes = self.matched_betting_outcomes(back_odds, lay_odds, lay_commission, amount)

        # Connect to the database
        conn = sqlite3.connect('bets.db')
        cursor = conn.cursor()
        
        # Save the bet for the selected person
        cursor.execute('''
        INSERT INTO Bets (person_id, game_name, bolag, amount, back_odds, lay_odds, lay_stake, required_liability, loss_if_back_wins, loss_if_lay_wins) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (person_id, game_name, bolag, amount, back_odds, lay_odds, outcomes['lay_stake'], -1*outcomes['required_liability'], -1*outcomes['loss_if_back_wins'], -1*outcomes['loss_if_lay_wins']))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Bet saved successfully!")


    def matched_betting_outcomes(self,back_odds, lay_odds, lay_commission, stake):
        lay_stake = (back_odds * stake) / (lay_odds - lay_commission)
        liability_at_exchange = lay_stake * (lay_odds - 1)
        loss_if_back_wins = -1*((stake * back_odds - stake) - liability_at_exchange)
        commission_on_lay_win = (lay_stake * (1 - 1/lay_odds)) * lay_commission
        loss_if_lay_wins = stake - lay_stake*(1-lay_commission)

        return {
            'lay_stake': lay_stake,
            'required_liability': liability_at_exchange,
            'loss_if_back_wins': loss_if_back_wins,
            'loss_if_lay_wins': loss_if_lay_wins
        }
  