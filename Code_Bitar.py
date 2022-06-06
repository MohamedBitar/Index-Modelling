import pandas as pd
import numpy as np

from datetime import datetime as dt


#Read the csv data 
data = pd.read_csv(r'C:\Users\DISIPLINE\Desktop\Test\Assessment-Index-Modelling-master\data_sources\stock_prices.csv')

# Managing data to get a better access
data=data.transpose()
data.columns = data.iloc[0] 
data = data[1:] 



# Collecting all LAST business days -  ( Let's call LD := Last Day)
LD = pd.date_range('2019-12-30', '2020-12-31',freq='CBM')
LD = LD.format(formatter=lambda x: x.strftime('%d/%m/%Y'))

# Collecting all FIRST business days ( Let's call FD := First Day)
FD = pd.date_range('2019-12-30', '2020-12-31',freq='BMS')
FD = FD.format(formatter=lambda x: x.strftime('%d/%m/%Y'))


# To collect the top three stocks for month
selected_stocks = []

for i in range(len(LD)-1):
    
    S = data[LD[i]].iloc[data[LD[i]].argsort()[-3:]]
    
    selected_stocks.append(S) # stocks_selected[i] gives the top three stocks for the (i+1)th month


#We will collect Index values over the year
Index_Evolution=[]
Index_Evolution.append(['Date','Index Level']) #Column names

#Initial Value
Index = 100

#weights
w=[0.25,0.25,0.5]

#Shares
X = np.multiply( w , Index )

#We introduce j for month changes (which probably implies stocks changes for our index, so respliting cash)
j=1

for i in range(len(data.columns) -2 ): #2):
    
    
    day = data.columns[i+2] #Starting the 1st January 2020
    DAY = dt.strptime(day, '%d/%m/%Y')
    M = DAY.month
    
    # Top 3 Stocks , Prices at the first business day 
    S_Fixed = data[FD[j-1]][selected_stocks[j-1].index]
    
    
    # Top 3 Stocks , Prices for the loop day ( will go through all business days for 2020 )
    S = data[day][selected_stocks[j-1].index]
    
    # a defined as a coefficient, representing the prices variation between 'loop day' and 'first business day' ( for the Top 3 stocks )
    a = 1 + (S-S_Fixed)/S_Fixed 
    
    # Computing the Index price : multipling Index shares by the evolution coefficient (component by component) and summing
    Index = sum(a*X)
    
    Index_Evolution.append([day,Index])

    if j != M:
        # Shares will change over the year (during month), so we update components of our Index    
        X = np.multiply(w,Index)
        j=j+1

df = pd.DataFrame(data=Index_Evolution)#,columns=({'Date','Index Level'}))

#saving into csv file (located in code folder )
df.to_csv('results_Bitar.csv',index=False,header=False,sep=';')


