import argparse
import json
import quandl
import pandas as pd

import stock_constants

quandl.ApiConfig.api_key = "s-GMZ_xkw6CrkGYUWs1p"


def fetch_stock_data(stock, show_profits, show_volume, show_bad_days):
    """ Fetch and print data about a stock.  """
    print("Data for stock ticker:", stock)
    stock_data = get_stock_data(stock,
                                stock_constants.START_DATE,
                                stock_constants.END_DATE)

    display_basic_stock_data(stock_data)
    if show_profits:
        print(get_max_daily_profit(stock_data))
    if show_volume:
        print(get_high_volume_days(stock_data))
    if show_bad_days:
        print("Number of bad days: {} for the analysis period".format(
                get_bad_days(stock_data)))


def display_basic_stock_data(stock_data):
    """ Print stock data for each month of the analysis period.
    Data displayed:
    (start_date, end_date, average_closing_price, average_opening_price)
    """
    print("Basic Stock Data for each month between Jan and July 2017:")
    year = 2017
    for month in range(1, 7):
        month_data = fetch_monthly_data(stock_data, year, month)
        average_close = float(month_data[['close']].mean())
        average_open = float(month_data[['open']].mean())
        print(json.dumps(
                {stock_constants.START_DATE_KEY: create_first_of_month_timestamp(year, month),
                 stock_constants.END_DATE_KEY: create_first_of_month_timestamp(year, month + 1),
                 stock_constants.AVG_CLOSE_KEY: average_close,
                 stock_constants.AVG_OPEN_KEY: average_open},
                sort_keys=True,
                indent=4))


def fetch_monthly_data(stock_data, year, month):
    """ Filters and returns a single month's data from the complete dataset passed in. """
    pandas_dates = pd.to_datetime(stock_data['date'])
    start_date_prefix = create_first_of_month_timestamp(year, month)
    end_date_prefix = create_first_of_month_timestamp(year, month + 1)
    return stock_data[(pandas_dates < end_date_prefix) & (pandas_dates >= start_date_prefix)]


def create_first_of_month_timestamp(year, month):
    """ Creates a string timestamp of the first day of the month of the form:
    year-month-01

    Where the month is zero padded if it is a single digit month.

    >>> create_first_of_month_timestamp(2014, 1)
    '2014-01-01'
    >>> create_first_of_month_timestamp(1000, 12)
    '1000-12-01'
    """
    zero_prefix = "0" if month < 10 else ""
    return "{}-{}{}-01".format(year, zero_prefix, month)


def get_max_daily_profit(stock_data):
    """ Get the most profitable day of the analysis period. """
    if stock_data.empty:
        raise ValueError("Stock data cannot be empty")
    print("Displaying the most profitable day:")
    stock_data['profit'] = stock_data.apply(lambda row: row['high'] - row['low'], axis=1)
    most_profitable_day = stock_data.loc[stock_data['profit'].idxmax()]
    return most_profitable_day[['date', 'ticker', 'high', 'low', 'profit']]


def get_high_volume_days(stock_data):
    if stock_data.empty:
        raise ValueError("Stock data cannot be empty")
    """ get the rows of the analysis period with a volume 10% above the average volume. """
    print("Displaying days which had volumes exceeding 10% of the average volume for the period:")
    avg_volume = stock_data['volume'].mean()
    high_volume_mark = (1 + stock_constants.HIGH_VOLUME_THRESHOLD) * avg_volume
    high_days = stock_data[stock_data['volume'] > high_volume_mark]
    print("Avg volume: " + str(avg_volume))
    print("High volume days:")
    return high_days[['ticker', 'date', 'volume']]


def get_bad_days(stock_data):
    if (stock_data.empty):
        raise ValueError("Stock data cannot be empty")
    """ Return the number of days in the analysis period which had a closing price lower than the opening price. """
    print("Displaying Number of 'Losing' days")
    bad_days = stock_data[stock_data['close'] < stock_data['open']]
    return bad_days.shape[0]


def get_stock_data(stock, start_date, end_date):
    """ Make a request to quandl to fetch stock data for a single stock for a period of time """
    return quandl.get_table(
        stock_constants.TABLE_NAME,
        ticker=stock,
        date={'gte': stock_constants.START_DATE, 'lte': stock_constants.END_DATE})


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stocks",
                        default='COF,GOOGL,MSFT',
                        help="A comma separated list of ticker symbols to run the analysis on. " +
                        "Default is `COF,GOOGL,MSFT`.")
    parser.add_argument("--max-daily-profit",
                        help="Adds output which specifies the day in the analysis which would have " +
                        "provided the highest gain for each security.",
                        action="store_true")
    parser.add_argument("--busy-day",
                        help="Adds output which specifies the day in the analysis during which volume " +
                        "was 10 percent higher than average for each security.",
                        action="store_true")
    parser.add_argument("--biggest-loser",
                        help="Adds output which specifies the security which had the most days where " +
                        "the closing price was lower than the opening price.",
                        action="store_true")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    for ticker in args.stocks.split(','):
        fetch_stock_data(ticker, args.max_daily_profit, args.busy_day, args.biggest_loser)


if __name__ == "__main__":
    main()
