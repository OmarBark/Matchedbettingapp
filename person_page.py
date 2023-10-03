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


class PersonPage(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        self.controller = controller
        self.selected_person = None

    def select_person(self, person_name):
        self.selected_person = person_name
        self.setup_person_page()

    def setup_person_page(self):
        df,data = df_data()

        person_id = get_or_add_person(self.selected_person)


        self.selected_person_label = ttk.Label(self, text=f"Selected Person: {self.selected_person}")
        self.selected_person_label.grid(row=0, column=1, pady=10, padx=10)  # spans across two columns for center alignment

        # Button to view previous bets 
        self.check_bets_button = ttk.Button(self, text="Check Previous Bets", command=self.go_to_check_previous_bets)
        self.check_bets_button.grid(row=1, column=0, pady=10, padx=10)

        # Button to place a new bet
        self.new_bet_button = ttk.Button(self, text="Place a New Bet", command=self.go_to_place_new_bet_page)
        self.new_bet_button.grid(row=1, column=2, pady=10, padx=10)

                # Button to place a new bet
        self.free_bet_button = ttk.Button(self, text="Place a Free Bet", command=self.go_to_free_bet_page)
        self.free_bet_button.grid(row=2, column=2, pady=10, padx=10)


        self.sportsbook_win_btn = ttk.Button(self, text="sportsbook win", command=self.go_to_sportsbook_win)
        self.sportsbook_win_btn.grid(row=2, column=1, pady=10, padx=10) 

        self.companies_betted_on_btn = ttk.Button(self, text="Companies Betted On", command=self.go_to_companies_betted_on)
        self.companies_betted_on_btn.grid(row=2, column=0, pady=10, padx=10) 

        # Home button to return to main page


        self.home_button = ttk.Button(self, text="Home", command=self.go_to_home_page)
        self.home_button.grid(row=6, column=1, pady=10, padx=10)  # spans across two columns for center alignment

        total_net_profit = 0
        # Retrieve bets for the selected person

        # Connect to the database
        conn = sqlite3.connect('bets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT bolag, game_name, amount, back_odds, lay_odds, lay_stake, required_liability, loss_if_back_wins, loss_if_lay_wins FROM Bets WHERE person_id = ?', (person_id,))
        bets = cursor.fetchall()
        all_bolags = list(set(bet[0] for bet in bets))  # assuming `bets` is globally available or fetched in this context
        for bolag in all_bolags:
            bonus_info = data['Bonusinformation'][data['Bolag'].index(bolag)]
            bonus = float(bonus_info.split()[0])
            initial_amount = float(bonus_info.split()[0])*2
            bolag_bets = [bet for bet in bets if bet[0] == bolag]
            
            net_profit = initial_amount - bonus
            for bet in bolag_bets:
                net_profit += bet[7]
            
            total_net_profit += net_profit

        # Display the total_net_profit in the GUI
        self.total_net_profit_label = ttk.Label(self, text=f"Total net profit across all bolags: {total_net_profit:.2f}")
        self.total_net_profit_label.grid(row=3, column=1, pady=10, padx=10)  # spans across two columns for center alignment

                # Assuming data['Bolag'] contains a list of all bolags
        all_possible_bolags = data['Bolag']
        
        # Get unbet companies from the database
        unbet_companies = get_unbet_companies(person_id)  # You already have this function
        
        # Compute bolags not bet on
        bolags_not_bet_on = list(set(unbet_companies))
        
        total_bonus_from_unbet_bolags = 0
        for bolag in bolags_not_bet_on:
            bonus_info = data['Bonusinformation'][data['Bolag'].index(bolag)]
            bonus = float(bonus_info.split()[0])
            total_bonus_from_unbet_bolags += bonus
        
               # Display the bolags not bet on and the total bonus in the GUI
        bolags_not_bet_on_str = ", ".join(bolags_not_bet_on)

        
        self.bolags_not_bet_on_label = ttk.Label(self, text=f"Bolags not bet on: ")
        self.bolags_not_bet_on_label.grid(row=4, column=0, pady=10, padx=5, sticky='e')
        self.bolags_not_bet_on = ttk.Combobox(self, values=bolags_not_bet_on, state='readonly')
        self.bolags_not_bet_on.grid(row=4, column=1, padx=5, pady=10)

        self.total_bonus_label = ttk.Label(self, text=f"Total bonuses from bolags not bet on: {total_bonus_from_unbet_bolags:.2f}")
        self.total_bonus_label.grid(row=5, column=1, pady=10, padx=10)
