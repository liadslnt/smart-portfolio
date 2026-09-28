import numpy as np


def compute_returns(prices):
    returns = prices.pct_change()
    return returns


def annualize_returns(returns):
    prod = (1 + returns).prod()
    nbr_years = returns.shape[0] / 252
    geo_mean = np.power(prod, 1 / nbr_years) - 1
    return geo_mean


def annualize_returns_aritm(returns):
    daily_mean = returns.mean()
    return daily_mean * 252


def annualize_volatility(returns):
    daily_vol = returns.std()
    annualized_vol = daily_vol * np.sqrt(252)
    return annualized_vol


def sharpe_ratio(returns, risk_free_returns=None):
    if risk_free_returns is None:
        excess_returns = returns
    else:
        rf = risk_free_returns.reindex(returns.index).ffill()
        excess_returns = returns - rf

    annual_excess_return = excess_returns.mean() * 252
    annual_vol = excess_returns.std() * np.sqrt(252)

    return annual_excess_return / annual_vol


def cov_matrix(returns):
    cov_matrix = returns.cov() * 252
    return cov_matrix


def corr_matrix(returns):
    corr_matrix = returns.corr()
    return corr_matrix


def drawdown_series(returns):
    wealth = (1 + returns).cumprod()
    curr_max = wealth.cummax()
    drawdown = wealth / curr_max - 1
    return drawdown


def drawdown(returns):
    return drawdown_series(returns).min()