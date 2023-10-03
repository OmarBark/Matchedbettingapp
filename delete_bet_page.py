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

class DeleteBetPage(BaseFrame):

        
    def __init__(self, parent, controller):
        super().__init__(parent,controller)

        self.controller = controller
        self.selected_person = None

    def select_person(self, person_name):
        self.selected_person = person_name
        self.delete_bet()

    def delete_bet(self):


        person_id = get_or_add_person(self.selected_person)

        # Connect to the database
        conn = sqlite3.connect('bets.db')
        cursor = conn.cursor()

        # Retrieve bets for the selected person, including the unique ID
        cursor.execute('SELECT id, bolag, game_name, amount, back_odds, lay_odds, lay_stake, required_liability, loss_if_back_wins, loss_if_lay_wins FROM Bets WHERE person_id = ?', (person_id,))
        self.bets = cursor.fetchall()

        conn.close()

        if not self.bets:
            messagebox.showinfo("Previous Bets", "No previous bets for this person.")
            return

        # Create a Listbox to show the bets
        self.bets_listbox = tk.Listbox(self, width=150, height=20)
        self.bets_listbox.grid(row=0, column=0, padx=10, pady=10)

        for bet in self.bets:
            bet_display = f"Bolag: {bet[1]}, Game: {bet[2]}, Amount: {bet[3]}, Back Odds: {bet[4]}, Lay Odds: {bet[5]}, Lay Stake: {bet[6]}, Required Liability: {bet[7]}, Loss if Back Wins: {bet[8]}, Loss if Lay Wins: {bet[9]}"
            self.bets_listbox.insert(tk.END, bet_display)

        # Button to delete the selected bet
        self.delete_button = ttk.Button(self, text="Delete Bet", command=self.delete_selected_bet)
        self.delete_button.grid(row=1, column=0, pady=10, padx=10)

        # Home button to return to main page
        self.home_button = ttk.Button(self, text="Home", command=self.go_to_home_page)
        self.home_button.grid(row=2, column=0, pady=10, padx=10)

    def delete_selected_bet(self):
        # Get the selected bet from the listbox
        selected_index = self.bets_listbox.curselection()
        
        # If nothing is selected, return
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a bet to delete!")
            return
        
        # Get the actual bet data from the fetched bets (including the unique ID now)
        bet_to_delete = self.bets[selected_index[0]]
        
        # Ask for confirmation
        confirm = messagebox.askyesno("Delete Bet", "Are you sure you want to delete the selected bet?")
        if not confirm:
            return
        
        # Delete from the database
        conn = sqlite3.connect('bets.db')
        cursor = conn.cursor()
        
        # Use the unique ID to delete the bet
        cursor.execute('DELETE FROM Bets WHERE id = ?', (bet_to_delete[0],))
        
        conn.commit()
        conn.close()
        
        # Remove from the listbox
        self.bets_listbox.delete(selected_index)

