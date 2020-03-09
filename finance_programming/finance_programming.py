"""
DOCSTRING
"""
import bs4
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as pyplot
import matplotlib.style as style
import mplfinance.original_flavor as mplfinance
import pandas
import pandas_datareader.data as web
import pickle
import requests

style.use('ggplot')

def get_data():
    """
    DOCSTRING
    """
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime(2016, 12, 31)
    dataframe_a = web.DataReader('GOOGL', 'yahoo', start, end)
    dataframe_a.to_csv('google.csv')

def graph_data():
    """
    DOCSTRING
    """
    dataframe_a = pandas.read_csv('google.csv', parse_dates=True, index_col=0)
    dataframe_a.plot()
    pyplot.show()

def manipulate_data():
    """
    DOCSTRING
    """
    dataframe_a = pandas.read_csv('google.csv', parse_dates=True, index_col=0)
    dataframe_b = dataframe_a['Adj Close'].resample('10D').ohlc()
    dataframe_b.reset_index(inplace=True)
    dataframe_b['Date'] = dataframe_b['Date'].map(mdates.date2num)
    dataframe_c = dataframe_a['Volume'].resample('10D').sum()
    axis_1 = pyplot.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    axis_1.xaxis_date()
    mplfinance.candlestick_ohlc(axis_1, dataframe_b.values, width=2, colorup='g')
    axis_2 = pyplot.subplot2grid((6, 1), (5, 0), rowspan=5, colspan=1, sharex=axis_1)
    axis_2.fill_between(dataframe_c.index.map(mdates.date2num), dataframe_c.values, 0)
    pyplot.show()

def save_sp500_tickers():
    """
    DOCSTRING
    """
    response = requests.get('https://en.wikipedia.org/wiki/S%26P_500_Index')
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        tickers.append(row.findAll('td')[0].text)
    with open('sp500_tickers.pkl', 'wb') as file:
        pickle.dump(tickers, file)
    return tickers

if __name__ == '__main__':
    save_sp500_tickers()
