import pandas as pd
import openpyxl
#import pandas_datareader as web
# import streamlit as st

# data = pd.read_excel("DatabaseCS.xlsx")
data = pd.read_excel("/Users/lina/Desktop/APP/pages/cs.xlsx")


print(data.head())
print(data.columns)
print(data.iloc[0])