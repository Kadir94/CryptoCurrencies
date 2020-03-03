#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "inlineBackend.figure_format = 'svg'")
plt.style.use('fivethirtyeight')



current = pd.read_json('https://api.coinmarketcap.com/v1/ticker/')
current.head()



df = pd.read_csv('coinmarketcap_06122017.csv.txt',sep=',')
mar_cap_raw = df[['id','market_cap_usd']]
mar_cap_raw.count()





cap = mar_cap_raw.query('market_cap_usd > 0')
cap.count()



#selecting first 10 rows and indexing them
cap10 = mar_cap_raw.head(10).set_index('id')
#calculate market_cap_perc
cap10 = cap10.assign(market_cap_perc = lambda x: x['market_cap_usd']/cap['market_cap_usd'].sum()*100)
#and plot
ax=cap10['market_cap_perc'].plot.bar()
ax.set_title('Top 10 market capitalization')
ax.set_ylabel('% of total cap')
plt.show()





#modifying the plot
Colors=['orange', 'green', 'orange', 'cyan', 'cyan', 'blue', 'silver', 'orange', 'red', 'green']
ax=cap10['market_cap_usd'].plot.bar( color = Colors)
ax.set_title('Top 10 market capitalization')
ax.set_ylabel('USD')
ax.set_xlabel('')
plt.show()



volatility = df[['id','percent_change_24h','percent_change_7d']]
#setting index to id and drop NAN values
volatility = volatility.set_index('id').dropna()
#sorting dataframe by percent_change_24h in asc
volatility = volatility.sort_values('percent_change_24h')
volatility.head()




#define function with 2 parameters,the series(column name) to plot and the title
def top10_subplot(volatility_series,title):
    fig,axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    ax = volatility_series[:10].plot.bar(color = 'darkred',ax = axs[0])
    ax.set_ylabel('% change')
    fig.suptitle(title)
    ax = volatility_series[-10:].plot.bar(color = 'darkblue',ax = axs[1])
    return fig,ax
DTITLE = '24 hours top losers and winners'
fig,axs = top10_subplot(volatility['percent_change_24h'],DTITLE)



#selecting everything bigger than 10 billion
largecaps = cap.query('market_cap_usd > 1e10')
print(largecaps)





#now check the cryptocurrencies how large they are
def capcount(query_string):
    return cap.query(query_string).count().id
#labels for plot
LABELS = ['biggish','micro','nano']

biggish = capcount('market_cap_usd > 3e8')
micro = capcount('market_cap_usd >= 50e6 & market_cap_usd <= 3e8')
nano = capcount ('market_cap_usd < 50e6')
values = [biggish,micro,nano]
plt.bar(x= LABELS, height=values)







