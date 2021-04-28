import pandas as pd
import urllib.request,urllib.response,urllib.error
from bs4 import BeautifulSoup

def drawdown(return_series):
    wealth_index=1000*(1+return_series).cumprod()
    previous_peaks=wealth_index.cummax()
    drawdowns=(wealth_index-previous_peaks)/previous_peaks
    return pd.DataFrame({
        "wealth":wealth_index,
        "peaks":previous_peaks,
        "drawdown":drawdowns
    })
def get_ffme_returns():
    me_m = pd.read_csv("C:/Users/SAGAR/Downloads/VweKqLJfEemJ1w4LYV5qDg_2c089d97f24e49daa70b757b8337a76f_data/data/Portfolios_Formed_on_ME_monthly_EW.csv",header=0,index_col=0,parse_dates=True,na_values=-99.99)
    rets = me_m[['Lo 10','Hi 10']]
    rets.columns=['Midcap','Largecap']
    rets = rets/100
    rets.index = pd.to_datetime(rets.index,format="%Y%m").to_period('M')
    return rets

def get_hfi_returns():
    """
    load and format edhec hedge fund index returns
    """
    hfi = pd.read_csv("C:/Users/SAGAR/Downloads/VweKqLJfEemJ1w4LYV5qDg_2c089d97f24e49daa70b757b8337a76f_data/data/edhec-hedgefundindices.csv",header=0,index_col=0,parse_dates=True,na_values=-99.99)
    hfi=hfi/100
    hfi.index = hfi.index.to_period("M")
    return hfi

def semideviation(r):
    """
    Returns the semideviation aka negative semideviation of r
    r must be a Series or a DataFrame
    """
    is_negative = r < 0
    return r[is_negative].std(ddof=0)

def skewness(r):
    """
    Alternative to scipy.stats.skew()
    Computes the skewness of the supplied Series or DataFrame
    Returns a float or a Series
    """
    demeaned_r = r - r.mean()
    # use the population standard deviation, so set dof=0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3


def kurtosis(r):
    """
    Alternative to scipy.stats.kurtosis()
    Computes the kurtosis of the supplied Series or DataFrame
    Returns a float or a Series
    """
    demeaned_r = r - r.mean()
    # use the population standard deviation, so set dof=0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4

def stock_data(stock):
    url = 'https://ticker.finology.in/company/'+stock
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    return(soup)

def balance_sheet(stock):
    return(pd.read_html("https://www.screener.in/company/"+stock+"/consolidated/"))

def drop_divnstksplit(stocks):
    cols=['Dividends', 'Stock Splits'] 
    for i in range(len(stocks)):
        stocks[i].drop(cols,axis=1,inplace=True)
    return(stocks)
    