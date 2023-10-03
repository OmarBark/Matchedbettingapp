import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import ttk, Text, Button
from data import df,data
from data_utils import * 



class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
    def go_to_home_page(self):
        self.destroy_frame_contents()
        home = self.controller.frames['HomePage']
        home.home_button()
        self.controller.show_frame('HomePage')
    
    def destroy_frame_contents(self):
        for widget in self.winfo_children():
            widget.destroy()

    def go_to_check_previous_bets(self):
        person_page_frame = self.controller.frames['CheckPreviousBetPage']
        person_page_frame.select_person(self.selected_person)
        self.destroy_frame_contents()
        self.controller.show_frame('CheckPreviousBetPage')

    def go_to_place_new_bet_page(self):
        place_new_bet_page_frame = self.controller.frames['PlaceBetPage']
        place_new_bet_page_frame.select_person(self.selected_person)
        self.destroy_frame_contents()
        self.controller.show_frame('PlaceBetPage')

    def go_to_person_page(self):
        person_page_frame = self.controller.frames['PersonPage']
        person_page_frame.select_person(self.selected_person)
        self.destroy_frame_contents()
        self.controller.show_frame('PersonPage')  # Adjust the frame name accordingly

    def go_to_manage_companies(self):
        person_page_frame = self.controller.frames['ManageCompanies']
        person_page_frame.manage_companies()
        self.controller.show_frame('ManageCompanies')  

    def go_to_free_bet_page(self):
        free_bet_page = self.controller.frames['FreeBetPage']
        free_bet_page.select_person(self.selected_person)
        self.controller.show_frame('FreeBetPage')  

    def go_to_delete_bet(self):
        delete_bet_page = self.controller.frames['DeleteBetPage']
        delete_bet_page.select_person(self.selected_person)
        self.controller.show_frame('DeleteBetPage')  

    def go_to_companies_betted_on(self):
        companies_betted_on = self.controller.frames['CompaniesBettedOn']
        companies_betted_on.select_person(self.selected_person)
        self.destroy_frame_contents()
        self.controller.show_frame('CompaniesBettedOn')  

    def go_to_sportsbook_win(self):
        sportsbook_win = self.controller.frames['SportsBookWin']
        sportsbook_win.select_person(self.selected_person)
        self.destroy_frame_contents()
        self.controller.show_frame('SportsBookWin')  

        



