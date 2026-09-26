import pandas as pd
import numpy as np

import metrics
import allocations



def make_excess_returns(returns, risk_free_returns):
    rf = risk_free_returns.reindex(returns.index).ffill()
    excess_returns = returns.sub(rf, axis=0)
    return excess_returns


def block_bootstrap_indices(n_obs, block_size, rng):
    indices = []

    while len(indices) < n_obs:
        start = rng.integers(0, n_obs - block_size + 1)
        block = range(start, start + block_size)
        indices.extend(block)

    return indices[:n_obs]

def bootstrap_sharpe(excess_returns, block_size, n_bootstrap, seed=42):
    rng = np.random.default_rng(seed)

    bootstrap_results = []

    for i in range (n_bootstrap):
        indices = block_bootstrap_indices(len(excess_returns), block_size, rng)
        sample_bootstrap = excess_returns.iloc[indices]

        sharpe = (sample_bootstrap.mean() / sample_bootstrap.std() * np.sqrt(252))
        bootstrap_results.append(sharpe)

    bootstrap_results = pd.DataFrame(bootstrap_results)

    return bootstrap_results
        
