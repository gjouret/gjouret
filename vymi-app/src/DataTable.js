import React from 'react';

const DataTable = ({ data }) => {
  if (!data) {
    return null;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>VYMI (USD)</th>
          <th>EUR/USD</th>
          <th>VYMI (EUR)</th>
        </tr>
      </thead>
      <tbody>
        {Object.keys(data).map((date) => (
          <tr key={date}>
            <td>{date}</td>
            <td>{data[date].stockPrice}</td>
            <td>{data[date].currencyRate}</td>
            <td>{data[date].stockPriceInEur}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTable;
