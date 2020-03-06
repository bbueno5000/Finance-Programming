"""
DOCSTRING
"""
import datetime
import matplotlib.pyplot as pyplot
import matplotlib.style as style
import pandas
import pandas_datareader.data as web

style.use('ggplot')

def getting_data():
    """
    DOCSTRING
    """
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime(2016, 12, 31)
    dataframe_a = web.DataReader('GOOGL', 'yahoo', start, end)
    print(dataframe_a.head())

if __name__ == '__main__':
    getting_data()
