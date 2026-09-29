# Smart Portfolio — Final Analysis

## 1. Raw performance

We can start with the raw portfolios, where the strategies are compared at their natural risk levels. Higher returns often come with substantially larger drawdowns. For example, Max Geo delivers an annual return of 11.28%, but experiences a maximum drawdown of 39.34%. Tech is even more extreme, with a 16.43% annual return and a drawdown of 49.37%.

This matters because drawdown is not only a statistical risk measure. It also captures how difficult a strategy may be to hold in practice. A portfolio can look attractive over the full sample, but if it loses 40% or 50% at some point, many investors may not be willing or able to stay invested long enough to realize the long-run return.

The Sharpe ratio gives additional information by relating excess return to realized volatility, but it is still estimated from one historical sample. Tech, which consists only of QQQ, has the highest raw Sharpe ratio at 0.728 in our sample. However, it is also a highly concentrated exposure to the technology sector, and that exposure performed particularly well over the observed period. Under a different market path, both its returns and its realized volatility could have been very different, leading to a very different Sharpe ratio. Historical Sharpe therefore reflects the risks that materialized in the sample, not the full range of risks the portfolio was exposed to. The bootstrap analysis in Section 7 quantifies how sensitive these Sharpe estimates are to alternative resampled histories.

There is also a clear contrast between the low-volatility allocation methods and the more equity-focused portfolios. Carver and Hierarchical Inverse Volatility both have raw volatility below 4% and drawdowns close to 10%, but their annual returns are only 3.17% and 3.33%. Tech and SPY deliver much higher returns, but with much larger volatility and drawdowns. This already shows that there is no meaningful ranking from return alone.

## 2. Volatility targeting and leverage

We then apply a 10% volatility target. The raw results mainly compare the allocation rules themselves, while the targeted results compare how those strategies behave when implemented at a similar intended risk level.

Volatility targeting is useful, but it is not perfect. Some naturally low-volatility strategies would need very high leverage to reach a 10% target, which could require borrowing several times the portfolio capital. High leverage also makes the portfolio more sensitive to errors in the volatility estimate: after a calm period, estimated volatility can be too low, causing the strategy to take too much exposure just before risk increases again. For this reason, leverage is capped at 2x, which limits the impact of these estimation errors and keeps exposures more realistic.

This effect is visible for Inverse Vol. Its raw annual volatility is only 4.94%, so reaching a 10% target would often require close to or more than 2x exposure. It therefore spends 73.33% of the backtest at the 2x leverage cap. As a result, its realized volatility after targeting is only 8.43%, below the intended 10% target.

The effect is even stronger for Carver and Hierarchical Inverse Volatility, which spend 88.44% and 87.56% of the time at the 2x cap. Their average leverage is 1.96x and 1.95x respectively. By contrast, naturally high-volatility portfolios require less exposure. Tech uses only 0.59x average leverage and never reaches the cap, while SPY averages 0.74x.

This is important for the interpretation of the targeted results. Volatility targeting does not simply put every portfolio at exactly 10% realized volatility. The realized level depends on the volatility estimate, the monthly rebalancing frequency and the leverage cap. Low-volatility strategies can remain below the target because they are constrained by the cap, while high-volatility strategies are scaled down and hold part of the portfolio in cash.

After volatility targeting, the risk profiles become much more comparable across strategies. In the raw portfolios, maximum drawdowns range from around 10% for the lowest-volatility methods to more than 50% for SPY. After targeting, they are compressed into a much narrower range of roughly 18% to 24%. This is one of the main purposes of volatility targeting: not to mechanically improve Sharpe ratios, but to put strategies with very different natural risk levels on a more comparable absolute-risk basis.

## 3. Risk-free rate, cash and funding

The risk-free rate is based on the FRED DGS3MO 3-Month U.S. Treasury series. The annual rate is converted to a daily return and aligned with the ETF trading dates. It plays two different roles in the project. First, Sharpe ratios are calculated from excess returns, so the relevant return is the portfolio return minus the risk-free return. Second, the risk-free rate is used directly inside the backtest when volatility targeting changes total exposure.

When leverage is below 1x, the uninvested part of the portfolio remains in cash and earns the daily risk-free rate. When leverage is above 1x, the portfolio has to borrow. In the base case, borrowed capital costs the risk-free rate plus a 1% annual funding spread.
This matters mainly for the low-volatility strategies. Carver and Hierarchical Inverse Volatility spend most of the sample close to 2x leverage, so their targeted performance is exposed to funding costs almost continuously. Tech is the opposite case: with average leverage of only 0.59x, it generally holds cash rather than borrowing.

