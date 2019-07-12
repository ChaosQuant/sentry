import sys
import pdb
import json
import copy
from sqlalchemy import create_engine
from sqlalchemy import select, and_
import pandas as pd
import numpy as np
from model import Market
sys.path.append('../..')
from api import *
from api.Analysis import DELTA
from Math.Accumulators import Log
from Math.Accumulators import MovingRank
from Math.Accumulators.IAccumulators import Pow

def recursion_func(formula_list, operator_list):
    new_list = []
    for formula_i in formula_list:
        for formula_j in formula_list:
            for op in operator_list:
                if formula_i != formula_j:
                    func = '({0}) {1} ({2})'.format(formula_i, op, formula_j)
                    new_list.append(func)
    return new_list

##参数化递归方式
def recursion_params():
    alpha2 = '(CLOSE() - LOW()) - (HIGH() - CLOSE()) / (HIGH() - LOW()) * param1'
    alpha26 = '(CLOSE() + HIGH() + LOW()) / param1'
    alpha154 = '(CLOSE() + HIGH() + LOW()) / param1 * VOLUME()'
    alpha250 = '(CLOSE() * param1 + HIGH() * param2) / (OPEN() * param3 + LOW() * param4)'
    
    formula_dict = {}
    with open('Alpha191_param.json','rb') as f:
        content = f.read()
        json_ob = json.loads(content)
        for name,values in json_ob.items():
            variable_name = locals()[name]
            formula_list = []
            for params in values:
                variable = copy.deepcopy(variable_name)
                for key in params.keys():
                    variable = variable.replace(key,str(params[key]))
                formula_list.append(variable)
            formula_dict[name] = formula_list
    
    new_list = []
    rule_list = ['alpha2', 'alpha26', 'alpha154', 'alpha250']
    operator_list = ['+','-']
    for formula_i in rule_list:
        for formula_j in rule_list:
            for op in operator_list:
                #获取对应的参数公式
                formula_i_list = formula_dict[formula_i]
                formula_j_list = formula_dict[formula_j]
                for fi in formula_i_list:
                    for fj in formula_j_list:
                        if fi != fj:
                            func = '({0}) {1} ({2})'.format(fi, op, fj)
                            new_list.append(func)
    
    #应采用树形结构存储，若上级设置无效，子树都设置无效
    new_list1 = []
    for formula_i in new_list:
        for formula_j in new_list:
            for op in operator_list:
                if formula_i != formula_j:
                    func = '({0}) {1} ({2})'.format(formula_i, op, formula_j)
                    new_list1.append(func)
    pdb.set_trace()
    new_list = new_list1 +  new_list
    
##递归方式
def recursion_formula():
    deep_length = 2
    alpha2 = '(CLOSE() - LOW()) - (HIGH() - CLOSE()) / (HIGH() - LOW()) * 1.5'
    alpha26 = '(CLOSE() + HIGH() + LOW()) / 3'
    alpha154 = '(CLOSE() + HIGH() + LOW()) / 1.2 * VOLUME()'
    alpha250 = '(CLOSE() * 1.2 + HIGH() * 1.5) / (OPEN() * 1.4 + LOW() * 1.3)'
    rule_list = [alpha2, alpha26, alpha154]
    operator_list = ['+','-']
    new_formula_list = rule_list
    temp_list = []
    for i in range(0, deep_length):
        temps_list = rule_list
        temp_list = recursion_func(temps_list, operator_list)
        new_formula_list += temp_list
        temps_list = temp_list

    engine = create_engine('postgresql+psycopg2://alpha:alpha@180.166.26.82:8889/alpha')
    begin_date = '2018-12-01'
    end_date = '2018-12-28'
    query = select([Market]).where(
                and_(Market.trade_date >= begin_date, Market.trade_date <= end_date, ))
    mkt_df = pd.read_sql(query, engine)
    mkt_df.rename(columns={'preClosePrice':'pre_close','openPrice':'openPrice',
                          'highestPrice':'highestPrice','lowestPrice':'lowestPrice',
                          'closePrice':'closePrice','turnoverVol':'turnoverVol',
                          'turnoverValue':'turnover_value','accumAdjFactor':'accum_adj',
                           'vwap':'vwap'}, inplace=True)
    mkt_df = mkt_df[[('000000' + str(code))[-6:][0] in '036' for code in mkt_df['code']]]
    trade_date_list = list(set(mkt_df.trade_date))
    trade_date_list.sort(reverse=True)
    mkt_df = mkt_df.set_index(['trade_date', 'code'])
    mkt_df = mkt_df[mkt_df['turnoverVol'] > 0]
    df = mkt_df.loc['2018-12-03']
    
    for formula in new_formula_list:
        pdb.set_trace()
        data = eval(formula).transform(df)
        print('-------')
    
    
    
def params_formula():
    ##参数化
    ##读取配置文件参数
    ##遍历生成对应的公式化
    alpha2 = '(CLOSE() - LOW()) - (HIGH() - CLOSE()) / (HIGH() - LOW()) * param1'
    alpha26 = '(CLOSE() + HIGH() + LOW()) / param1'
    alpha154 = '(CLOSE() + HIGH() + LOW()) / param1 * VOLUME()'
    alpha250 = '(CLOSE() * param1 + HIGH() * param2) / (OPEN() * param3 + LOW() * param4)'
    
    formula_dict = {}
    with open('Alpha191_param.json','rb') as f:
        content = f.read()
        json_ob = json.loads(content)
        for name,values in json_ob.items():
            variable_name = locals()[name]
            formula_list = []
            for params in values:
                variable = copy.deepcopy(variable_name)
                for key in params.keys():
                    variable = variable.replace(key,str(params[key]))
                formula_list.append(eval(variable))
            formula_dict[name] = formula_list
    
    engine = create_engine('postgresql+psycopg2://alpha:alpha@180.166.26.82:8889/alpha')
    begin_date = '2018-12-01'
    end_date = '2018-12-28'
    query = select([Market]).where(
                and_(Market.trade_date >= begin_date, Market.trade_date <= end_date, ))
    mkt_df = pd.read_sql(query, engine)
    mkt_df.rename(columns={'preClosePrice':'pre_close','openPrice':'openPrice',
                          'highestPrice':'highestPrice','lowestPrice':'lowestPrice',
                          'closePrice':'closePrice','turnoverVol':'turnoverVol',
                          'turnoverValue':'turnover_value','accumAdjFactor':'accum_adj',
                           'vwap':'vwap'}, inplace=True)
    mkt_df = mkt_df[[('000000' + str(code))[-6:][0] in '036' for code in mkt_df['code']]]
    trade_date_list = list(set(mkt_df.trade_date))
    trade_date_list.sort(reverse=True)
    mkt_df = mkt_df.set_index(['trade_date', 'code'])
    mkt_df = mkt_df[mkt_df['turnoverVol'] > 0]
    df = mkt_df.loc['2018-12-03']
    
    for formula in formula_list:
        pdb.set_trace()
        data = formula.transform(df)
        print('-------')

        
recursion_params()