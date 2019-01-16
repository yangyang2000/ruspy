""""
This function replicates Rust's 1987 paper on optimal bus engine replacement for the GMC 1975 buses
in the sample.
:return:
result.json         : A json file with the results stored.
transistion_results : A list with the estimated transition probabilities.
result              : A dictionary with the estimation results on the cost parameters.
"""

import pandas as pd
import numpy as np
import scipy.optimize as opt
import yaml
import json

from estimation_auxiliary import estimate_transitions_5000
from estimation_auxiliary import create_transition_matrix
from estimation_auxiliary import create_state_matrix
from estimation_auxiliary import loglike_opt_rule

with open('init.yml') as y:
    init_dict = yaml.load(y)

beta = init_dict['beta']
group = init_dict['group']
df = pd.read_pickle('../pkl/replication_data/Rep' + group + '.pkl')
df[['state']] = (df[['state']]/5000).astype(int)  # Creating states.
transition_results = estimate_transitions_5000(df)
endog = df.loc[:, 'decision']
exog = df.loc[:, 'state']
num_obs = df.shape[0]
num_states = init_dict['states']
decision_mat = np.vstack(((1 - endog), endog))
trans_mat = create_transition_matrix(num_states, np.array(transition_results['x']))
state_mat = create_state_matrix(exog, num_states, num_obs)
result = opt.minimize(loglike_opt_rule, args=(num_states, trans_mat, state_mat, decision_mat, beta),
                      x0=np.array([5, 5]), bounds=[(1e-6, None), (1e-6, None)])

json.dump([transition_results['x'].tolist(), result['x'].tolist()],
              open('result_5000.json', 'w'))

print(transition_results, result)
