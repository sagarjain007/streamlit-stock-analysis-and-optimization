#note use .interactive() in altair charts after .encode().interactive() to make it zoomable

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import risk_kit as rk
from bs4 import BeautifulSoup
import plotly.graph_objects as go #remove this
import altair as alt
from datetime import date
import streamlit.components.v1 as components
from scipy import stats


#https://docs.streamlit.io/en/stable/api.html#streamlit.set_page_config
st.set_page_config(page_title='Stock Analysis', page_icon=None, layout='wide', initial_sidebar_state='collapsed')
#NOTE - if u remove layout='wide' it will make the app centered and awesome

#Ticker Tape Widget
components.html('''
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com" rel="noopener" target="_blank"><span class="blue-text">Ticker Tape</span></a> by TradingView</div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {
      "proName": "FOREXCOM:SPXUSD",
      "title": "S&P 500"
    },
    {
      "proName": "FOREXCOM:NSXUSD",
      "title": "Nasdaq 100"
    },
    {
      "description": "INR/USD",
      "proName": "FX_IDC:INRUSD"
    },
    {
      "proName": "BITSTAMP:BTCUSD",
      "title": "BTC/USD"
    },
    {
      "proName": "BITSTAMP:ETHUSD",
      "title": "ETH/USD"
    },
    {
      "description": "GOLD",
      "proName": "TVC:GOLD"
    },
    {
      "description": "SENSEX",
      "proName": "BSE:SENSEX"
    },
    {
      "description": "",
      "proName": "TVC:USOIL"
    }
  ],
  "showSymbolLogo": true,
  "colorTheme": "light",
  "isTransparent": false,
  "displayMode": "adaptive",
  "locale": "en"
}
  </script>
</div>
<!-- TradingView Widget END -->
''')

"""
# Stock Analysis & Portfolio Optimization📊
*****
Welcome, to Stock Analysis and Portfolio Optimization using Python 🐍.
This is a fundamental analysis application for Indian stocks listed on NSE/BSE. 
International Stocks are not suppoted as of now. For more information on inputs click the ❔ symbol to get information related those inputs. Go ahead & start analyzing now!
""" 
st.text("")
st.text("")

#functions
@st.cache
def stock_data(stock):
    url = 'https://ticker.finology.in/company/'+stock
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    return(soup)
@st.cache
def balance_sheet(stock):
    return(pd.read_html("https://www.screener.in/company/"+stock+"/consolidated/"))
@st.cache
def get_ticker_info(stock):
    return stock.info