The leverage-cap robustness test makes this visible. Carver's Sharpe falls from 0.521 with a 1x cap to 0.427 with a 1.5x cap and 0.362 with a 2x cap. Hierarchical Inverse Volatility moves similarly, from 0.522 to 0.437 and then 0.370. Inverse Vol falls from 0.502 at 1x to 0.372 at 2x. By contrast, Tech is almost unchanged, with Sharpe ratios of 0.751, 0.764 and 0.765 across the three caps because it does not need leverage to reach the target.

For Carver, the decline can be largely explained by funding costs. With average leverage close to 1.96x, the strategy borrows about 0.96 times its capital on average. At a 1% funding spread, this represents a cost of about 0.96% per year, which corresponds to about 0.15 Sharpe points relative to its 6.45% realized volatility. This is very close to the observed decline from the 1x to the 2x cap, suggesting that funding costs explain a large part of the deterioration.

The conclusion is not that leverage is always bad. The point is that once a low-volatility strategy is scaled up, its performance is no longer determined only by the allocation rule. It also depends on the leverage constraint and the assumed cost of financing.

## 4. Turnover and transaction costs

Implementation costs also differ substantially across strategies. Transaction costs are directly linked to turnover: the more a portfolio changes its exposures at each rebalance, the more trading it requires.

The optimization-based strategies generate the most raw turnover. Max Sharpe has an average turnover of 11.70%, compared with 8.25% for Max Geo, 0.94% for Inverse Vol and only 0.72% for Carver. Max Sharpe also reaches a maximum one-period turnover of 85.40%, showing that some rebalances involve very large changes in the portfolio.

The difference is not simply that the inputs are re-estimated each month, because Inverse Vol and Carver also update risk estimates. The important difference is that the optimization-based methods depend much more on estimated expected returns and covariance inputs. Expected returns are noisy, and an optimizer can transform relatively small changes in these estimates into large changes in optimal weights. Simpler allocation methods rely more heavily on risk estimates and therefore tend to move more gradually.

Volatility targeting adds another source of turnover because total exposure itself changes when estimated volatility changes. Max Sharpe's average turnover rises from 11.70% to 17.59% after volatility targeting. Equal Weight rises from 1.36% to 6.53%, even though its underlying allocation rule is simple.

Tech is the clearest example of this effect. In raw form it has 0% turnover because it simply holds QQQ. After volatility targeting, average turnover rises to 4.25%. The underlying asset has not changed; all of this trading comes from changing total exposure as the volatility estimate moves over time.

The transaction-cost results reflect these differences. With the 10 bps base-case assumption, Max Sharpe accumulates 5.27% of transaction-cost deductions over the full raw backtest and 7.92% after volatility targeting. Max Geo accumulates 3.71% raw and 4.85% targeted. Carver is much cheaper to trade, at 0.33% raw and 1.20% targeted.

The 10 bps transaction-cost assumption should be viewed as a simple base-case estimate rather than a universal trading cost. Actual costs can vary significantly depending on the investor, the assets traded, liquidity, trade size, bid-ask spreads, broker fees and market impact. A large institutional investor and a private investor trading the same portfolio may therefore face very different effective costs. For this reason, the transaction-cost results are best interpreted as an illustration of how higher turnover leads to higher trading costs, rather than as a precise estimate of what every investor would actually pay. The reported Total Cost is cumulative over the full backtest and is not an annualized percentage.

## 5. Volatility-estimation horizon

One of the most important robustness results is that volatility targeting depends strongly on how volatility is estimated. The base case uses a 60-trading-day volatility window, but the robustness analysis also tests 20, 126, 252 and 756 trading days.

For high-volatility portfolios, a faster estimator performs much better in this sample. Tech's targeted Sharpe is 0.842 with a 20-day volatility window, 0.765 with the 60-day base case, 0.705 with a 252-day window and 0.683 with a 756-day window. SPY follows the same pattern, moving from 0.629 at 20 days to 0.619 at 60 days and 0.507 at 756 days.

Max Geo also falls from a Sharpe of 0.759 with the 20-day estimator to 0.650 with the 756-day estimator. The reason is simple: a longer volatility window reacts more slowly when market volatility changes, so the portfolio can keep an exposure that is no longer well adapted to current conditions.

