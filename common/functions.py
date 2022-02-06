import numpy as np
import pandas as pd
import statsmodels.api as sm
import asyncio, time


def portstats_bm(v, bm, nper=12, logret=False):
    """Arguments:
    v: pd.DataFrame containing rows of returns OR
    bm: pd.DataFrame containing rows of returns
    nper: int for annualization
    """
    try:
        c = v.columns
    except AttributeError:
        c = ["Portfolio"]
    
    mu = v.mean() * nper
    sig = v.std() * np.sqrt(nper)
    
    alpha, rsq, mae, tr, ir, reg = [], [], [], [], [], []
    beta = {}
    for col in bm.columns:
        beta[col] = []
    
    for name, col in v.iteritems():
        res = sm.OLS(col, sm.add_constant(bm.values), missing="drop").fit()
        
        alpha.append(res.params[0] * nper)
        rsq.append(res.rsquared)
        mae.append(abs(res.params[0] * nper))
        for i, col in enumerate(bm.columns):
            beta[col].append(res.params[i+1])
        tr.append(mu[name] / res.params[1])
        ir.append(res.params[0] / res.resid.std() * np.sqrt(nper))
        reg.append(res)
    
    alpha = pd.Series(alpha, index=c)
    beta = pd.DataFrame(beta, index=c).T
    beta.index = ["beta_"+i for i in beta.index]
    mae = pd.Series(mae, index=c)
    tr = pd.Series(tr, index=c)
    ir = pd.Series(ir, index=c)
    
    if logret:
        cumu = np.exp(v.cumsum())
    else:
        cumu = (v+1).cumprod()
    from_peak = (cumu - cumu.cummax()) / cumu.cummax()

    pl, rl, dl = [], [], []
    trough = from_peak.idxmin()
    for col, date in trough.iteritems():
        pk = v.loc[(from_peak.index < date) & (from_peak[col] == 0), col].index
        if len(pk):
            peak = max(pk)
        else:
            peak = max(v.index)
            date = peak
        
        try:
            reco = min(v.loc[(from_peak.index > date) & (from_peak[col] == 0), col].index)
        except ValueError:
            reco = None
        
        if logret:
            # This may not work right at the moment...
            draw = np.log(cumu.loc[date,col] / cumu.loc[peak,col])
        else:
            draw = (cumu.loc[date,col] - cumu.loc[peak,col]) / cumu.loc[peak,col]

        pl.append(peak); rl.append(reco); dl.append(draw)

    dl = pd.Series(dl, index=c)
    pl = pd.Series(pl, index=c)
    rl = pd.Series(rl, index=c)
    
    ret = pd.DataFrame([mu, sig, mu / sig, alpha],
                       index=["mean", "std", "sharpe", "alpha"],
                       columns=c)
    end = pd.DataFrame([rsq, mae, tr, ir, dl], index=["r2", "mae", "treynor", "info ratio", "drawdown"], columns=c)
    dra = pd.DataFrame([pl, trough, rl],
                       index=["peak", "trough", "recovery"],
                       columns=c)
    ret = pd.concat([ret, beta, end, dra]).T
    return ret, reg


# # THIS DOESNT WORK! NEED MULTIPLE REQUEST INSTANCES...
# async def quandl_zacks(db, dates, tickers, keys):
#     """Asynchronously Pulls Zacks Data
#     db: str of the format ZACKS/xx
#     dates: list<str> for period_end_date
#     tickers: list"""
    
#     async def pull_date(db, date, tickers, key):
# #         print(f"Concurrently sleeping {key}")
# #         await asyncio.sleep(3)
# #         print(f"Done sleeping {key}")
#         try:
#             print(f"Pulling {date}.")
#             # quandl.get_table still pulls the stuff sequentially somehow...
#             ret = quandl.get_table(db, per_end_date=date, ticker=tickers,
#                                    paginate=True, api_key=key)
#             return ret
#         except Exception as e:
#             print(e, "\nError with", date)
    
#     n = len(keys)
#     tasks = [asyncio.ensure_future(pull_date(db, d, tickers, keys[i%n]))
#              for i, d in enumerate(dates)]
#     a = await asyncio.gather(*tasks)
        
#     return pd.concat(a, axis=0).sort_values(["per_end_date", "ticker"])

# start = time.time()

# raw = await quandl_zacks("ZACKS/FC", dates=PER_END_DATES, tickers=list(un), keys=QUANDL_API_KEYS)

# el = time.time()-start
# print(f"{n} Dates Elapsed: {el:.3f}. Per Date {el/n:.3f}")