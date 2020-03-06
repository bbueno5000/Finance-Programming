"""
DOCSTRING
"""
import datetime
import matplotlib.pyplot as pyplot
import matplotlib.style as style
import pandas
import pandas_datareader.data as web

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
    dataframe_a['100ma'] = dataframe_a['Adj Close'].rolling(window=100).mean()
    axis_1 = pyplot.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    axis_2 = pyplot.subplot2grid((6, 1), (5, 0), rowspan=5, colspan=1, sharex=axis_1)
    axis_1.plot(dataframe_a.index, dataframe_a['Adj Close'])
    axis_1.plot(dataframe_a.index, dataframe_a['100ma'])
    axis_2.bar(dataframe_a.index, dataframe_a['Volume'])
    pyplot.show()

if __name__ == '__main__':
    manipulate_data()
