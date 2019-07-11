# -*- coding: utf-8 -*-

import copy
from Analysis.SecurityValueHolders cimport SecurityValueHolder
from Analysis.SecurityValueHolders cimport SecurityCombinedValueHolder
from Analysis.SecurityValueHolders cimport build_holder
from Math.Accumulators.IAccumulators cimport Sign
from Math.Accumulators.StatelessAccumulators cimport XAverage
from Math.Accumulators.StatefulAccumulators cimport MACD
from Math.Accumulators.IAccumulators cimport Exp
from Math.Accumulators.IAccumulators cimport Log
from Math.Accumulators.IAccumulators cimport Pow
from Math.Accumulators.IAccumulators cimport Sqrt
from Math.Accumulators.IAccumulators cimport Abs
from Math.Accumulators.IAccumulators cimport Acos
from Math.Accumulators.IAccumulators cimport Acosh
from Math.Accumulators.IAccumulators cimport Asin
from Math.Accumulators.IAccumulators cimport Asinh
from Math.Accumulators.IAccumulators cimport NormInv
from Math.Accumulators.IAccumulators cimport Ceil
from Math.Accumulators.IAccumulators cimport Floor
from Math.Accumulators.IAccumulators cimport Round
from Math.Accumulators.StatelessAccumulators cimport Diff
from Math.Accumulators.StatelessAccumulators cimport SimpleReturn
from Math.Accumulators.StatelessAccumulators cimport LogReturn
from Analysis.SeriesValues import s_maximum
from Analysis.SeriesValues import s_minimum


cdef class SecurityStatelessSingleValueHolder(SecurityValueHolder):
    def __init__(self, holderType, x, **kwargs):
        super(SecurityStatelessSingleValueHolder, self).__init__()
        self._compHolder = build_holder(x)
        self._holderTemplate = holderType(x=str(self._compHolder), **kwargs)
        self._innerHolders = {name: copy.deepcopy(self._holderTemplate) for name in self._compHolder.symbolList}
        self._dependency = self._compHolder.fields

    def __str__(self):
        return str(self._holderTemplate)


cdef class SecurityXAverageValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, window, x):
        super(SecurityXAverageValueHolder, self).__init__(holderType=XAverage,
                                                          x=x,
                                                          window=window)


cdef class SecurityMACDValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, short_win, long_win, x):
        super(SecurityMACDValueHolder, self).__init__(holderType=MACD,
                                                      x=x,
                                                      short_win=short_win,
                                                      long_win=long_win)


cdef class SecuritySignValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecuritySignValueHolder, self).__init__(holderType=Sign,
                                                      x=x)


cdef class SecurityExpValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x='x'):
        super(SecurityExpValueHolder, self).__init__(holderType=Exp,
                                                     x=x)


cdef class SecurityLogValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityLogValueHolder, self).__init__(holderType=Log,
                                                     x=x)


cdef class SecurityPowValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x, n=1):
        super(SecurityPowValueHolder, self).__init__(holderType=Pow,
                                                     x=x,
                                                     n=n)


cdef class SecuritySqrtValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecuritySqrtValueHolder, self).__init__(holderType=Sqrt,
                                                      x=x)


cdef class SecurityAbsValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityAbsValueHolder, self).__init__(holderType=Abs,
                                                     x=x)


cdef class SecurityAcosValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityAcosValueHolder, self).__init__(holderType=Acos,
                                                      x=x)


cdef class SecurityAcoshValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityAcoshValueHolder, self).__init__(holderType=Acosh,
                                                       x=x)


cdef class SecurityAsinValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityAsinValueHolder, self).__init__(holderType=Asin,
                                                      x=x)


cdef class SecurityAsinhValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityAsinhValueHolder, self).__init__(holderType=Asinh,
                                                       x=x)


cdef class SecurityNormInvValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x, fullAcc=False):
        super(SecurityNormInvValueHolder, self).__init__(holderType=NormInv,
                                                         x=x,
                                                         fullAcc=fullAcc)


cdef class SecurityCeilValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityCeilValueHolder, self).__init__(holderType=Ceil,
                                                      x=x)


cdef class SecurityFloorValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityFloorValueHolder, self).__init__(holderType=Floor,
                                                       x=x)


cdef class SecurityRoundValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityRoundValueHolder, self).__init__(holderType=Round,
                                                       x=x)


cdef class SecurityDiffValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityDiffValueHolder, self).__init__(holderType=Diff,
                                                      x=x)


cdef class SecuritySimpleReturnValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecuritySimpleReturnValueHolder, self).__init__(holderType=SimpleReturn,
                                                              x=x)


cdef class SecurityLogReturnValueHolder(SecurityStatelessSingleValueHolder):
    def __init__(self, x):
        super(SecurityLogReturnValueHolder, self).__init__(holderType=LogReturn,
                                                           x=x)


cdef class SecurityMaximumValueHolder(SecurityCombinedValueHolder):
    def __init__(self, x, y):
        super(SecurityMaximumValueHolder, self).__init__(x, y, s_maximum)

    def __str__(self):
        return "maximum({0}, {1})".format(str(self._left), str(self._right))


cdef class SecurityMinimumValueHolder(SecurityCombinedValueHolder):
    def __init__(self, x, y):
        super(SecurityMinimumValueHolder, self).__init__(x, y, s_minimum)

    def __str__(self):
        return "minimum({0}, {1})".format(str(self._left), str(self._right))
