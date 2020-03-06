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

if __name__ == '__main__':
    graph_data()
