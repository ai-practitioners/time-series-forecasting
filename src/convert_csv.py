# source: https://stackoverflow.com/a/63912093
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/raw/forecasting.db')
c = conn.cursor()
calendar = pd.read_csv('data/raw/calendar.csv')
calendar.to_sql('calendar', conn, if_exists='append', index = False, chunksize = 10000)

train = pd.read_csv('data/raw/sales_train_evaluation.csv')
train.to_sql('train', conn, if_exists='append', index = False, chunksize = 10000)

prices = pd.read_csv('data/raw/sell_prices.csv')
prices.to_sql('prices', conn, if_exists='append', index = False, chunksize = 10000)
