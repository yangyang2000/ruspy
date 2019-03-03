import pytest
import yaml
import numpy as np
from numpy.testing import assert_array_almost_equal
from ruspy.estimation.estimation import estimate
from ruspy.ruspy_config import TEST_RESOURCES_DIR
from ruspy.data.data_reading import data_reading
from ruspy.data.data_processing import data_processing

with open(TEST_RESOURCES_DIR + 'replication_test/init_replication_test.yml') as y:
    init_dict = yaml.load(y)
data_reading()
data = data_processing(init_dict['replication'])
result_trans, result_fixp = estimate(init_dict['replication'], data)

@pytest.fixture
def inputs():
    out = dict()
    out['trans_est'] = result_trans['x']
    out['params_est'] = result_fixp['x']
    return out

@pytest.fixture
def outputs():
    out = dict()
    out['trans_base'] = np.loadtxt(TEST_RESOURCES_DIR + 'replication_test/repl_test_trans.txt')
    out['params_base'] = np.loadtxt(TEST_RESOURCES_DIR + 'replication_test/repl_test_params.txt')
    return out


def test_repl_params(inputs, outputs):
    assert_array_almost_equal(inputs['params_est'], outputs['params_base'], decimal=4)


def test_repl_trans(inputs, outputs):
    assert_array_almost_equal(inputs['trans_est'], outputs['trans_base'], decimal=4)
