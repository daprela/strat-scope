import { useEffect, useState } from 'react';
import { connectStatus } from './transport';
import styles from './Foundation.module.css';

export function Foundation() {
  const [status, setStatus] = useState('Checking infrastructure');
  useEffect(() => {
    let disposed = false;
    let close: (() => void) | undefined;
    void connectStatus(() => {
      if (!disposed) setStatus('Infrastructure ready');
    })
      .then((cleanup) => {
        if (disposed) cleanup();
        else close = cleanup;
      })
      .catch(() => {
        if (!disposed) setStatus('Authority unavailable — restart the service to reclaim');
      });
    return () => {
      disposed = true;
      close?.();
    };
  }, []);
  return (
    <main className={styles.entry}>
      <h1>Strat Scope</h1>
      <p role="status">{status}</p>
      <p>Foundation only. Chart workspace, market data and trading features are not implemented.</p>
      <p>
        <a href="/licenses/lightweight-charts-NOTICE">Lightweight Charts notices</a>
        {' · '}
        <a href="https://www.tradingview.com/" rel="noreferrer">
          TradingView
        </a>
      </p>
    </main>
  );
}
