import sqlite3 as sql
import os
import pandas as pd


class SQL_Manager:

    def __init__(self, db_name):

        self.db = db_name + '.db'
        self.current_folder = os.getcwd()
        self.connection = sql.connect(self.current_folder + '\\{}'.format(self.db))
        self.QueryCursor = self.connection.cursor()

        # print('\nEnvironnement :\t\t{}\n'.format(self.db))
        return

    def create_table(self, table_name, table_dictonnary):

        self.table_name = table_name
        temp = ''
        for k, v in table_dictonnary.items():
            if list(table_dictonnary.keys()).index(k) + 1 != len(table_dictonnary):
                creation = '{} {}, '.format(k, v.upper())
            else:
                creation = '{} {}'.format(k, v.upper())
            temp += creation

        query = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(self.table_name, temp)
        self.QueryCursor.execute(query)
        print('Table {} has been created'.format(self.table_name))
        return

    def table_list(self):

        query = 'SELECT name from sqlite_master where type= "table"'
        r = self.QueryCursor.execute(query)
        return r.fetchall()

    def get_table_as_df(self, table_name):

        query = 'SELECT * FROM {}'.format(table_name)
        df = pd.read_sql(query, self.connection)
        return df

    def print_table(self, table_name):

        print(self.get_table_as_df(table_name))

    def insert_values(self, table_name, insert_dict):
        temp = ''
        values = [
        ]
        inter = ''
        for k, v in insert_dict.items():
            if list(insert_dict.keys()).index(k) + 1 != len(insert_dict):
                creation = '{}, '.format(k)
                inter += '?,'
            else:
                creation = '{}'.format(k)
                inter += '?'
            value = '{}'.format(v)
            temp += creation
            values.append(value)

        query = 'INSERT INTO {} ({}) VALUES ({})'.format(table_name, temp, inter)
        print(query, tuple(values))
        self.QueryCursor.execute(query, tuple(values))
        self.connection.commit()
        return

    def update(self, table_name, modif_dict, field, spotter):

        for k, v in modif_dict.items():
            query = 'UPDATE {} SET {} = {} WHERE {} = "{}"'.format(table_name, field, v, k,spotter)
            self.QueryCursor.execute(query)
            self.connection.commit()

        return

    def close_connections(self):
        self.connection.close()

    def delete_all_records(self, table_name):
        query = 'DELETE FROM {}'.format(table_name)
        self.QueryCursor.execute(query)
        self.connection.commit()
        return

    def delete_row(self, table_name, field, spotter):
        query = 'DELETE  FROM {} WHERE {} = "{}"'.format(table_name, field, spotter)
        self.QueryCursor.execute(query)
        self.connection.commit()
        return
