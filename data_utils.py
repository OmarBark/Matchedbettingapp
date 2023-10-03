import sqlite3
from data import *
df,data = df_data()

def init_db():
    conn = sqlite3.connect('bets.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS People (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bets (
        id INTEGER PRIMARY KEY,
        person_id INTEGER,
        game_name TEXT,
        bolag TEXT,
        amount REAL,
        back_odds REAL,
        lay_odds REAL,
        lay_stake REAL,
        required_liability REAL,
        loss_if_back_wins REAL,
        loss_if_lay_wins REAL,
        result TEXT DEFAULT NULL,  
        FOREIGN KEY(person_id) REFERENCES People(id)
    )
    ''')


    conn.commit()
    conn.close()


def get_or_add_person(name):
    conn = sqlite3.connect('bets.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM People WHERE name = ?', (name,))
    person_id = cursor.fetchone()

    if not person_id:
        try:
            cursor.execute('INSERT INTO People (name) VALUES (?)', (name,))
            conn.commit()
            person_id = (cursor.lastrowid,)
        except sqlite3.IntegrityError:  # name already exists in the database
            pass

    conn.close()
    return person_id[0] if person_id else None

def get_saved_persons():
    conn = sqlite3.connect('bets.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM People')
    persons = cursor.fetchall()

    conn.close()
    return [person[0] for person in persons]

def delete_person(name):
    conn = sqlite3.connect('bets.db')
    cursor = conn.cursor()

    # First, get the person's ID to delete related bets
    cursor.execute('SELECT id FROM People WHERE name = ?', (name,))
    person_id = cursor.fetchone()

    if person_id:
        # Delete the bets related to the person
        cursor.execute('DELETE FROM Bets WHERE person_id = ?', (person_id[0],))

        # Delete the person from the People table
        cursor.execute('DELETE FROM People WHERE name = ?', (name,))

        conn.commit()

    conn.close()


def get_companies_betted_on_by_person(person_id):
    conn = sqlite3.connect('bets.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT bolag FROM Bets WHERE person_id = ?', (person_id,))
    companies = cursor.fetchall()
    
    conn.close()
    return [company[0] for company in companies]

def get_unbet_companies(person_id):
    df,data = df_data()

    all_companies = data['Bolag']
    companies_betted_on = get_companies_betted_on_by_person(person_id)
    return list(set(all_companies) - set(companies_betted_on))

def update_company_status(selected_company, person_id):
    conn = sqlite3.connect('bets.db')
    cursor = conn.cursor()
    bonus_info = data['Bonusinformation'][data['Bolag'].index(selected_company)]
    bonus = -1 * float(bonus_info.split()[0])
    try:
        cursor.execute('''
            INSERT INTO Bets (person_id, bolag, game_name, amount, back_odds, lay_odds, lay_stake, required_liability, loss_if_back_wins, loss_if_lay_wins) 
            VALUES (?, ?, NULL, 0, 0, 0, 0, 0, ?, ?)
        ''', (person_id, selected_company, bonus, bonus))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error updating company status: {e}")
    conn.close()



