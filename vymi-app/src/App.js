import React, { useState, useEffect } from 'react';
import { fetchStockData, fetchCurrencyData } from './api';
import DataTable from './DataTable';
import Chart from './Chart';
import { irr } from 'financial';

function App() {
  const [processedData, setProcessedData] = useState(null);
  const [irrValue, setIrrValue] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getData = async () => {
      try {
        const stock = await fetchStockData('VYMI');
        const currency = await fetchCurrencyData('EUR', 'USD');

        const processed = {};
        const cashFlows = [];
        const dates = Object.keys(stock).sort();

        for (const date of dates) {
          if (currency[date]) {
            const stockPrice = parseFloat(stock[date]['4. close']);
            const currencyRate = parseFloat(currency[date]['4. close']);
            const stockPriceInEur = stockPrice / currencyRate;
            processed[date] = {
              stockPrice,
              currencyRate,
              stockPriceInEur,
            };
          }
        }

        const values = Object.values(processed).map(d => d.stockPriceInEur);
        const cashFlowsForIrr = [-values[0], ...Array(values.length - 2).fill(0), values[values.length - 1]];
        setIrrValue(irr(cashFlowsForIrr));
        setProcessedData(processed);

      } catch (err) {
        setError(err);
      }
    };
    getData();
  }, []);

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!processedData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <h1>VYMI Price Analysis</h1>
      {irrValue && <h2>IRR: {(irrValue * 100).toFixed(2)}%</h2>}
      <Chart data={processedData} />
      <DataTable data={processedData} />
    </div>
  );
}

export default App;
