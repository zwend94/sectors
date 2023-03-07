import pandas as pd
from yahoo_fin import stock_info as si
import yfinance as yf
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Sector Heatmap",
    layout="wide")

spdrs = ['XLB',	'XLC',	'XLP',	'XLE',	'XLF',	'XLV',	'XLI',	'XLRE',	'XLK',	'XLU']
sec_names = ['Materials',	'Communications',	'Consumer Staples',	'Energy',	'Financials',	'Healthcare',	'Industrials',	'Real Estate',	'Tech',	'Utilities']

myd = {spdrs[x]:sec_names[x] for x in range(len(spdrs))}


def fetch_price_data(symbol, period, interval):
    #  valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,year,max
    #  valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    data = yf.download(tickers=symbol, period=period, interval=interval)
    
    prices_df = pd.DataFrame(data)
    prices_df.dropna(inplace=True)
    prices_df.reset_index(inplace=True)
    
    # prices_df.to_csv('sector_prices.csv')
    return prices_df

def calculate_returns(symbols, prices_dict):
    returns_df = pd.DataFrame()
    for symbol in symbols:
        #  Calculate return
        if symbol in prices_dict:
            prices_df = prices_dict[symbol]
            first_price = prices_df['Adj Close'].iloc[0]
            last_price = prices_df['Adj Close'].iloc[-1]
            return_rate = ((last_price - first_price) / first_price) * 100
            return_row = pd.DataFrame({'symbol': [symbol], 'return': [return_rate]})
            returns_df = pd.concat([returns_df, return_row], axis=0, ignore_index=True)
    return returns_df

# def get_prices()

ytd_dict = {}
year_dict = {}
quart_dict = {}
thirty_day_dict = {}
week_dict = {}
day_dict = {}

tickers = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLB', 'XLRE', 'XLK', 'XLU']

for etf in tickers:
    year_dict[etf] = si.get_data(ticker=etf, start_date="03-01-2022", interval="1d").close
    quart_dict[etf] = si.get_data(ticker=etf, start_date="12-06-2022", interval="1d").close
    thirty_day_dict[etf] = si.get_data(ticker=etf, start_date='02-06-2023', interval="1d").close
    week_dict[etf] = si.get_data(ticker=etf, start_date='02-28-2023', interval="1d").close
    ytd_dict[etf] = si.get_data(ticker=etf, start_date='01-01-2023', interval="1d").close
    
    thirty_df = pd.DataFrame(thirty_day_dict)
    quart_df = pd.DataFrame(quart_dict)
    year_df = pd.DataFrame(year_dict)
    week_df = pd.DataFrame(week_dict)
    ytd_df = pd.DataFrame(ytd_dict)
    
    
    thirty_rets = thirty_df.pct_change().dropna()
    quart_rets = quart_df.pct_change().dropna()
    year_rets = year_df.pct_change().dropna()
    week_rets = week_df.pct_change().dropna()
    ytd_rets = ytd_df.pct_change().dropna()

quart_rets_sum = round(quart_rets.sum()*100,2)
thirty_rets_sum = round(thirty_rets.sum()*100,2)
week_rets_sum = round(week_rets.sum()*100,2)
yearly_rets_sum = round(year_rets.sum()*100,2)
ytd_sum = round(ytd_rets.sum()*100,2)

mlr = dict(quart_rets_sum)
trl = dict(thirty_rets_sum)
wrl = dict(week_rets_sum)
yrl = dict(yearly_rets_sum)
yss = dict(ytd_sum)

tickl = list(wrl.keys())
prl = list(wrl.values())
qrl = list(trl.values())
mll = list(mlr.values())
ull = list(yrl.values())
ydd = list(yss.values())

tick_df = pd.DataFrame(tickl,columns=['ticker'])
prl_df = pd.DataFrame(prl,columns=['week'])
qrl_df = pd.DataFrame(qrl,columns=['month'])
mll_df = pd.DataFrame(mll,columns=['quarter'])
url_df = pd.DataFrame(ull,columns=['year'])
ydd_df = pd.DataFrame(ydd,columns=['ytd'])

hm_wk_df = pd.concat([tick_df,prl_df,qrl_df,mll_df,url_df,ydd_df],axis=1)

hm_wk_df.set_index(['ticker'],inplace=True)

cmap = LinearSegmentedColormap.from_list('RedGreenRed', ['lime', 'crimson'])
ax=sns.heatmap(hm_wk_df,cmap=cmap,vmin=5, vmax=-5, annot=True)
ax.set_title('Sector Returns')
st.write(plt.show())
