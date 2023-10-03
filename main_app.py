#!/usr/bin/env python3


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




from delete_bet_page import DeleteBetPage
from check_previous_bets_frame import CheckPreviousBetPage
from home_page import HomePage
from person_page import PersonPage
from place_bet_page import PlaceBetPage
from base_frame import BaseFrame
from manage_companies import ManageCompanies
from free_bet_page import FreeBetPage
from companies_betted_on import CompaniesBettedOn
from sportsbook_win import SportsBookWin
from ttkthemes import ThemedTk


class BettingAppController(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # You can set the theme of your choice
        self.set_theme('arc')  
        

        self.title('Betting App')
        self.geometry('800x500')

        self.selected_person = None
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)
        
        self.frames = {}
        
        frame_classes = {
            HomePage: 'HomePage',
            PersonPage: 'PersonPage',
            CheckPreviousBetPage:'CheckPreviousBetPage',
            PlaceBetPage : 'PlaceBetPage',
            ManageCompanies: 'ManageCompanies',
            FreeBetPage: 'FreeBetPage',
            DeleteBetPage: 'DeleteBetPage',
            CompaniesBettedOn:'CompaniesBettedOn',
            SportsBookWin : 'SportsBookWin'

        }
        
        for cls, name in frame_classes.items():
            frame = cls(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame('HomePage')
        
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == '__main__':
    init_db()  # initialize the database before running the app

    app = BettingAppController()
    app.mainloop()
