"""
This module creates  a pickle file which contain the total number of observations for each group.
Therefore every DataFrame row contains the bus identifier, the state variable and the according decision. Also the
odometer gets set to zero after replacement.
"""


import pandas as pd
import os
import numpy as np

def data_processing(init_dict):
    repl = dict()
    df = pd.read_pickle('pkl/group_data/' + init_dict['group'] + '.pkl')
    for i in df.index:
        repl[i] = 0
    for j, i in enumerate(df.columns.values[11:]):
        df2 = df[['Bus_ID', i]]
        df2 = df2.assign(decision=0)
        for m in df2.index:
            if repl[m] == 1:
                df2.at[m, i] = df2.iloc[m][i] - df.iloc[m]['Odo_1st']
            if repl[m] == 2:
                df2.at[m, i] = df2.iloc[m][i] - df.iloc[m]['Odo_2nd']
            if i < df.columns.values[-1]:
                if (df.iloc[m][i+1] > df.iloc[m]['Odo_1st']) & (df.iloc[m]['Odo_1st'] != 0) & (repl[m] == 0):
                    df2.at[m, 'decision'] = 1
                    repl[m] = repl[m] + 1
                if (df.iloc[m][i+1] > df.iloc[m]['Odo_2nd']) & (df.iloc[m]['Odo_2nd'] != 0) & (repl[m] == 1):
                    df2.at[m, 'decision'] = 1
                    repl[m] = repl[m] + 1
        df2 = df2.rename(columns={i: 'state'})
        if j == 0:
            df3 = df2
        else:
            df3 = pd.concat([df3, df2])

    num_bus = len(df3['Bus_ID'].unique())
    num_periods = df3.shape[0] / num_bus
    df3['period'] = np.arange(num_periods).repeat(num_bus).astype(int)
    df3[['state']] = (df3[['state']] / init_dict['binsize']).astype(int)
    df3.sort_values(['Bus_ID', 'period'], inplace=True)
    df3.reset_index(drop=True, inplace=True)
    os.makedirs('pkl/replication_data', exist_ok=True)
    df3.to_pickle('pkl/replication_data/Rep' + init_dict['group'] + '.pkl')
    return df3