This does not mean that the shortest possible estimator is always better. Very short windows can themselves be noisy, and the result depends on the exact historical return distribution. The important point is that the volatility estimator is part of the strategy. Volatility targeting should not be treated as a neutral scaling operation.

Compared with the raw portfolios, this also means that volatility targeting can either improve or reduce risk-adjusted performance depending on how volatility is estimated. SPY's raw Sharpe of 0.574 rises to 0.619 with the 60-day estimator, but falls to 0.507 with the 756-day estimator.

By contrast, changing the volatility target itself should, in theory, have only a limited effect on the Sharpe ratio. If exposure is scaled proportionally, excess return and volatility increase by a similar factor, so Sharpe remains approximately unchanged. This is what we observe for Tech and SPY. Tech has Sharpe ratios of 0.763, 0.765 and 0.758 at 5%, 10% and 15% targets, while SPY has 0.620, 0.619 and 0.611.

For low-volatility strategies, Sharpe changes more because reaching the target requires borrowing and therefore paying funding costs, as discussed in Section 3.
At a lower target, less leverage is needed and less funding spread is paid. For example, Carver's Sharpe is 0.410 at a 5% target but falls to 0.362 at 10%. At 10% and 15%, Carver is already constrained by the 2x leverage cap in both cases, so its Sharpe remains almost unchanged at 0.362 and 0.374.

## 6. Robustness of the allocation methods

The allocation-window tests show that the optimization-based methods are much more sensitive to the amount of historical data used. To make the comparison fair, the code explicitly aligns all window lengths to the exact same out-of-sample period before computing the performance metrics.

Max Geo and Max Sharpe both change by about 0.18 Sharpe points across the tested windows, while Inverse Vol changes by about 0.04 and Carver by about 0.03. This suggests that the optimization-based methods are more sensitive to changes in the estimated inputs.

The key difference is what is being estimated. Max Geo and Max Sharpe rely more heavily on expected returns, while Inverse Vol and Carver rely mainly on volatility estimates. Expected returns are difficult to estimate because the long-run average return is a small signal compared with large day-to-day market fluctuations. Even with daily data, three years still provide only a short historical period to estimate this long-term mean. Volatility is different: every daily price movement provides direct information about how much returns fluctuate, so it can be estimated more precisely from the same sample. This helps explain why the optimization-based methods are more sensitive to the estimation window.

The rebalancing-frequency test shows a similar, but weaker, pattern. Max Sharpe changes by about 0.07 Sharpe points across the tested frequencies, compared with only about 0.005 for Carver. This suggests that Max Sharpe is also more sensitive to how frequently the portfolio is updated.

Overall, the results suggest that estimation choices are an important source of uncertainty for the optimized strategies, while the simpler allocation methods are more stable across reasonable parameter choices.

## 7. Statistical uncertainty

The robustness tests show how results change when modeling assumptions are modified, but there is another source of uncertainty: the historical sample itself. A Sharpe ratio calculated from one backtest is only an estimate based on one realized market history.

To measure this uncertainty, the project uses a block bootstrap with 21-trading-day blocks and 10,000 bootstrap samples. Instead of resampling individual days independently, entire blocks of consecutive returns are resampled. This preserves some of the short-term dependence present in market returns.

The resulting Sharpe confidence intervals are wide. For example, Equal Weight has a raw 95% interval of [0.068, 0.903], while Tech ranges from 0.327 to 1.185. In the targeted portfolios, Max Geo ranges from 0.295 to 1.171 and Max Sharpe from 0.224 to 1.086.

These wide intervals are not simply a weakness of the bootstrap. They reflect the difficulty of estimating Sharpe ratios from a limited historical period. As discussed in Section 6, the long-term average return is difficult to estimate precisely. Since the Sharpe ratio depends directly on average excess return, uncertainty in the mean return translates into uncertainty in the Sharpe ratio.

The pairwise comparisons are therefore particularly useful. Instead of comparing two individual Sharpe confidence intervals, the bootstrap directly measures the distribution of the difference between two strategies. The same blocks are used for both strategies, so they are exposed to the same resampled market periods. This removes part of the common market noise from the comparison.

A clear example is Carver versus Hierarchical Inverse Volatility. Their raw Sharpe difference has a 95% interval of only [-0.034, 0.035], showing that their historical Sharpe ratios are extremely similar.

