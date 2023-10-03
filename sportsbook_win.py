import sqlite3
import tkinter as tk
from tkinter import ttk
from data_utils import get_or_add_person
from base_frame import BaseFrame


class SportsBookWin(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.selected_person = None


    def select_person(self, person_name):
        self.selected_person = person_name

        self.setup_ui()


    def setup_ui(self):

        self.game_var = tk.StringVar()
        self.company_var = tk.StringVar()

        # Games dropdown
       
        self.games_dropdown = ttk.Combobox(self, textvariable=self.game_var,state='readonly')
        self.games_dropdown.bind('<<ComboboxSelected>>', self.on_game_selected)
        self.games_dropdown.grid(row=1, column=0, padx=10, pady=10)
        self.populate_games_dropdown()

        # Companies dropdown
        self.companies_dropdown = ttk.Combobox(self, textvariable=self.company_var)
        self.companies_dropdown.grid(row=1, column=1, padx=10, pady=10)

        # Total winnings and losses labels
        self.total_winnings_label = tk.Label(self, text="Total Winnings: 0.00")
        self.total_winnings_label.grid(row=2, column=0, padx=10, pady=10)

        self.total_losses_label = tk.Label(self, text="Total Losses: 0.00")
        self.total_losses_label.grid(row=2, column=1, padx=10, pady=10)

                # Adding descriptive text for the dropdown menus
        self.games_label = tk.Label(self, text="Select Game:")
        self.games_label.grid(row=0, column=0, padx=10, sticky='w')
        
        self.companies_label = tk.Label(self, text="Select Company:")
        self.companies_label.grid(row=0, column=1, padx=10, sticky='w')
        
        # Positioning dropdowns below their respective labels

        self.classify_win_button = tk.Button(self, text="Classify as Win", command=self.on_classify_as_win)
        self.classify_win_button.grid(row=3, column=0, pady=10)

        self.classify_loss_button = tk.Button(self, text="Classify as Loss", command=self.on_classify_as_loss)
        self.classify_loss_button.grid(row=3, column=1, pady=10)

        self.menu_button = ttk.Button(self, text="Menu", command=self.go_to_person_page)
        self.menu_button.grid(row=5, column=0, pady=10, padx=10)  # spans across two columns for center alignment
        # Check previous bets button

        # Home button to return to main page
        self.home_button = ttk.Button(self, text="Home", command=self.go_to_home_page)
        self.home_button.grid(row=5, column=1,  pady=10, padx=(5, 0))  # Added padx to the left side of the button

        self.company_totals_label = tk.Label(self, text="Select Company to View Totals:")
        self.company_totals_label.grid(row=4, column=0, padx=10, sticky='w')

        self.company_totals_var = tk.StringVar()
        self.company_totals_dropdown = ttk.Combobox(self, textvariable=self.company_totals_var, state='readonly')
        self.company_totals_dropdown.grid(row=4, column=1, padx=10, pady=10)

        self.populate_company_totals_dropdown()

        self.update_totals()  # Update totals when entering the page

    def populate_company_totals_dropdown(self):
        person_id = get_or_add_person(self.selected_person)
        with sqlite3.connect('bets.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT bolag FROM Bets WHERE person_id = ?', (person_id,))
            companies = cursor.fetchall()

        company_totals_list = []
        for company in companies:
            company_name = company[0]
            # Calculate total winnings for this company
                # Calculate total winnings for this company based on the condition
            cursor.execute('''
            WITH RankedBets AS (
                SELECT 
                    amount,
                    back_odds,
                    ROW_NUMBER() OVER(PARTITION BY bolag ORDER BY rowid) AS bet_rank
                FROM Bets
                WHERE person_id = ? AND bolag = ? AND result = "won"
            )
            SELECT 
                SUM(CASE 
                        WHEN bet_rank = 1 THEN amount * back_odds 
                        ELSE amount * back_odds - amount 
                    END) AS total_won
            FROM RankedBets;
            ''', (person_id, company_name,))
            total_won = cursor.fetchone()[0] or 0
            
            # Calculate total losses for this company
            cursor.execute('''
            SELECT SUM(amount) 
            FROM Bets
            WHERE person_id = ? AND bolag = ? AND result = "lost"
            ''', (person_id, company_name,))
            total_lost = cursor.fetchone()[0] or 0

            
            # Calculate the net amount for this company
            net_total = total_won - total_lost
            if (net_total<0):
                net_total=0
            company_totals_list.append(f"{company_name}: {net_total:.2f}")

        self.company_totals_dropdown['values'] = company_totals_list



    def populate_games_dropdown(self):
        person_id = get_or_add_person(self.selected_person)

        # Retrieve bets for the selected person
        with sqlite3.connect('bets.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT game_name FROM Bets WHERE person_id = ? AND game_name IS NOT NULL', (person_id,))
            games = [game[0] for game in cursor.fetchall()]
        
        self.games_dropdown['values'] = games


    def on_company_selected(self, event):
        selected_company = self.company_var.get()
        selected_game = self.game_var.get()
        person_id = get_or_add_person(self.selected_person)
        net_winnings=0
        total_losses=0
        with sqlite3.connect('bets.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT bolag FROM Bets WHERE person_id = ?', (person_id,))
            companies = cursor.fetchall()

        company_totals_list = []
        for company in companies:
            company_name = company[0]
            # Calculate total winnings for this company
            cursor.execute('''
            SELECT SUM(amount * back_odds) 
            FROM Bets
            WHERE person_id = ? AND bolag = ? AND result = "won"
            ''', (person_id, company_name,))
            total_won = cursor.fetchone()[0] or 0
            
            # Calculate total losses for this company
            cursor.execute('''
            SELECT SUM(amount) 
            FROM Bets
            WHERE person_id = ? AND bolag = ? AND result = "lost"
            ''', (person_id, company_name,))
            total_lost = cursor.fetchone()[0] or 0

            # Calculate the net amount for this company
            net_total = total_won - total_lost
        # Calculate the net winnings (total winnings - total losses)
            if(net_total>0):
                net_winnings += net_total
            else:
                total_losses += net_total
        
        # Update the labels with the calculated totals
        self.total_winnings_label.config(text=f"Net Winnings: {net_winnings:.2f}")
        self.total_losses_label.config(text=f"Total Losses: {total_losses:.2f}")

    def update_totals(self):
        person_id = get_or_add_person(self.selected_person)
        net_winnings = 0
        total_losses = 0

        with sqlite3.connect('bets.db') as conn:
            cursor = conn.cursor()
            
            # Fetch the distinct companies for the person
            cursor.execute('SELECT DISTINCT bolag FROM Bets WHERE person_id = ?', (person_id,))
            companies = cursor.fetchall()

            for company in companies:
                company_name = company[0]

                # Calculate total winnings for this company based on the condition
                cursor.execute('''
                WITH RankedBets AS (
                    SELECT 
                        amount,
                        back_odds,
                        ROW_NUMBER() OVER(PARTITION BY bolag ORDER BY rowid) AS bet_rank
                    FROM Bets
                    WHERE person_id = ? AND bolag = ? AND result = "won"
                )
                SELECT 
                    SUM(CASE 
                            WHEN bet_rank = 1 THEN amount * back_odds 
                            ELSE amount * back_odds - amount 
                        END) AS total_won
                FROM RankedBets;
                ''', (person_id, company_name,))
                total_won = cursor.fetchone()[0] or 0
                
                # Calculate total losses for this company
                cursor.execute('''
                SELECT SUM(amount) 
                FROM Bets
                WHERE person_id = ? AND bolag = ? AND result = "lost"
                ''', (person_id, company_name,))
                total_lost = cursor.fetchone()[0] or 0

                # Calculate the net amount for this company
                net_total = total_won - total_lost

                # Calculate the net winnings (total winnings - total losses)
                if net_total > 0:
                    net_winnings += net_total
                else:
                    total_losses -= net_total  # Subtract so the losses are positive

        # Update the labels with the calculated totals
        self.total_winnings_label.config(text=f"Money at spoortsbook: {net_winnings:.2f}")
        self.total_losses_label.config(text=f"Money in exchange: {total_losses:.2f}")


    def on_game_selected(self, event):
        selected_game = self.game_var.get()
        person_id = get_or_add_person(self.selected_person)

        with sqlite3.connect('bets.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT bolag FROM Bets WHERE person_id = ? AND game_name = ?' , (person_id, selected_game))
            companies = [company[0] for company in cursor.fetchall()]
        self.companies_dropdown['values'] = companies
        if companies:  # If there are companies, set the first one as default
            self.company_var.set(companies[0])

    def on_classify_as_win(self):
        if self.game_var.get() and self.company_var.get():
            self.classify_bet('won')
            self.update_totals()
        else:
            tk.messagebox.showwarning('Warning', 'Please select a Game and a Company first!')

    def on_classify_as_loss(self):
        if self.game_var.get() and self.company_var.get():
            self.classify_bet('lost')
            self.update_totals()
        else:
            tk.messagebox.showwarning('Warning', 'Please select a Game and a Company first!')

    def classify_bet(self, result):
        selected_company = self.company_var.get()
        selected_game = self.game_var.get()
        person_id = get_or_add_person(self.selected_person)

        with sqlite3.connect('bets.db') as conn:
            cursor = conn.cursor()
            # Modify Update Query as per the result won/lost
            cursor.execute('''UPDATE Bets SET result = ? 
                              WHERE person_id = ? AND game_name = ? AND bolag = ?''',
                           (result, person_id, selected_game, selected_company))
            conn.commit()

        # Refresh the companies dropdown
        self.on_game_selected(None)