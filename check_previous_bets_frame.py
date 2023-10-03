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

class CheckPreviousBetPage(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent,controller)

        self.controller = controller
        self.selected_person = None

    def select_person(self, person_name):
        self.selected_person = person_name
        self.check_previous_bets()

    def check_previous_bets(self):




        person_id = get_or_add_person(self.selected_person)

        # Connect to the database
        conn = sqlite3.connect('bets.db')
        cursor = conn.cursor()

        # Retrieve bets for the selected person

        cursor.execute('SELECT bolag, game_name, amount, back_odds, lay_odds, lay_stake, required_liability, loss_if_back_wins, loss_if_lay_wins FROM Bets WHERE person_id = ?', (person_id,))
        bets = cursor.fetchall()

        conn.close()
        if not bets:
            messagebox.showinfo("Previous Bets", "No previous bets for this person.")

            self.home_button = ttk.Button(self, text="Home", command=self.go_to_home_page)
            self.home_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

            self.menu_button = ttk.Button(self, text="Menu", command=self.go_to_person_page)
            self.menu_button.grid(row=5, column=0, pady=10, padx=10, columnspan=2)  # spans across two columns for center alignment
            return

        # Extract unique bolags
        bolags = list(set(bet[0] for bet in bets))
        # Extract unique game names
        games = list(set(bet[1] for bet in bets))

        # Combobox for selecting bolag
        ttk.Label(self, text="Bolag").grid(row=0, column=0, pady=5)
        bolag_combobox = ttk.Combobox(self, values=bolags)
        bolag_combobox.grid(row=0, column=1, pady=5, padx=10)

        # Combobox for selecting games
        ttk.Label(self, text="Game").grid(row=1, column=0, pady=5)
        game_combobox = ttk.Combobox(self, values=games)
        game_combobox.grid(row=1, column=1, pady=5, padx=10)

        details = tk.StringVar()

        def show_bolag_details(event):
            selected_bolag = bolag_combobox.get()
            bolag_bets = [bet for bet in bets if bet[0] == selected_bolag]
            bonus_info = data['Bonusinformation'][data['Bolag'].index(selected_bolag)]
            bonus =  float(bonus_info.split()[0])
            initial_amount =  float(bonus_info.split()[0])*2
            # Calculate net profit for the selected bolag

            net_profit = initial_amount - bonus

            for bet in bolag_bets:
                net_profit += bet[7]

            # Display bonus info and net profit
            details.set(f"Bonus Information: {bonus_info}\nNet Profit: {net_profit:.2f}\n")

        bolag_combobox.bind("<<ComboboxSelected>>", show_bolag_details)

        def show_game_details(event):
            selected_game = game_combobox.get()
            game_bets = [bet for bet in bets if bet[1] == selected_game]
            bet_strings = []
            for bet in game_bets:
                bet_string = (
                    f"Bolag: {bet[0]}, "
                    f"Game: {bet[1]}, "
                    f"Amount: {round(bet[2], 2)}, "  # rounding here
                    f"Back Odds: {round(bet[3], 2)}, "  # rounding here
                    f"Lay Odds: {round(bet[4], 2)}, "  # rounding here
                    f"Lay Stake: {round(bet[5], 2)}, "  # rounding here
                    f"Required Liability: {round(bet[6], 2)}, "  # rounding here
                    f"Loss if Back Wins: {round(bet[7], 2)}, "  # rounding here
                    f"Loss if Lay Wins: {round(bet[8], 2)}"  # rounding here
                )
                bet_strings.append(bet_string)
            details.set("\n\n".join(bet_strings))

        game_combobox.bind("<<ComboboxSelected>>", show_game_details)

        # Text widget to display game details
        game_details_label = tk.Label(self, textvariable=details, justify=tk.LEFT)
        game_details_label.grid(row=2, column=0, pady=10, padx=10, columnspan=2)

        # Home button to return to main page
        self.home_button = ttk.Button(self, text="Home", command=self.go_to_home_page)
        self.home_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)
                # Home button to return to main page


        self.delete_bet_button = ttk.Button(self, text="Detele bet", command=self.go_to_delete_bet)
        self.delete_bet_button.grid(row=4, column=0, columnspan=2, pady=10, padx=(5, 0))  # Added padx to the left side of the button

        self.menu_button = ttk.Button(self, text="Menu", command=self.go_to_person_page)
        self.menu_button.grid(row=5, column=0, pady=10, padx=10, columnspan=2)  # spans across two columns for center alignment



