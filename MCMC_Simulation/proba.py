#%%
""" 
    Transition Matrix with checkout,
    Random probability calulator for entrance,
    and function for getting the number of customer per minute.

"""


import pandas as pd 
import numpy as np

#%%
# loading the cleaned data that was built in EDA.ipynb file
final = pd.read_csv('../data/cleaned_up/clean_final.csv', index_col=0)
final
#%% [markdown]
### Building Transition Matrix
#%%
# adding next location column 
final['next_location'] = final['location'].shift(-1)
# frequency table for number of customers in each state
final.groupby('location')['next_location'].value_counts().unstack()
# leaving the 'checkout' rows from location to be able to add the 'absorbing state' later on
df_1 = final[final['location'] != 'checkout'].copy()
# probability table without checkout in location
trans_without_checkout= pd.crosstab(df_1['location'], df_1['next_location'], normalize=0)
# Hardcoding the absorbing state into transition matrix
prob = np.array([1.0,0.0,0.0,0.0,0.0,
                0.138084,0.330109,0.186343,0.232072,0.113392,
                0.143430,0.326136,0.183015,0.232778,0.114641,
                0.127124,0.334015,0.173851,0.246696,0.118314,
                0.131730,0.329882,0.174737,0.239726,0.123925
                ]).reshape(5,5)
trans_matrix = pd.DataFrame(prob,columns=['checkout','dairy','drinks','fruit','spices'],
                index=['checkout','dairy','drinks','fruit','spices'])

#%%
# random probability for entrance (for visualization purposes)
entrance = np.identity(1)

# Add a random drift term.  We can guarantee that the diagonal terms
entrance = entrance + np.random.uniform(low=0. , size=(1, 4))

# Lastly, divide by row-wise sum to normalize to 1.
ent_prob = entrance / entrance.sum(axis=1, keepdims=1)
ent_prob = ent_prob.reshape(4,)

#%%
# dataframe with the time and average number of daily customers entering the supermarket per minute
entrance_number = (round(
    final[final["section_order"] == "first"]
    .groupby(["time"])[["cust_id"]]
    .count()
    / 5, 0)
)
remaining_minutes = pd.DataFrame(data=np.zeros(9,),columns=['cust_id'],index=['21:51:00','21:52:00','21:53:00','21:54:00','21:55:00','21:56:00','21:57:00','21:58:00','21:59:00'])
entrance_number = pd.concat([entrance_number,remaining_minutes])
