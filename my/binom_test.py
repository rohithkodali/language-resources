#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""One-sided binomial test.

Performs a binomial test concerning an alternative hypothesis that the
observed number of successes in a given number of Bernoulli trials is
greater than what would be expected under the null hypothesis involving a
known fixed probability of success.

Prints verbose test results in a well-known output format.
"""

from __future__ import division, print_function

import sys

from scipy import stats


def UpperTailPValue(successes, trials, prob):
  assert 0 <= successes <= trials
  assert 0 <= prob <= 1
  p_value = stats.binom.sf(successes - 1, trials, prob)
  return p_value


def UpperTailConfidenceInterval(successes, trials, conf_level):
  assert 0 <= successes <= trials
  assert 0 <= conf_level <= 1
  if successes == 0:
    lo = 0
  else:
    lo = stats.beta.ppf(1 - conf_level, successes, trials - successes + 1)
  hi = 1
  return lo, hi


def UpperTailBinomTest(x, n, p=0.5, conf_level=0.95):
  p_value = UpperTailPValue(x, n, p)
  confint = UpperTailConfidenceInterval(x, n, conf_level)
  print()
  print('\tExact binomial test')
  print()
  print('data:  %d and %d' % (x, n))
  print('number of successes = %d, number of trials = %d, p-value = %.7g'
        % (x, n, p_value))
  print('alternative hypothesis: true probability of success is' +
        ' greater than %.7g' % p)
  print('%g percent confidence interval:' % (conf_level * 100.0))
  print(' %.7g %.7g' % confint)
  print('sample estimates:')
  print('probability of success')
  print('          %12.7g' % (x / n))
  print()
  return p_value


def main(argv):
  successes = int(argv[1])
  trials = int(argv[2])
  prob = float(argv[3])
  conf_level = 0.95 if len(argv) < 5 else float(argv[4])
  p_value = UpperTailBinomTest(successes, trials, prob, conf_level)
  significance_level = 1 - conf_level
  sys.exit(0 if p_value > significance_level else 1)
  return


if __name__ == '__main__':
  main(sys.argv)
