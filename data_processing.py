import requests
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bs4 import BeautifulSoup


def collect_data(stock):
    """Collects the stock data from alphavantage REST API."""

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + stock + '&interval=1min&outputsize=compact&apikey=2SZ9CCP9FW1Z9B2S'
    response = requests.get(url)

    # Error handler in the case where get request does not go through
    if response.status_code != 200:
        print("Couldn't get data")
    else:
        data = response.json()['Time Series (1min)']

    return data


def normalise_data(data):
    """Normalises stock data into pandas dataframe for easier manipulation."""

    # Changes Dictionary into dataframe
    df = pd.DataFrame.from_dict(data, orient='index')

    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S")

    return df


def candlestick_graph(stock):
    """Creates a candlestick graph for a given stock within a one day time period."""

    # Collects the stock dataframe
    data = collect_data(stock)
    df = normalise_data(data)

    # Creation of candlestick graph
    inc = df.close > df.open
    dec = df.open > df.close
    w = 60 * 1000  # number of milliseconds in 1 min
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    p = figure(x_axis_type="datetime", tools=TOOLS, width=1000, title="Candlestick Graph for " + stock.upper(),
               x_axis_label="Time",
               y_axis_label="Stock Price")
    p.grid.grid_line_alpha = 0.3
    p.toolbar.logo = None
    p.background_fill_color = 'beige'
    p.width = 500
    p.segment(df.index, df.high, df.index, df.low, color="black")
    p.vbar(df.index[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.index[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    # Breaks the graph into an HTML Div and script execute to be inserted in website
    script, div = components(p)

    return script, div


def collect_stock_price(stock):
    """Collects the current stock price of a chosen stock."""

    new_url = "https://www.marketwatch.com/investing/stock/" + stock
    response = requests.get(new_url)
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find(class_="intraday__price").find('bg-quote').text

    return price
