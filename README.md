# Regression Analysis and Quantitative Trading Strategies (FINM 33150)

Instructor: Brian Boonstra

University of Chicago

Philip Lee | Winter 2022

# Summary

1. Commodity Spread Characterization
* Contracts analyzed: 2 vs 5-year Treasuries; Brent vs Gasoil.
* Construct continuous futures using second-month quarterly contracts.
* Analyze spread characteristics using moving averages, autocorrelation, and quantiles.
2. ETF Spreads
* ETFs analyzed: FCOM vs VOX (Communication Services)
* Visualize lagged return spread characteristics.
* Construct an algorithm that trades daily closes.
* Manipulate parameters including lookback window, entry/exit parameters, and stop-loss to understand how they change the algorithm's behavior.
* Gridsearch to tune parameters to find optimal profitability without overfitting.
* Analyze strategy performance by computing key ratios (drawdown, Sharpe, Info, Treynor) and conduct factor risk decomposition.
3. Quantamental Ratios
* AKA investigating the Fama-French ratios that were never published
* Narrow tradable universe of equities to fulfull certain fundamental, industry, and trading history requirements.
* Create factors using Earnings Yield, Debt/Market Cap, and Return on Investment.
* Build trading engine that places weekly trades dampened by EWMA.
* Assess performance of dynamic sizing and quantile ranking based on weekly factor changes.
4. Cryptocurrency Flow
* Use information within a lookback window to predict returns in a lookforward window.
* Analyze how aggressive trades impact microstructure characteristics and cause price movements.
* Flow and imbalance are used to predict return (simple and VWAP).
