"""
DOCSTRING
"""
import bs4
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as pyplot
import matplotlib.style as style
import mplfinance.original_flavor as mplfinance
import numpy
import os
import pandas
import pandas_datareader.data as web
import pickle
import requests

style.use('ggplot')

def consolidate_data():
    """
    DOCSTRING
    """
    with open('sp500_tickers.pkl', 'rb') as file:
        tickers = pickle.load(file)
    dataframe_a = pandas.DataFrame()
    tickers = tickers[:10]
    for count, ticker in enumerate(tickers):
        ticker = ticker.strip()
        dataframe_b = pandas.read_csv(os.path.join('stock_dataframes', ticker + '.csv'))
        dataframe_b.set_index('Date', inplace=True)
        dataframe_b.rename(columns={'Adj Close': ticker}, inplace=True)
        dataframe_b.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
        if dataframe_a.empty:
            dataframe_a = dataframe_b
        else:
            dataframe_a = dataframe_a.join(dataframe_b, how='outer')
        print(count)
    dataframe_a.to_csv('sp500_closes.csv')

def get_data():
    """
    DOCSTRING
    """
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime(2016, 12, 31)
    dataframe_a = web.DataReader('GOOGL', 'yahoo', start, end)
    dataframe_a.to_csv('google.csv')

def get_data_from_yahoo(reload_sp500=False):
    """
    DOCSTRING
    """
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('sp500_tickers.pkl', 'rb') as file_a:
            tickers = pickle.load(file_a)
    if not os.path.exists('stock_dataframes'):
        os.makedirs('stock_dataframes')
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime(2016, 12, 31)
    for ticker in tickers[:10]:
        ticker = ticker.strip()
        print(ticker)
        if not os.path.exists('stock_dataframes/{}.csv'.format(ticker)):
            dataframe_a = web.DataReader(ticker, 'yahoo', start, end)
            dataframe_a.to_csv(os.path.join('stock_dataframes', ticker + '.csv'))
        else:
            print('{} already exists'.format(ticker))

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
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        tickers.append(row.findAll('td')[0].text)
    with open('sp500_tickers.pkl', 'wb') as file_a:
        pickle.dump(tickers, file_a)
    return tickers

def visualize_data():
    """
    DOCSTRING
    """
    dataframe_a = pandas.read_csv('sp500_closes.csv')
    dataframe_b = dataframe_a.corr()
    data = dataframe_b.values
    figure = pyplot.figure()
    axis_1 = figure.add_subplot(1, 1, 1)
    heatmap = axis_1.pcolor(data, cmap=pyplot.cm.get_cmap('RdYlGn'))
    figure.colorbar(heatmap)
    axis_1.set_xticks(numpy.arange(data.shape[0])+0.5, minor=False)
    axis_1.set_yticks(numpy.arange(data.shape[1])+0.5, minor=False)
    axis_1.invert_yaxis()
    axis_1.xaxis.tick_top()
    column_labels = dataframe_b.columns
    row_labels = dataframe_b.index
    axis_1.set_xticklabels(column_labels)
    axis_1.set_yticklabels(row_labels)
    heatmap.set_clim(-1, 1)
    pyplot.xticks(rotation=90)
    pyplot.tight_layout()
    pyplot.show()

if __name__ == '__main__':
    visualize_data()
