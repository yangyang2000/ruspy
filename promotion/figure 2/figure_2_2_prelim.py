import yaml
import numpy as np
import matplotlib.pyplot as plt
from ruspy.estimation.estimation_cost_parameters import create_transition_matrix
from ruspy.estimation.estimation_cost_parameters import myopic_costs
from ruspy.estimation.estimation_cost_parameters import lin_cost
from ruspy.estimation.estimation_cost_parameters import calc_fixp
from ruspy.simulation.simulation import simulate
from ruspy.plotting.discounting import discount_utility
from ruspy.simulation.robust_sim import get_worst_trans


with open('init.yml') as y:
    init_dict = yaml.load(y)

beta = init_dict['simulation']['beta']
init_dict['simulation']['states'] = 90

v_exp_known = []
v_exp_real = []
v_disc = []
roh_plot = []
for roh in np.arange(0, 4, 0.25):
    roh_plot += [roh]
    init_dict['simulation']['roh'] = roh
    worst_trans = get_worst_trans(init_dict['simulation'])
    init_dict['simulation']['real probs'] = worst_trans

    df, unobs, utilities, num_states = simulate(init_dict['simulation'])

    costs = myopic_costs(num_states, lin_cost, init_dict['simulation']['params'])

    num_buses = init_dict['simulation']['buses']
    num_periods = init_dict['simulation']['periods']
    gridsize = init_dict['plot']['gridsize']

    real_trans_probs = np.array(init_dict['simulation']['real probs'])
    real_trans_mat = create_transition_matrix(num_states, real_trans_probs)
    ev_real = calc_fixp(num_states, real_trans_mat, costs, beta)

    known_trans_probs = np.array(init_dict['simulation']['known probs'])
    known_trans_mat = create_transition_matrix(num_states, known_trans_probs)
    ev_known = calc_fixp(num_states, known_trans_mat, costs, beta)

    v_calc = 0
    for i in range(num_buses):
        v_calc = v_calc + unobs[i, 0, 0] + ev_known[0]
    v_calc = v_calc / num_buses
    v_exp_known += [v_calc]

    v_calc = 0
    for i in range(num_buses):
        v_calc = v_calc + unobs[i, 0, 0] + ev_real[0]
    v_calc = v_calc / num_buses
    v_exp_real += [v_calc]

    v_start = [0., 0.]
    v_disc += [discount_utility(v_start, num_buses, num_periods, num_periods,
                                utilities, beta)[1]]
    print(v_exp_known, v_exp_real, v_disc)

ax = plt.figure(figsize=(14, 6))

ax1 = ax.add_subplot(111)

ax1.set_ylim([0, -5000])

ax1.set_ylabel(r"Value at time 0")
ax1.set_xlabel(r"roh")

l1 = ax1.plot(roh_plot, v_disc, color='blue')
l2 = ax1.plot(roh_plot, v_exp_known, color='green')
l3 = ax1.plot(roh_plot, v_exp_real, color='red')

plt.tight_layout()

plt.savefig('figure_2_2.png', dpi=300)
