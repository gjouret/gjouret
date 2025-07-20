import axios from 'axios';

const API_KEY = 'N1HXV2WWQU8MJHEB';
const BASE_URL = 'https://www.alphavantage.co/query';

export const fetchStockData = async (symbol) => {
  const response = await axios.get(BASE_URL, {
    params: {
      function: 'TIME_SERIES_DAILY_ADJUSTED',
      symbol: symbol,
      outputsize: 'full',
      apikey: API_KEY,
    },
  });
  return response.data['Time Series (Daily)'];
};

export const fetchCurrencyData = async (from_currency, to_currency) => {
  const response = await axios.get(BASE_URL, {
    params: {
      function: 'FX_DAILY',
      from_symbol: from_currency,
      to_symbol: to_currency,
      outputsize: 'full',
      apikey: API_KEY,
    },
  });
  return response.data['Time Series FX (Daily)'];
};
