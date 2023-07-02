# source: https://stackoverflow.com/a/63912093
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/raw/forecasting.db')
c = conn.cursor()
calendar = pd.read_csv('data/raw/calendar.csv')
calendar.to_sql('calendar', conn, if_exists='append', index = False, chunksize = 10000)

sales_train = pd.read_csv('data/raw/sales_train_evaluation.csv')
sales_train.to_sql('sales_train', conn, if_exists='append', index = False, chunksize = 10000)

sell_prices = pd.read_csv('data/raw/sell_prices.csv')
sell_prices.to_sql('sell_prices', conn, if_exists='append', index = False, chunksize = 10000)
