# -*- coding: utf-8 -*-


import functools

from Analysis.SecurityValueHolders import SecurityShiftedValueHolder
from Analysis.SecurityValueHolders import SecurityDeltaValueHolder
from Analysis.SecurityValueHolders import SecurityCurrentValueHolder
from Analysis.SecurityValueHolders import SecurityLatestValueHolder
from Analysis.SecurityValueHolders import SecurityIIFValueHolder

from Analysis.CrossSectionValueHolders import CSRankedSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSTopNSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSBottomNSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSTopNPercentileSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSBottomNPercentileSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSAverageSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSAverageAdjustedSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSZScoreSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSPercentileSecurityValueHolder
from Analysis.CrossSectionValueHolders import CSResidueSecurityValueHolder


def CSRank(x, groups=None):
    return CSRankedSecurityValueHolder(x, groups)


def CSTopN(x, n, groups=None):
    print('CSTopN')
    return CSTopNSecurityValueHolder(x, n, groups)


def CSTopNQuantile(x, n, groups=None):
    return CSTopNPercentileSecurityValueHolder(x, n, groups)


def CSBottomN(x, n, groups=None):
    return CSBottomNSecurityValueHolder(x, n, groups)


def CSBottomNQuantile(x, n, groups=None):
    return CSBottomNPercentileSecurityValueHolder(x, n, groups)


def CSMean(x, groups=None):
    return CSAverageSecurityValueHolder(x, groups)


def CSMeanAdjusted(x, groups=None):
    return CSAverageAdjustedSecurityValueHolder(x, groups)


def CSQuantiles(x, groups=None):
    return CSPercentileSecurityValueHolder(x, groups)


def CSZScore(x, groups=None):
    return CSZScoreSecurityValueHolder(x, groups)


def CSRes(left, right):
    return CSResidueSecurityValueHolder(left, right)

def CURRENT(x='x'):
    return SecurityCurrentValueHolder(x)


def LAST(x='x'):
    return SecurityLatestValueHolder(x)


def DELTA(x, n):
    return SecurityDeltaValueHolder(x, n)


def IIF(flag, left, right):
    return SecurityIIFValueHolder(flag, left, right)


def INDUSTRY(name, level=1):
    name = name.lower()
    if name == 'sw':
        if level in (1, 2, 3):
            return LAST(name + str(level))
        else:
            raise ValueError('{0} is not recognized level for {1}'.format(level, name))
    else:
        raise ValueError('currently only `sw` industry is supported. {1} is not a recognized industry type')


HIGH = functools.partial(LAST, 'highestPrice')
LOW = functools.partial(LAST, 'lowestPrice')
OPEN = functools.partial(LAST, 'openPrice')
CLOSE = functools.partial(LAST, 'closePrice')



