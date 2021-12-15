#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/7/23 14:24
Desc: 债券-集思录-可转债
集思录：https://app.jisilu.cn/data/cbnew/#cb
"""
import pandas as pd
import requests


def bond_cov_jsl(cookie: None = '') -> pd.DataFrame:
    """
    集思录可转债
    https://app.jisilu.cn/data/cbnew/#cb
    :return: 集思录可转债
    :rtype: pandas.DataFrame
    """
    url = "https://app.jisilu.cn/data/cbnew/cb_list/"
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-length': '220',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'origin': 'https://app.jisilu.cn',
        'pragma': 'no-cache',
        'referer': 'https://app.jisilu.cn/data/cbnew/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    params = {
        "___jsl": "LST___t=1627021692978",
    }
    payload = {
        "fprice": "",
        "tprice": "",
        "curr_iss_amt": "",
        "volume": "",
        "svolume": "",
        "premium_rt": "",
        "ytm_rt": "",
        "market": "",
        "rating_cd": "",
        "is_search": "N",
        'market_cd[]': 'shmb',
        'market_cd[]': 'shkc',
        'market_cd[]': 'szmb',
        'market_cd[]': 'szcy',
        "btype": "",
        "listed": "Y",
        'qflag': 'N',
        "sw_cd": "",
        "bond_ids": "",
        "rp": "50",
    }
    r = requests.post(url, params=params, json=payload, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame([item["cell"] for item in data_json["rows"]])
    return temp_df


def bond_conv_adj_logs_jsl(symbol: str = "128013") -> pd.DataFrame:
    """
    集思录可转债转股价调整记录
    https://app.jisilu.cn/data/cbnew/#cb
    :return: 转股价调整记录
    :rtype: pandas.DataFrame
    """
    url = "https://www.jisilu.cn/data/cbnew/adj_logs/?bond_id=%s" % symbol
    response = requests.get(url).text
    if '</table>' not in response:
        # 1. 该可转债没有转股价调整记录，服务端返回文本 '暂无数据'
        # 2. 无效可转债代码，服务端返回 {"timestamp":1639565628,"isError":1,"msg":"无效代码格式"}
        # 以上两种情况，返回空的 DataFrame
        return pd.DataFrame()
    else:
        return pd.read_html(response, parse_dates=True)[0]


if __name__ == '__main__':
    bond_convert_jsl_df = bond_cov_jsl(cookie='')
    print(bond_convert_jsl_df)
    bond_conv_adj_logs_jsl_df = bond_conv_adj_logs_jsl()
    print(bond_conv_adj_logs_jsl_df)
