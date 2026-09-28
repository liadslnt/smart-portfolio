import pandas as pd
import numpy as np
import cvxpy as cp


def equal_weights(returns):
    frac = 1 / returns.shape[1]
    weights = pd.Series(frac, index=returns.columns)
    return weights


def max_geo_mean(arit_mean, cov, max_weight):
    index = arit_mean.index

    arit_mean = np.asarray(arit_mean)
    cov = np.asarray(cov)

    n = arit_mean.size
    w = cp.Variable(n)

    rendement = arit_mean @ w
    variance = cp.quad_form(w, cov)

    objective = cp.Maximize(rendement - 0.5 * variance)
    constraints = [cp.sum(w) == 1, w >= 0, w <= max_weight]

    cp.Problem(objective, constraints).solve()

    weights = w.value
    weights[np.abs(weights) < 1e-10] = 0

    return pd.Series(weights, index=index)


def max_sharpe_ratio(arit_mean, cov, max_weight=None, risk_free_rate=0.0):
    index = arit_mean.index

    arit_mean = np.asarray(arit_mean)
    cov = np.asarray(cov)

    excess = arit_mean - risk_free_rate
    n = arit_mean.size
    y = cp.Variable(n)

    variance = cp.quad_form(y, cov)
    objective = cp.Minimize(variance)
    constraints = [excess @ y == 1, y >= 0]

    problem = cp.Problem(objective, constraints)
    problem.solve()

    weights = y.value / y.value.sum()
    weights[np.abs(weights) < 1e-10] = 0

    return pd.Series(weights, index=index)


def risk_weighing(vols):
    vols_inv = 1 / vols
    weights = vols_inv / vols_inv.sum()
    return weights


def inv_vol_handcrafting(vols, cov, groups):
    intra = {}
    cluster_vols = {}

    for cluster_name, assets in groups.items():
        intra[cluster_name] = risk_weighing(vols[assets])

        cluster_cov = cov.loc[assets, assets]
        w = intra[cluster_name].values

        cluster_vols[cluster_name] = np.sqrt(
            w @ cluster_cov.values @ w
        )

    cluster_vols_series = pd.Series(cluster_vols)

    # Inverse-volatility weighting across clusters
    inter = risk_weighing(cluster_vols_series)

    final = {}

    for cluster_name, assets in groups.items():
        for asset in assets:
            final[asset] = intra[cluster_name][asset] * inter[cluster_name]

    return pd.Series(final)


def carver_handcrafting(vols, groups):
    n_clusters = len(groups)
    cluster_risk_weight = 1 / n_clusters

    final_risk_weights = {}

    for cluster_name, assets in groups.items():
        n_assets = len(assets)
        intra_risk_weight = 1 / n_assets

        for asset in assets:
            final_risk_weights[asset] = (
                cluster_risk_weight * intra_risk_weight
            )

    final_risk_weights = pd.Series(final_risk_weights)

    # Convert risk weights into cash weights
    raw_cash_weights = (
        final_risk_weights /
        vols[final_risk_weights.index]
    )

    cash_weights = raw_cash_weights / raw_cash_weights.sum()

    return cash_weights