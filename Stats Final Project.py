#!/usr/bin/env python
# coding: utf-8

# In[128]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# In[62]:


path = '/Users/walkers/Downloads/Actual Stats Data.csv'
#data as of 3/4/2022

df = pd.read_csv(path)
df.describe()


# In[63]:


df.head(107) # to see how goalies look


# In[64]:


total_played = df['GP'].count()
print("Percentage of Drafted Players Appearing in NHL:", (round(total_played/len(df['GP']), 2)))


# In[65]:


df['GP.1'] = df['GP.1'].isnull()
df = df.rename(columns={"GP.1": "Skater"})


# In[74]:


df['PS_per_GP'] = np.where(df['Skater'] == True, df['PS']/df['GP'], (2*df['PS'])/(3*df['GP']))
#Adjusts for goalies only playing ~2/3 of games
df.head(45)


# In[126]:


grp = df.groupby(by='Overall').sum()[{'PS_per_GP', 'PS'}]
prev_gp_name = 'PS_per_GP'
prev_reg_name = 'PS'

for x in range(1,5):
    x*=5
    gp_name = "GP_rolling" + str(x)
    reg_name = "Rolling" + str(x)
    grp[gp_name] = grp['PS_per_GP'].rolling(x).mean()
    grp[gp_name] = grp[gp_name].fillna(grp[prev_gp_name])
    grp[reg_name] = grp['PS'].rolling(x).mean()
    grp[reg_name] = grp[reg_name].fillna(grp[prev_reg_name])
    prev_reg_name = reg_name
    prev_gp_name = gp_name

grp[['PS','Rolling5','Rolling10','Rolling15','Rolling20']].plot()
grp['Zero'] = 0
grp[['PS_per_GP','GP_rolling5','GP_rolling10','GP_rolling15','GP_rolling20', "Zero"]].plot()


# In[127]:


#Zoom in on the first round
first = grp.head(30)
first[['PS','Rolling5','Rolling10']].plot()
first[['PS_per_GP','GP_rolling5','GP_rolling10']].plot()


# In[188]:


x = np.linspace(1,210,num=210)
arr = grp['PS']


# In[189]:


def func(x, a, b, c):
    return (a * np.exp(-b*x)) + c


# In[190]:


popt, pcov = curve_fit(func, x, arr)


# In[191]:


print(popt)


# In[192]:


plt.plot(x, arr, 'b-', label='data')
plt.plot(x, func(x, *popt), 'g--',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))


# In[193]:


for i in range(10):
    val = i
    print(func(val+1,popt[0],popt[1],popt[2]), val)


# In[194]:


grp['Rolling10']


# In[260]:


final = df.groupby(by='Overall').sum()[{'PS_per_GP', 'PS'}]

gp_name = "Pick Value"

final[gp_name] = final['PS'].rolling(10).mean()
for i in range(9):
    final.iloc[i,2] = func(i,popt[0],popt[1],popt[2])*1.2

final[[gp_name]].plot()

values = final[gp_name].tolist()


# In[263]:


first = final.head(30)
first[[gp_name]].plot()


# In[254]:


def trade_analysis(name_1, name_2, team_1, team_2): #list of picks each team acquired
    team_1_total = 0
    team_2_total = 0
    winner = name_1
    for i in range(len(team_1)):
        team_1_total += values[team_1[i]]
    for i in range(len(team_2)):
        team_2_total += values[team_2[i]]
    
    delta = team_1_total - team_2_total
    if (delta < 0):
        winner = name_2
        delta = abs(delta)
    
    
    for equiv in range(210):
        if (delta > values[equiv]):
            equiv +=1
            break;

    print("The %s won the trade, gaining %f expected future point shares,\nor approximately the value of the no. %d overall pick" 
          % (winner, delta, equiv))
    
    #team Winner won the trade, gaining Delta expected future point shares, or the equivalent of 
    #the N overall pick
    


# In[255]:


trade_analysis("Walke", "Anuka", [20], [22,90])


# In[256]:


trades = [["Rangers", "Senators", [22], [26,48]], 
          ["Blues", "Maple Leafs", [25], [29,76]],
          ["Coyotes", "Flyers", [11], [14,45]],
          ["Blues", "Flames", [19], [22,72]],
          ["Red Wings", "Stars", [15], [23,48,138]],
          ["Oilers", "Wild", [20], [22,90]],
          ["Predators", "Hurricanes", [27], [40,51]]]


# In[257]:


for trade in trades:
    trade_analysis(trade[0], trade[1], trade[2], trade[3])
    print("\n")


# In[262]:


picks_desired = [0, 29, 59, 149, 209]
for pick in picks_desired:
    val = values[pick]
    print("The no. %d pick is worth %f expected future point shares" % (pick+1, val))


# In[ ]:




