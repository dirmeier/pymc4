"""PyMC4 Distribution of a random variable consisting of a mixture of other
distributions.

Wraps tfd.Mixture as pm.Mixture
"""
import tensorflow as tf
from tensorflow_probability import distributions as tfd

import pymc4 as pm
from pymc4.distributions.distribution import Distribution


class Mixture(Distribution):
    r"""
    Mixture random variable.

    Often used to model subpopulation heterogeneity

    .. math:: f(x \mid w, \theta) = \sum_{i = 1}^n w_i f_i(x \mid \theta_i)

    ========  ============================================
    Support   :math:`\cap_{i = 1}^n \textrm{support}(f_i)`
    Mean      :math:`\sum_{i = 1}^n w_i \mu_i`
    ========  ============================================

    Parameters
    ----------
    p : array of floats
        p >= 0 and p <= 1
        the mixture weights, in the form of probabilities, must sum to one.
    distributions : multidimensional PyMC4 distribution (e.g. `pm.Poisson(...)`)
        or iterable of one-dimensional PyMC4 distributions the
        component distributions :math:`f_1, \ldots, f_n`
    """

    def __init__(self, name, p, distributions, **kwargs):
        super().__init__(name, p=p, distributions=distributions, **kwargs)

    @staticmethod
    def _init_distribution(conditions):
        p, distributions = conditions["p"], conditions["distributions"]
        if isinstance(p, pm.Categorical):
            cat = p._distribution
        else:
            cat = tfd.Categorical(probs=p)
        if isinstance(distributions, list):
            distributions = [d._distribution for d in distributions]
        elif isinstance(distributions, Distribution):
            return
        return tfd.Mixture(cat=cat, components=distributions)