#STOCK ANALYSIS
def stock_analysis():
  st.header("Enter the stock name")
  user_input = st.text_input("",help="Enter the ticker symbol of any stock on BSE/NSE. Ex - TCS")


  if(user_input):
      stock_name = user_input.upper()
      try:
          soup = rk.stock_data(stock_name)
          stock = yf.Ticker(stock_name+".NS")
      except:
          st.error("❗ Check your connection / Enter a valid name")
          st.stop()
      cmp = soup.find("span", class_="Number")
      #st.write("Current Market Price - ₹",cmp.text,sep='.')

      
      stock_info = get_ticker_info(stock)

      st.text("")

      #Company_description
      html1 = '''
          <html>
          <head>
          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
          <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
          <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
          <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
          @media screen and (min-width: 601px){
              h1{
                  font-size: 30px;
              }
          }
          .jumbotron{
              background-color:#F0F2F6;
              margin-top: 50px;
          }
          img{
              position: absolute;
              z-index: 2;
              right: 20px;
              border: 5px solid grey;
              border-width: thin;
              top: -110px;
              box-shadow: 1px 1px 3px 0.5px;
          }
          .container{
            paddin
          }
          </style>
          </head>        
          <body>
          <main role="main">
          <!-- Main jumbotron for a primary marketing message or call to action -->
          <div class="jumbotron">

      <div style="position: relative; z-index: 1;">
      <img src=%s style="position: absolute; z-index: 2;" />

      </div>
              <div class="container">
              <h1 class="display-3">%s</h1>
              <p style="font-weight: 500;margin-bottom: 32px;">Industry >> %s</p>
              <p><h5><span style="color: white;" class="sc-hover badge bg-dark" data-cardsize="small" data-quantity="2" data-ordertype="BUY">%s</span></h5>%s</p><br>
              <p><a class="btn btn-primary btn-lg" href=%s role="button" target="_blank">Learn more &raquo;</a></p>
              </div>
          </div>
          </main>
          <script async src="https://www.gateway-tt.in/assets/embed.js"></script>
          </body>
      </html>
      ''' %(stock_info['logo_url'],stock_info['longName'],stock_info['industry'],stock_name,stock_info['longBusinessSummary'],stock_info['website'])
      components.html(html1,height=720)
      
      #Financial info
      c1,c2,c3 = st.beta_columns(3)

      with c1:
          '''
          ### Market Cap: ₹**%d Cr.**
          ### EPS: ₹**%.2f**
          ### Book Value: ₹**%.2f **
          ### Stock PE: ** %.2f **
          ### Beta: ** %.2f **
          ''' %(stock_info['marketCap']//10000000,stock_info['trailingEps'],stock_info['bookValue']*70,stock_info['trailingPE'],stock_info['beta'])


      with c2:
          '''
          ### Earnings Growth(QoQ):** %.2f%% ** 
          ### Forward PE:** %.2f **
          ### Forward EPS: ₹**%.2f**
          ### Sector:** %s **
          ### 50 DMA: ₹**%.2f **
          ''' %(stock_info['earningsQuarterlyGrowth']*100,stock_info['forwardPE'],stock_info['forwardEps'],stock_info['sector'],stock_info['fiftyDayAverage'])


      with c3:
          '''
          ### 52 Week High / Low: ₹**%.2f / %.2f **
          ### Promoter Holding:** %.2f%% **
          ### Dividend Yield:** %.2f%% **
          ### 200 DMA: ₹**%.2f **
          ### CMP: ₹**%s ** 
          
          ''' %(stock_info['fiftyTwoWeekHigh'],stock_info['fiftyTwoWeekLow'],stock_info['heldPercentInsiders']*100,stock_info['dividendYield']*100,stock_info['twoHundredDayAverage'],cmp.text)

      ''' ***** '''
      st.text("")

      # strength & limitations
      col1, col2 = st.beta_columns(2)

      #Strengths
      col1.header("Strengths")
      strength = soup.find("ul", class_="strength").text
      strength = strength.strip().replace('\n','  \n')
      if strength=='':
        col1.success('No Strength')
      else:
        col1.success(strength)

      #Limitations
      col2.header("Limitations")
      limitations = soup.find("ul", class_="limitations").text
      limitations = limitations.strip().replace('\n','  \n')
      if limitations=='':
            col2.error("No Limitations")
      else:
            col2.error(limitations)
      
      #Price Chart
      st.text("")
      st.header("Price Chart")
      ticker = user_input
      new_ticker = '\"'+'BSE:'+ticker+'\"'
      chart='''
      <!-- TradingView Widget BEGIN -->
      <div class="tradingview-widget-container">
        <div id="basic-area-chart"></div>
        <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/'''+ticker+'''/" rel="noopener" target="_blank"><span class="blue-text">'''+ticker+''' Chart</span></a> by TradingView</div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget(
        {
        "container_id": "basic-area-chart",
        "width": 1200,
        "height": 700,
        "symbol": '''+new_ticker+''',
        "interval": "D",
        "timezone": "exchange",
        "theme": "light",
        "style": "3",
        "toolbar_bg": "#f1f3f6",
        "hide_top_toolbar": true,
        "save_image": false,
        "locale": "en"
      }
        );
        </script>
      </div>
      <!-- TradingView Widget END -->
      '''
      components.html(chart,width=1400,height=700)

      #Annual Report
      reports = rk.balance_sheet(stock_name)
      annual_report = reports[1].rename(columns={'Unnamed: 0':' '})
      if 'TTM' in annual_report.columns:
          annual_report.drop('TTM',axis=1,inplace=True)
      years=np.array(annual_report.columns[1:])
      years= [int(item.split()[1]) for item in years]

      revenue=annual_report.iloc[0][1:]
      revenue = [int(item) for item in revenue]

      #Revenue (YOY)
      st.text("")
      st.header("Revenue (YOY) in Cr.")
      c=alt.Chart(pd.DataFrame({"Revenue":revenue,"Year":years})).mark_bar(size=50).encode(x='Year:O',y='Revenue',tooltip=['Revenue','Year'],opacity=alt.value(0.7),
      color=alt.value('#26c6da')).configure_view(strokeWidth=0).properties(height=500)
      st.altair_chart(c,use_container_width=True)

      #Profit (YOY)
      profit=annual_report.iloc[9][1:]
      profit = [int(item) for item in profit]

      st.text("")
      st.header("Profits (YOY) in Cr.")
      c=alt.Chart(pd.DataFrame({"Profit":profit,"Year":years})).mark_bar(size=50).encode(x='Year:O',y='Profit',tooltip=['Profit','Year'],opacity=alt.value(0.7),
      color=alt.value('#48e421')).configure_view(strokeWidth=0).properties(height=500)
      st.altair_chart(c,use_container_width=True)

      #Balance Sheet
      st.text("")
      st.header("Balance Sheet")
      balance_sheet = reports[6].rename(columns={'Unnamed: 0':' '})
      st.write(balance_sheet)

      #Shareholding pattern
      st.text("")
      st.header("Shareholding Pattern ")
      shareholders = list(reports[9]['Unnamed: 0'])
      shareholders = [i.rstrip("\xa0+") for i in shareholders]
      shareholding = list(reports[9][reports[9].columns[-1]])

      col1, col2, col3 = st.beta_columns([1,2,1])

      col1.write("")

      col2.vega_lite_chart(pd.DataFrame({'Shareholders':shareholders,'Shareholding':shareholding}), {
      "width": 600,
      "height": 600,
      "encoding": {
      "theta": {"field": "Shareholding", "type": "quantitative", "stack": True},
      "color": {"field": "Shareholders", "type": "nominal"},
      "tooltip": {"field": "Shareholding", "type": "quantitative"}
      },
      "layer": [{
          "mark": {"type": "arc", "outerRadius": 150}
      }, {
          "mark": {"type": "text", "radius": 190},
          "encoding": {
          "text": {"field": "Shareholders", "type": "nominal"}
          }
      }]
      })

      col3.write("")

      
      #Competitor analysis
      st.text("")
      st.header("Comparison with other stocks")
      stocks=[]
      stocks.append(stock.history(period="20y"))

      user_input2 = st.text_input("Enter stock 1",help="Enter a stock to compare with"+user_input)
      if user_input2!='':
          stock1 = yf.Ticker(user_input2.upper()+".NS")
          stocks.append(stock1.history(period="20y"))
          if (stocks[1].empty):
                  st.error("Error.....Incorrect")
                  st.stop()

      user_input3 = st.text_input("Enter stock 2",help="Enter a stock to compare with"+user_input)
      if user_input3!='':
          stock2 = yf.Ticker(user_input3.upper()+".NS")
          stocks.append(stock2.history(period="20y"))
          if (stocks[2].empty):
                  st.error("Error.....Incorrect")
                  st.stop()


      if user_input2!='' and user_input3!='':

        stocks[0]['symbol']=user_input
        stocks[1]['symbol']=user_input2
        stocks[2]['symbol']=user_input3
        #st.write(stocks[0].tail(5))
        df = pd.concat([s[['Close','Volume','symbol']] for s in stocks])
        df.reset_index(level=0, inplace=True) #make Date a column instead of index
        st.text("")
        st.header("Comparative Price Chart")
        c=alt.Chart(df,height=650).mark_line().encode(
        x='Date',
        y='Close',
        color='symbol',
        tooltip=alt.Tooltip(['Close'], format='.2f',title='INR')
        ).interactive()
        st.altair_chart(c,use_container_width=True)
        
        #volume
        st.text("")
        st.header("Traded Volumes")
        selection = alt.selection_multi(fields=['symbol'], bind='legend')
        c=alt.Chart(df,height=650).mark_line().encode(
        x='Date',
        y='Volume',
        color='symbol',
        tooltip=alt.Tooltip(['Volume']),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
        ).add_selection(selection)
        st.altair_chart(c,use_container_width=True)

        #Histogram
        st.text("")
        st.header("Daily Percentage Change")
        col1, col2, col3 = st.beta_columns(3)
        for i,col,name in (zip(range(3),[col1,col2,col3],[user_input,user_input2,user_input3])):
            stocks[i]['Returns']=stocks[i]['Close'].pct_change(1)
            col.altair_chart(alt.Chart(stocks[i]).mark_bar().encode(
                x=alt.X("Returns:Q", bin=alt.Bin(extent=[-0.100,0.100],step=0.005),title=name),
                y=alt.Y(aggregate="count",title="",type="quantitative")
            ).properties(height=500).interactive(),use_container_width=True)

        #Scatter Matrix
        st.text("")
        st.header("Scatter Matrix - (Finding Correlation)")
        st.text("")
        box_df = pd.concat([stocks[0]['Returns'],stocks[1]['Returns'],stocks[2]['Returns']],axis=1)
        box_df.columns = [user_input+" Returns",user_input2+" Returns",user_input3+" Returns"]
        st.altair_chart(alt.Chart(box_df).mark_circle().encode(
            alt.X(alt.repeat("column"), type='quantitative'),
            alt.Y(alt.repeat("row"), type='quantitative'),
            color='Origin:N'
        ).properties(
            width=385,
            height=185
        ).repeat(
            row=list(box_df.columns),
            column=list(box_df.columns[::-1])
        ).interactive(),use_container_width=True)


#PORTFOLIO OPTIMIZATION
def portfolio_optimization():
  def get_Position(weights,amount):
    weights = [i*amount for i in weights]
    stks = normed_stocks * weights
    stks['Total Position']=stks.sum(axis=1)
    return stks

  def cagr(f,l,y):
    return((round(l,2)/round(f,2))**(1/float(y)) - 1)

  def calc_portfolio_perf_VaR(weights, cov, alpha, days):
      
    #amount here is investment amount
    portfolio = portfolio_stocks * (weights*amount)
    portfolio['Total Position']=portfolio.sum(axis=1)
    portfolio_return = cagr(portfolio['Total Position'].iloc[0],portfolio['Total Position'].iloc[-1],11)
    
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov, weights))) * np.sqrt(days)
    portfolio_var = abs(portfolio_return - (portfolio_std * stats.norm.ppf(1 - alpha)))
    return portfolio_return, portfolio_std, portfolio_var

  def simulate_random_portfolios_VaR(num_portfolios, no_of_stocks, cov, alpha, days):

    results_matrix = np.zeros((no_of_stocks+3, num_portfolios))
    my_bar = st.progress(0)
    for i in range(num_portfolios):
      weights = np.random.random(no_of_stocks)
      weights /= np.sum(weights)
      portfolio_return, portfolio_std, portfolio_VaR = calc_portfolio_perf_VaR(weights, cov, alpha, days)
      results_matrix[0,i] = portfolio_return
      results_matrix[1,i] = portfolio_std
      results_matrix[2,i] = portfolio_VaR
      #iterate through the weight vector and add data to results array
      for j in range(len(weights)):
          results_matrix[j+3,i] = weights[j]
      my_bar.progress((i+1)/num_portfolios)
            
    results_df = pd.DataFrame(results_matrix.T,columns=['ret','stdev','VaR'] + [ticker for ticker in p_stocks])

    return results_df
          

  st.header("Enter portfolio stocks")
  p_stocks = st.text_input("Enter list of stocks separated by comma",help="Enter the ticker symbol of portfolio stock on BSE/NSE. Ex - TCS,INFY,HCLTECH").upper().split(',')
  no_of_stocks = len(p_stocks)

  if no_of_stocks == 1 and p_stocks[0]!='':
    st.error("Enter atleast two stocks")
    st.stop()
  portfolio = [yf.Ticker(i+".NS") for i in p_stocks]

  amount = st.number_input("Enter the total investment amount",help="The total to amount be invested in the portfolio",value=0)

  if amount <= 0:
    st.stop()

  for i in range(no_of_stocks):
    portfolio[i]=portfolio[i].history(start="2010-01-01") #contains ticker dataframe

  #Dropping unwanted columns
  portfolio = rk.drop_divnstksplit(portfolio)

  portfolio_stocks = pd.concat([df['Close'] for df in portfolio],axis=1)
  portfolio_stocks.columns = p_stocks

  st.header("Enter the portfolio allocation for each stock")
  st.info("**NOTE** - ***The sum of all the allocations should be equal to 1.0***")
  allocations=[]
  for i in p_stocks:
    allocations.append(st.number_input("Enter the portfolio allocation for - "+i,min_value=0.0, max_value=1.0,help="Ex - If you want to allocate 50% in two stocks enter 0.5 and 0.5 in the respective fields"))


  if sum(allocations) != 1.0 and allocations[-1]!=0.0:
    allocations = []
    st.error("(Error) Please Re - Enter, The sum of all allocations must equal to 1")
    st.stop()
  elif sum(allocations) == 1.0:
    normed_stocks=portfolio_stocks/portfolio_stocks.iloc[0]
    portfolio_val=get_Position(allocations,amount)

    # Portfolio Price Chart
    st.text("")
    st.subheader("Portfolio Performance (5 years)")
    p1_chart=alt.Chart(portfolio_val.reset_index(level=0)).mark_line().encode(x='Date',
    y='Total Position',color=alt.value('#34a853'),
    tooltip=alt.Tooltip(['Total Position'], format='.2f',title='INR')).properties(height=600).configure_view(strokeOpacity=0).configure_axis(grid=False).interactive()
    st.altair_chart(p1_chart,use_container_width=True)


    #Portfolio Histogram
    st.text("")
    st.subheader("Portfolio Return Distribution")
    portfolio_val['Daily Return'] = portfolio_val['Total Position'].pct_change(1)
    #Cumulative returns i.e total return from the day i invested till now
    # cum_ret = 100 * (portfolio_val['Total Position'][-1]/portfolio_val['Total Position'][0] -1 )
    # print('Our return was {}  percent!'.format(cum_ret))
    st.altair_chart(alt.Chart(portfolio_val).mark_bar().encode(
    alt.X("Daily Return:Q", bin=alt.Bin(extent=[-0.100,0.100], step=0.005)),y='count()',color=alt.value('#ff7c0c')
    ).properties(height=500).interactive(),use_container_width=True)

    st.write("")

    st.header("Portfolio Optimization")


    if st.button('Click Here To Optimize Portfolio!'):

      #PORTFOLIO OPTIMIZATION
      cov = portfolio_stocks.pct_change().cov()
      num_portfolios = 5000
      rf = 0.0
      days = 252
      alpha = 0.05

      results_frame = simulate_random_portfolios_VaR(num_portfolios, no_of_stocks, cov, alpha, days)

      #locate positon of portfolio with minimum VaR
      min_VaR_port = results_frame.iloc[results_frame['VaR'].idxmin()]
      #create scatter plot coloured by VaR

      fig1 = plt.figure()
      ax = fig1.add_subplot(1,1,1)
      ax.scatter(results_frame.VaR,results_frame.ret,c=results_frame.VaR,cmap='plasma')
      ax.set_xlabel('Value at Risk')
      ax.set_ylabel('Returns')
      ax.scatter(min_VaR_port[2],min_VaR_port[0],marker=(5,1,0),color='r',s=500)

      st.pyplot(fig1)

      st.header('***CAGR*** = '+str(min_VaR_port[0])+' ***VaR*** = '+str(min_VaR_port[2]))
      st.write("")
            

      col1, col2 = st.beta_columns([1,1])

      with col1:

        st.subheader("Your Allocation")
        st.vega_lite_chart(pd.DataFrame({'Stocks':p_stocks,'Allocation':allocations}), {
        "width": 600,
        "height": 600,
        "encoding": {
        "theta": {"field": "Allocation", "type": "quantitative", "stack": True},
        "color": {"field": "Stocks", "type": "nominal"},
        "tooltip": {"field": "Allocation", "type": "quantitative"}
        },
        "layer": [{
            "mark": {"type": "arc", "outerRadius": 150}
        }, {
            "mark": {"type": "text", "radius": 190},
            "encoding": {
            "text": {"field": "Stocks", "type": "nominal"}
            }
        }]
        })

        #CAGR and VaR
        c,s,v=calc_portfolio_perf_VaR(np.array(allocations),cov,alpha,days)
        st.subheader('***CAGR*** = '+str(c))
        st.subheader('***VaR*** = '+str(v))

        # Portfolio1 Price Chart
        st.text("")
        st.subheader("Input Portfolio Performance")
        st.altair_chart(p1_chart,use_container_width=True)


      with col2:

        st.subheader("Recommended Allocation")
        st.vega_lite_chart(pd.DataFrame({'Stocks':p_stocks,'Allocation':list(round(min_VaR_port[p_stocks]*100,2))}), {
        "width": 600,
        "height": 600,
        "encoding": {
        "theta": {"field": "Allocation", "type": "quantitative", "stack": True},
        "color": {"field": "Stocks", "type": "nominal"},
        "tooltip": {"field": "Allocation", "type": "quantitative"}
        },
        "layer": [{
            "mark": {"type": "arc", "outerRadius": 150}
        }, {
            "mark": {"type": "text", "radius": 190},
            "encoding": {
            "text": {"field": "Stocks", "type": "nominal"}
            }
        }]
        })

        #CAGR and VaR
        st.subheader('***CAGR*** = '+str(min_VaR_port[0]))
        st.subheader('***VaR*** = '+str(min_VaR_port[2]))

        # Portfolio2 Price Chart
        st.text("")
        st.subheader("Recommended Portfolio Performance")
        sugg_portfolio_val=get_Position(list(round(min_VaR_port[p_stocks],4)),amount)
        p2_chart=alt.Chart(sugg_portfolio_val.reset_index(level=0)).mark_line().encode(x='Date',
        y='Total Position',color=alt.value('#34a853'),
        tooltip=alt.Tooltip(['Total Position'], format='.2f',title='INR')).properties(height=600).configure_view(strokeOpacity=0).configure_axis(grid=False).interactive()
        st.altair_chart(p2_chart,use_container_width=True)


      results_frame.to_csv("results_frame.csv",index=False) 
      st.write("")

      #Generating portfolio for Custom Returns

    try:

      results_frame=pd.read_csv("results_frame.csv")
      st.write(results_frame)
      st.subheader("Want more returns! Just enter your expected return by referring the above Portfolio Allocation chart to get the most optimal portfolio for your expected return")
      st.info("**NOTE - ** The input return must be within the range of achievable returns from the above chart")
      st.write("")
      alt_return=st.number_input("Enter the expected portfolio return",min_value=round(min(results_frame['ret']),4), max_value=round(max(results_frame['ret']),4),help="Enter your expected return by refering the above graph")
      if alt_return == round(min(results_frame['ret']),4):
        st.stop()
      alt_var=min((results_frame[(results_frame['ret']<alt_return+0.0005) & (results_frame['ret']>alt_return-0.0005)]).VaR)
      st.write(alt_return)
      #Plotting the chart

      #locate positon of portfolio with minimum VaR
      min_VaR_port = results_frame.query('VaR=='+str(alt_var)).iloc[0]
      #create scatter plot coloured by VaR
      fig2 = plt.figure()
      ax = fig2.add_subplot(1,1,1)
      ax.scatter(results_frame.VaR,results_frame.ret,c=results_frame.VaR,cmap='plasma')
      ax.set_xlabel('Value at Risk')
      ax.set_ylabel('Returns')
      ax.scatter(min_VaR_port[2],min_VaR_port[0],marker=(5,1,0),color='r',s=500)
      st.pyplot(fig2)
      st.write("")

      c1, c2 = st.beta_columns([1,1])

      with c1:
        st.vega_lite_chart(pd.DataFrame({'Stocks':p_stocks,'Allocation':list(round(min_VaR_port[p_stocks]*100,2))}), {
        "width": 600,
        "height": 600,
        "encoding": {
        "theta": {"field": "Allocation", "type": "quantitative", "stack": True},
        "color": {"field": "Stocks", "type": "nominal"},
        "tooltip": {"field": "Allocation", "type": "quantitative"}
        },
        "layer": [{
            "mark": {"type": "arc", "outerRadius": 150}
        }, {
            "mark": {"type": "text", "radius": 190},
            "encoding": {
            "text": {"field": "Stocks", "type": "nominal"}
            }
        }]
        })

      with c2:
        st.subheader('***CAGR*** = '+str(min_VaR_port[0]))
        st.subheader('***VaR*** = '+str(min_VaR_port[2]))
        # Portfolio 3 Price Chart
        st.text("")
        st.subheader("Portfolio Performance")
        new_portfolio_val=get_Position(list(round(min_VaR_port[p_stocks],4)),amount)
        p2_chart=alt.Chart(new_portfolio_val.reset_index(level=0)).mark_line().encode(x='Date',
        y='Total Position',color=alt.value('#34a853'),
        tooltip=alt.Tooltip(['Total Position'], format='.2f',title='INR')).properties(height=600).configure_view(strokeOpacity=0).configure_axis(grid=False).interactive()
        st.altair_chart(p2_chart,use_container_width=True)



    except Exception as e:
      # st.error("Error")
      # st.exception(e)
      pass









#SIDEBBAR
PAGES = {
    "Stock Analysis": stock_analysis,
    "Portfolio Optimization": portfolio_optimization
}

st.sidebar.title("Navigator")

choice = st.sidebar.radio('Choose an application',['Stock Analysis','Portfolio Optimization'])
PAGES[choice]()




        
        




    
