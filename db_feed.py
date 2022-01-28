from DataBaseManagement import SQL_Manager as dbm
import pandas as pd
from Provider import Markets

pd.set_option('max_columns', 500)


class InsertStatic:

    def __init__(self, excel):
        self.d = dbm('Prices')
        self.raw = pd.read_excel(excel, engine='openpyxl')

    def fill_db(self, table):
        for i in range(len(self.raw)):
            dict = {
                'ISIN': self.raw.iloc[i, 2],
                'NOM': self.raw.iloc[i, 0],
                'TICKER': self.raw.iloc[i, 1],
            }
            self.d.insert_values(table, dict)


class InsertMobile:

    def __init__(self):
        self.d = dbm('Prices')

    def fill_db(self, table):
        df = self.d.get_table_as_df(table)
        t = Markets(set(df['TICKER'].to_list())).daily_price_table(nb_days=10)

        spots = t.iloc[-1].round(3)

        tbis = t.pct_change()
        vars = round(tbis.iloc[-1] * 100, 4)

        for i in range(len(spots)):
            cursor = spots.index[i]
            var = vars.iloc[i]
            spot = spots.iloc[i]
            dict_ = {
                'TICKER': str(spot),

            }
            self.d.update(table_name=table, modif_dict=dict_, field='PRICE', spotter=cursor)

            dict_ = {
                'TICKER': str(var),

            }
            self.d.update(table_name=table, modif_dict=dict_, field='VAR', spotter=cursor)

# InsertMobile().fill_db('LivePrice')
