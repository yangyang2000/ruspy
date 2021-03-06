import matplotlib.pyplot as plt
import yaml
import numpy as np
from ruspy.simulation.simulation import simulate
from ruspy.plotting.value_zero import discount_utility
from ruspy.plotting.value_zero import calc_ev_0
from ruspy.estimation.estimation_cost_parameters import calc_fixp
from ruspy.estimation.estimation_cost_parameters import lin_cost
from ruspy.estimation.estimation_cost_parameters import myopic_costs
from ruspy.estimation.estimation_cost_parameters import create_transition_matrix

with open("init.yml") as y:
    init_dict = yaml.safe_load(y)

beta = init_dict["simulation"]["beta"]

df, unobs, utilities, num_states = simulate(init_dict["simulation"])

costs = myopic_costs(num_states, lin_cost, init_dict["simulation"]["params"])
trans_probs = np.array(init_dict["simulation"]["probs"])
trans_mat = create_transition_matrix(num_states, trans_probs)
ev = calc_fixp(num_states, trans_mat, costs, beta)
num_buses = init_dict["simulation"]["buses"]
num_periods = init_dict["simulation"]["periods"]
gridsize = init_dict["plot"]["gridsize"]
num_points = int(num_periods / gridsize)

v_exp = np.full(num_points, calc_ev_0(ev, unobs, num_buses))

v_start = np.zeros(num_points)
v_disc = discount_utility(v_start, num_buses, gridsize, num_periods, utilities, beta)

periods = np.arange(0, num_periods, gridsize)

ax = plt.figure(figsize=(14, 6))

ax1 = ax.add_subplot(111)

ax1.set_ylim([0, -1500])

ax1.set_ylabel(r"Value at time 0")
ax1.set_xlabel(r"Periods")

ax1.plot(periods, v_disc, color="blue")
ax1.plot(periods, v_exp, color="orange")

plt.tight_layout()

plt.savefig("figure_1.png", dpi=300)
