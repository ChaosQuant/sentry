# -*- coding: utf-8 -*-
import time
import numpy as np
from Utilities.Asserts import pyFinAssert
from Utilities.Asserts import pyFinWarning
from Utilities.Asserts import isClose

__all__ = ['pyFinAssert',
           'pyFinWarning',
           'isClose']


def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        return t2 - t1, res
    return wrapper