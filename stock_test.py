import unittest
import pandas as pd
import quandl
import stock_data

TIME_STAMP1 = pd.Timestamp('2000-04-06 00:00:00')
TIME_STAMP2 = pd.Timestamp('2000-01-01 00:00:00')

TEST_PROFIT_INPUT = pd.DataFrame.from_dict({
       'date': [TIME_STAMP1, TIME_STAMP2],
       'low': [0,0],
       'high': [1, 1000],
       'ticker': ['SGMO', 'SGMO']
})

TEST_VOLUME_INPUT = pd.DataFrame.from_dict({
       'date': [TIME_STAMP1, TIME_STAMP2],
       'volume': [0,1000],
       'ticker': ['SGMO', 'SGMO']
})

TEST_BAD_DAY_INPUT = pd.DataFrame.from_dict({
       'date': [TIME_STAMP1, TIME_STAMP2],
       'open': [0,100],
       'close': [1, 0],
       'ticker': ['SGMO', 'SGMO']
})

EMPTY_INPUT = pd.DataFrame.from_dict({})

class StockTests(unittest.TestCase):

    def test_get_max_daily_profit(self):
        most_profitable_day = TEST_PROFIT_INPUT.loc[1]
        most_profitable_day['profit'] = 1000
        self.assertDictEqual(most_profitable_day.to_dict(), 
                             stock_data.get_max_daily_profit(TEST_PROFIT_INPUT).to_dict())


    def test_get_max_daily_profit_empty(self):
        self.assertRaises(ValueError, lambda: stock_data.get_max_daily_profit(EMPTY_INPUT))


    def test_get_high_volume_days(self):
        high_volume_day = TEST_VOLUME_INPUT.loc[[1]]
        self.assertDictEqual(high_volume_day.to_dict(), 
                             stock_data.get_high_volume_days(TEST_VOLUME_INPUT).to_dict())


    def test_get_high_volume_days_empty(self):
        self.assertRaises(ValueError, lambda: stock_data.get_high_volume_days(EMPTY_INPUT))


    def test_get_bad_days(self):
        self.assertEqual(1, stock_data.get_bad_days(TEST_BAD_DAY_INPUT))

    
    def test_get_bad_days_empty(self):
        self.assertRaises(ValueError, lambda: stock_data.get_bad_days(EMPTY_INPUT))


    def test_get_stock_data(self):
        return None

if __name__ == '__main__':
    unittest.main()
