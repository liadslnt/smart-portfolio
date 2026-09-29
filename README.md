# Smart Portfolio

A quantitative portfolio allocation project comparing several portfolio construction methods through rolling out-of-sample backtests, volatility targeting, implementation costs, robustness tests and bootstrap analysis.

The objective is not only to compare historical performance, but also to understand how estimation choices, leverage, funding costs and statistical uncertainty affect the results.

**[Detailed analysis](analysis.md)** · **[Results summary](notebooks/04_results_summary.ipynb)**

## Key findings

- **Most allocation methods cannot be clearly separated from Equal Weight.** Most pairwise Sharpe differences include zero in their 95% bootstrap intervals; Max Geo is an exception in the base-case volatility-targeted results.
- **Optimization-based methods are more sensitive to estimation choices.** Max Geo and Max Sharpe vary by about 0.18 Sharpe across allocation windows, versus about 0.03 for Carver.
- **Funding costs strongly affect leveraged low-volatility strategies.** Carver's Sharpe falls from 0.521 with a 1x leverage cap to 0.362 at 2x, with funding costs explaining a large part of the decline.
- **The volatility estimator can change the effect of volatility targeting.** SPY's Sharpe rises from 0.574 raw to 0.619 with the 60-day estimator, but falls to 0.507 with the 756-day estimator.

## Strategies

The project compares six allocation methods:

- **Equal Weight** — allocates the same weight to every asset.
- **Inverse Volatility** — gives larger weights to assets with lower estimated volatility.
- **Maximum Geometric Mean** — optimization-based allocation using estimated returns and covariance.
- **Maximum Sharpe** — chooses weights that maximize estimated excess return relative to portfolio volatility.
- **Carver** — a risk-based allocation relying mainly on volatility estimates and diversification across asset groups.
- **Hierarchical Inverse Volatility** — applies inverse-volatility weighting within a hierarchical asset-group structure.

Three simple reference portfolios are also included:

- **SPY** — US equity reference portfolio.
- **60/40** — traditional equity/bond reference portfolio.
- **Tech** — QQQ-only technology exposure.

The asset universe contains nine ETFs:

`SPY`, `QQQ`, `EWU`, `EZU`, `EEM`, `IEF`, `SHY`, `GLD`, `VNQ`

covering US and international equities, bonds, gold and real estate.

## Data

ETF prices are downloaded from Yahoo Finance and stored in:

`data/etf_prices_raw.csv`

The risk-free rate is based on the FRED `DGS3MO` series, corresponding to the 3-Month U.S. Treasury rate, and is stored in:

`data/risk_free_rate.csv`

The annual risk-free rate is converted to a daily return using 252 trading days and aligned with ETF trading dates.

The common dataset starts in January 2005, after all selected ETFs had become available.

## Methodology

The strategies are evaluated using a rolling out-of-sample backtest.

Base-case parameters:

| Parameter | Value |
|---|---:|
| Allocation estimation window | 3 years |
| Volatility estimation window | 60 trading days |
| Rebalancing frequency | 21 trading days |
| Volatility target | 10% |
| Maximum leverage | 2x |
| Transaction cost | 10 bps |
| Annual funding spread | 1% |

Sharpe ratios are calculated using excess returns.

When volatility targeting produces exposure below 1x, the remaining capital is held in cash and earns the risk-free rate. When exposure exceeds 1x, the portfolio borrows at the risk-free rate plus the funding spread.

The backtest also accounts for portfolio drift, turnover and proportional transaction costs.

## Main results

The raw portfolios show a clear trade-off between return and risk. Tech produces the highest annual return at **16.43%**, but also experiences a maximum drawdown close to **50%**. Max Geo returns **11.28%** with a **39.34%** maximum drawdown, while lower-volatility methods such as Carver and Hierarchical Inverse Volatility remain below 4% annual volatility but generate lower absolute returns.

Volatility targeting makes absolute risk levels more comparable. Maximum drawdowns, which range from roughly 10% to more than 50% in the raw portfolios, are compressed to approximately **18%–24%** after targeting. However, some low-volatility strategies require substantial leverage: Carver and Hierarchical Inverse Volatility spend around **88%** of the sample at the 2x leverage cap.