Against Equal Weight, most allocation methods cannot be clearly distinguished from zero. In the raw portfolios, the interval for Equal Weight minus Max Geo is [-0.434, 0.071], while for Max Sharpe it is [-0.551, 0.306]. Both include zero, meaning that the historical sample does not provide clear evidence of a Sharpe difference relative to Equal Weight.

After volatility targeting, the comparison changes. Max Geo has an interval of [-0.477, -0.037] relative to Equal Weight, which no longer includes zero, while Max Sharpe still has a wider interval of [-0.551, 0.170]. Volatility targeting changes the return series because exposure, cash holdings, leverage constraints and funding costs change over time, so the pairwise results can also change.

The Max Geo result should still be interpreted with some caution. Section 6 showed that Max Geo is relatively sensitive to the estimation window, so this result depends on the chosen base-case specification and should not be treated as proof that the strategy would always outperform Equal Weight.

The 60/40 portfolio also has an interval below zero relative to Equal Weight, both in the raw and targeted results. However, 60/40 is included mainly as a reference portfolio rather than as one of the allocation methods developed in the project. Max Geo is therefore more relevant when evaluating whether an allocation method improves on Equal Weight.

The bootstrap also has an important limitation. It only resamples return blocks that actually occurred in the historical sample. It therefore measures uncertainty within the observed history, but it cannot capture risks or market events that never appeared in that sample. This is especially important for concentrated portfolios such as Tech, where the observed period may not include all the adverse scenarios that the portfolio could realistically face.

The main conclusion from the bootstrap is therefore not a ranking of strategies. Many of the observed Sharpe differences are small relative to their sampling uncertainty. The backtest shows that some methods produced higher Sharpe ratios in this historical period, but for most allocation methods the evidence is not strong enough to conclude that the difference would persist under another realization of market returns.

## 8. Limitations

The project includes several realistic features, but some limitations remain.

First, the ETF universe is small and fixed. The results therefore depend on the chosen assets and on the historical period available for them. This is especially relevant for concentrated portfolios such as Tech, where a strong historical period for one exposure can produce an attractive Sharpe that may not generalize.

Second, expected returns, covariances and volatility are all estimated from historical data. The robustness tests show that some methods, especially the optimizers, are sensitive to those estimation choices.

Third, transaction costs are simplified. The model uses a constant 10 bps proportional cost assumption. Real trading costs depend on spreads, liquidity, order size, market impact, broker fees and execution conditions. The project also does not include a full transaction-cost sensitivity analysis across several cost assumptions.

Fourth, funding is modeled with a fixed 1% annual spread above the risk-free rate. This is more realistic than assuming borrowing at the risk-free rate, but the actual spread would vary across investors and over time. Because some strategies spend most of the sample close to 2x leverage, their results can depend strongly on this assumption.

Fifth, the 2x leverage cap is itself a modeling choice. The robustness analysis shows that it matters strongly for the low-volatility strategies.

Finally, the robustness analysis focuses mainly on parameter sensitivity and does not include a detailed comparison across different market periods. Studying performance separately during crises, calm markets and rising-rate periods would be a useful extension.

## 9. Conclusion

The project does not identify one allocation method that is consistently superior across all the tests. Although some strategies achieve higher Sharpe ratios in the historical sample, the bootstrap shows that most differences between allocation methods remain small relative to their sampling uncertainty.

The robustness analysis also shows an important difference between methods. Max Geo and Max Sharpe are more sensitive to the estimation window, while simpler methods such as Inverse Vol and Carver remain more stable. This is consistent with the greater difficulty of estimating expected returns compared with volatility.

Volatility targeting makes the overall risk levels more comparable, but its results depend strongly on how it is implemented. Low-volatility strategies require leverage and are therefore affected by funding costs and the leverage cap, while high-volatility portfolios are scaled down. The choice of volatility-estimation window also matters: for example, SPY's Sharpe rises from 0.574 in the raw portfolio to 0.619 with the 60-day estimator, but falls to 0.507 with the 756-day estimator.

Trading costs increase with turnover and are highest for Max Sharpe and Max Geo, but under the 10 bps base-case assumption their effect is smaller than the funding effect observed for highly leveraged low-volatility strategies.

Finally, the bootstrap shows that historical Sharpe rankings should not be interpreted as precise rankings of future performance. Most pairwise differences cannot be clearly separated from sampling uncertainty, and the bootstrap itself can only resample market periods that actually occurred.

Overall, in this sample, implementation choices such as leverage, funding and volatility estimation had large and clearly identifiable effects on performance, while differences between allocation methods were generally more uncertain.