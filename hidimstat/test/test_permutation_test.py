"""
Test the gaonkar module
"""

import numpy as np
from nose.tools import assert_almost_equal

from hidimstat.scenario import scenario
from hidimstat.permutation_test import permutation_test_cv


def test_clustered_inference():

    scenario_type = 'Toeplitz'
    seed = 0
    n_samples, n_features = 20, 50
    effect_small, effect_medium, effect_large = 0.25, 0.5, 1.0
    effect_s_nb, effect_m_nb, effect_l_nb = 0, 0, 1
    sigma = 0.1
    rho = 0.0
    shuffle = False

    n_support = effect_s_nb + effect_m_nb + effect_l_nb

    y, beta, X_init, epsilon = scenario(
        scenario_type, seed, n_samples, n_features, effect_small,
        effect_medium, effect_large, effect_s_nb, effect_m_nb, effect_l_nb,
        sigma, rho, shuffle)

    y = y - np.mean(y)
    X_init = X_init - np.mean(X_init, axis=0)

    sf_corr, cdf_corr = permutation_test_cv(X_init, y, n_permutations=100)

    expected = 0.5 * np.ones(n_features)
    expected[:n_support] = 0.0

    for i in np.arange(expected.size):
        assert_almost_equal(sf_corr[i], expected[i], places=1)