Implementation assumptions have an important effect. Carver's Sharpe falls from **0.521** with a 1x leverage cap to **0.362** at 2x, largely because of funding costs. The volatility estimator also matters: SPY's targeted Sharpe is **0.629** with a 20-day estimator, **0.619** with the 60-day base case and **0.507** with a 756-day estimator.

The robustness tests show that Max Geo and Max Sharpe are more sensitive to the allocation estimation window, with Sharpe changes of around **0.18**, compared with approximately **0.03–0.04** for Carver and Inverse Volatility.

Finally, a block bootstrap with **10,000 samples** and **21-trading-day blocks** is used to quantify statistical uncertainty. Most Sharpe differences between allocation methods cannot be clearly separated from zero. After volatility targeting, Max Geo is one of the few allocation methods whose 95% interval relative to Equal Weight excludes zero, although this result should be interpreted cautiously because Max Geo is also relatively sensitive to the estimation window.

Overall, implementation choices such as leverage, funding and volatility estimation have large and clearly identifiable effects, while differences between allocation methods are generally more uncertain.

For the full interpretation of these results, see **[analysis.md](analysis.md)**.

## Robustness and statistical analysis

The project tests sensitivity to:

- allocation windows: 2, 3 and 5 years
- rebalancing frequencies: weekly, monthly and quarterly
- volatility targets: 5%, 10% and 15%
- leverage caps: 1x, 1.5x and 2x
- volatility estimation windows: 20, 60, 126, 252 and 756 trading days

For allocation-window comparisons, all strategies are aligned to the same out-of-sample period before performance metrics are calculated.

Statistical uncertainty is evaluated using a block bootstrap applied to aligned excess returns. The same sampled blocks are used when comparing two strategies, preserving the paired nature of the comparison.

## Repository structure

```text
smart-portfolio/
│
├── README.md
├── analysis.md
├── requirements.txt
│
├── data/
│   ├── etf_prices_raw.csv
│   └── risk_free_rate.csv
│
├── notebooks/
│   ├── 01_backtesting.ipynb
│   ├── 02_bootstrap.ipynb
│   ├── 03_robustness.ipynb
│   └── 04_results_summary.ipynb
│
├── src/
│   ├── allocations.py
│   ├── backtesting.py
│   ├── bootstrap.py
│   └── metrics.py
│
└── results/
```

## Notebooks

### [`01_backtesting.ipynb`](notebooks/01_backtesting.ipynb)

Runs the rolling out-of-sample backtests and compares raw and volatility-targeted portfolios. It also analyzes leverage, turnover, transaction costs and portfolio risk.

### [`02_bootstrap.ipynb`](notebooks/02_bootstrap.ipynb)

Measures statistical uncertainty in Sharpe ratios using a block bootstrap and performs paired comparisons between strategies.

### [`03_robustness.ipynb`](notebooks/03_robustness.ipynb)

Tests sensitivity to allocation windows, rebalancing frequency, volatility targets, leverage caps and volatility-estimation horizons.

### [`04_results_summary.ipynb`](notebooks/04_results_summary.ipynb)

Presents the main tables, figures and final results of the project in a compact form.

## How to reproduce

The notebooks are committed with their outputs, so the main results and figures can be viewed directly on GitHub without rerunning the analysis.

To reproduce the project locally:

```bash
pip install -r requirements.txt
jupyter lab
```

Then run the notebooks in the following order:

1. `notebooks/01_backtesting.ipynb`
2. `notebooks/02_bootstrap.ipynb`
3. `notebooks/03_robustness.ipynb`
4. `notebooks/04_results_summary.ipynb`

The required ETF price data and risk-free rate data are already included in the `data/` directory.

The first three notebooks generate the outputs used by `04_results_summary.ipynb`.

## Limitations

The ETF universe is small and fixed, and all parameter estimates are based on historical data. Transaction costs use a constant 10 bps assumption, funding uses a fixed 1% annual spread above the risk-free rate, and the 2x leverage cap is a modeling choice.

The bootstrap only resamples periods that occurred in the historical sample, so it cannot capture market events that never appeared in the data.

For a detailed discussion of the methodology, results and limitations, see **[analysis.md](analysis.md)**.
