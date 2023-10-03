import pandas as pd

data = {
    'Bolag': ['Expekt', 'Speedybet', 'Bet365', 'No Account Bet', 'Bethard', 'Lyllocasino', 'x3000', 'Coolbet', 
              'Snabbare', 'Hajper', 'ComeOn', 'Nordicbet', 'Betsafe', 'Betsson'],
    'Bonusinformation': [
        '1500 free bet min 1.8 odds 1xbonus',
        '1000 min 1.5 odds 10xbonus',
        '1250 free bet min 1.2 odds 0xbonus ',
        '2000 min 1.5 odds 10xbonus ',
        '1000 min 1.8 odds 10xbonus ',
        '500 min 1.8 odds 12xbonus ',
        '1000 min 1.8 6x bonus ',
        '500 min 1.8 odds 6xbonus ',
        '500 min 1.8 odds 12xbonus ',
        '500 min 1.8 odds 12xbonus ',
        '500 min 1.8 odds 12xbonus ',
        '500 min 1.8 odds 6xbonus ',
        '500 min 1.8 odds 6xbonus ',
        '500 min 1.8 odds 6xbonus '
    ],
    'Koncern': ['', '', '', '', '', '', '', '', 'Koncern 1', 'Koncern 1', 'Koncern 1', 
                'Koncern 2', 'Koncern 2', 'Koncern 2']
}

df = pd.DataFrame(data)