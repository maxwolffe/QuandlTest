# Quandl Stock Data CLI Tool 

This tool supports basic operations over stock dataset from Jan 2017 to July 2017. 

```
python stock_data.py -h
usage: stock_data.py [-h] [--stocks STOCKS] [--max-daily-profit] [--busy-day]
                     [--biggest-loser]

optional arguments:
  -h, --help          show this help message and exit
  --stocks STOCKS     A comma separated list of ticker symbols to run the
                      analysis on. Default is `COF,GOOGL,MSFT`.
  --max-daily-profit  Adds output which specifies the day in the analysis
                      which would have provided the highest gain for each
                      security.
  --busy-day          Adds output which specifies the day in the analysis
                      during which volume was 10 percent higher than average
                      for each security.
  --biggest-loser     Adds output which specifies the security which had the
                      most days where the closing price was lower than the
                      opening price.
```

The easiest way to get output is to use the tool with no arguments. It will give you the average open and close price for MSFT, COF, and GOOG for each month in the analysis period in json format. 

```
$ python stock_data.py
python stock_data.py
Data for stock ticker: COF
Basic Stock Data for each month between Jan and July 2017:
{
    "average_close_price": 88.26,
    "average_open_price": 88.2985,
    "end_date": "2017-02-01",
    "start_date": "2017-01-01"
}
{
    "average_close_price": 90.19578947368421,
    "average_open_price": 89.85263157894737,
    "end_date": "2017-03-01",
    "start_date": "2017-02-01"
}
{
    "average_close_price": 88.92521739130437,
    "average_open_price": 89.26782608695652,
    "end_date": "2017-04-01",
    "start_date": "2017-03-01"
}
...
```

You can specify the stock you want analyzed with the `--stock` flag. 

`python stock_data.py --stock SGMO`

You can get further output by adding the optional flags specified in the help text. 

`python stock_data.py --stock SGMO --max-daily-profit`

## Run Tests

You can use nose to run the project's tests:

```
$ path/to/project
$ nosetests
..../Users/mwolffe/Personal/capitalOneChallenge/stock_test.py:35: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
  most_profitable_day['profit'] = 1000
/Users/mwolffe/.local/share/virtualenvs/capitalOneChallenge-chUDtyoW/lib/python3.6/site-packages/pandas/core/series.py:769: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
  self.loc[key] = value
...
----------------------------------------------------------------------
Ran 7 tests in 0.466s

OK
```

Alternatively, you can run the tests manually:

`python stock_test.py`. 

