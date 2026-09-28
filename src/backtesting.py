import pandas as pd
import numpy as np

import metrics
import allocations


# ============================================================
# HELPERS
# ============================================================

def align_risk_free(risk_free_returns, index):
    if risk_free_returns is None:
        return None

    return risk_free_returns.reindex(index).ffill()


# ============================================================
# STRATEGY WRAPPERS
# ============================================================

def equal_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    return allocations.equal_weights(returns)


def risk_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    return allocations.risk_weighing(vols)


def max_geo_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    return allocations.max_geo_mean(arit_mean, cov, max_weight=0.4)


def max_sharpe_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    excess_mean = arit_mean - annual_rf
    return allocations.max_sharpe_ratio(excess_mean, cov)


def inv_handcrafting_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    return allocations.inv_vol_handcrafting(vols, cov, groups)


def carver_handcrafting_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    return allocations.carver_handcrafting(vols, groups)


def spy_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    weights = pd.Series(0.0, index=returns.columns)
    weights["SPY"] = 1.0
    return weights


def sixty_forty_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    weights = pd.Series(0.0, index=returns.columns)
    weights["SPY"] = 0.6
    weights["IEF"] = 0.4
    return weights


def tech_strategy(returns, arit_mean, vols, cov, groups=None, annual_rf=0.0):
    weights = pd.Series(0.0, index=returns.columns)
    weights["QQQ"] = 1.0
    return weights


# ============================================================
# HOLDING PERIOD SIMULATION
# ============================================================

def simulate_holding_period(
    future_ret,
    target_weights,
    risk_free_returns=None,
    funding_spread=0.01
):
    current_weights = target_weights.copy()
    period_returns = []

    rf_returns = align_risk_free(risk_free_returns, future_ret.index)

    # Convert annual funding spread to a daily rate
    daily_funding_spread = (1 + funding_spread) ** (1 / 252) - 1

    for date, asset_returns in future_ret.iterrows():
        rf = 0.0 if rf_returns is None else rf_returns.loc[date]

        # Positive cash earns the risk-free rate; negative cash represents borrowing
        cash_weight = 1.0 - current_weights.sum()

        if cash_weight >= 0:
            cash_return = rf
        else:
            cash_return = (1 + rf) * (1 + daily_funding_spread) - 1

        port_ret = current_weights @ asset_returns + cash_weight * cash_return
        period_returns.append(port_ret)

        risky_values = current_weights * (1 + asset_returns)
        cash_value = cash_weight * (1 + cash_return)

        total_value = risky_values.sum() + cash_value

        # Let risky-asset weights drift during the holding period
        current_weights = risky_values / total_value

    return pd.Series(period_returns, index=future_ret.index), current_weights


# ============================================================
# LEVERAGE
# ============================================================

def compute_leverage(weights, cov, vol_target, max_leverage):
    portfolio_vol = np.sqrt(weights @ cov @ weights)

    leverage = vol_target / portfolio_vol
    leverage = min(leverage, max_leverage)

    return leverage


# ============================================================
# BACKTEST
# ============================================================

def backtest(
    returns,
    window,
    step,
    allocation_func,
    groups=None,
    vol_target=None,
    max_leverage=2.0,
    risk_free_returns=None,
    transaction_cost=0.001,
    funding_spread=0.01
):
    portfolio_returns = []
    weight_history = []
    leverage_history = []
    rebalance_dates = []
    turnover_history = []
    transaction_cost_history = []

    previous_weights = None

    for t in range(window, len(returns), step):
        curr_ret = returns.iloc[t - window:t]

        arit_mean = metrics.annualize_returns_aritm(curr_ret)
        vols = metrics.annualize_volatility(curr_ret)
        cov = metrics.cov_matrix(curr_ret)

        if risk_free_returns is not None:
            curr_rf = risk_free_returns.reindex(curr_ret.index).ffill()
            annual_rf = curr_rf.mean() * 252
        else:
            annual_rf = 0.0

        weights = allocation_func(
            returns=curr_ret,
            arit_mean=arit_mean,
            vols=vols,
            cov=cov,
            groups=groups,
            annual_rf=annual_rf
        )

        if vol_target is not None:
            leverage = compute_leverage(weights, cov, vol_target, max_leverage)
            weights = weights * leverage
        else:
            leverage = 1.0

        leverage_history.append(leverage)
        rebalance_dates.append(returns.index[t])

        # One-way turnover convention
        if previous_weights is None:
            turnover = 0.0
        else:
            turnover = 0.5 * (weights - previous_weights).abs().sum()

        turnover_history.append(turnover)

        # Multiply by 2 to recover total traded notional from one-way turnover
        transaction_cost_amount = turnover * transaction_cost * 2
        transaction_cost_history.append(transaction_cost_amount)

        end = min(t + step, len(returns))
        future_ret = returns.iloc[t:end]

        if risk_free_returns is not None:
            future_rf = align_risk_free(risk_free_returns, future_ret.index)
        else:
            future_rf = None

        period_portfolio_returns, end_weights = simulate_holding_period(
            future_ret,
            weights,
            future_rf,
            funding_spread
        )

        # Deduct transaction cost once at the rebalance
        period_portfolio_returns.iloc[0] = (
            (1 + period_portfolio_returns.iloc[0])
            * (1 - transaction_cost_amount)
            - 1
        )

        portfolio_returns.append(period_portfolio_returns)
        previous_weights = end_weights

        weights.name = returns.index[t]
        weight_history.append(weights)

    portfolio_returns = pd.concat(portfolio_returns)
    weight_history = pd.DataFrame(weight_history)

    leverage_history = pd.Series(
        leverage_history,
        index=rebalance_dates,
        name="leverage"
    )

    turnover_history = pd.Series(
        turnover_history,
        index=rebalance_dates,
        name="turnover"
    )

    transaction_cost_history = pd.Series(
        transaction_cost_history,
        index=rebalance_dates,
        name="transaction_cost"
    )

    return (
        portfolio_returns,
        weight_history,
        leverage_history,
        turnover_history,
        transaction_cost_history
    )