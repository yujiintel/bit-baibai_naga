#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains an `Algorithm` developed by Yuuji Nagatomo for automatically
determing when to buy and sell virtual currencies.
"""
import numpy as np
from .Algorithm import Algorithm
from datetime import datetime,timedelta
from ..TransationRecord import TransationRecord

class NagatomoAlgorithm(Algorithm):
    """
    長友さん特製のアルゴリズム！
    """
    def __init__(self,sigma):
        self.sigma = sigma
        self.data = []
        self.last_buy = None
        self.last_sell = None

    def process_data(self, price_samples):
        super().process_data(price_samples)
        for sample in price_samples:
            self.data.append(sample)
        # TODO:

    def check_far_enough_in_past(self,transaction):
        min_wait = timedelta(hours=3)
        if transaction is None:
            return True
        else:
            return transaction.date < datetime.now() - min_wait

    def check_should_buy(self):
        super().check_should_buy()
        if not self.check_enough_data() or not self.check_far_enough_in_past(self.last_buy):
            return False

        # TODO:

    def check_enough_data(self):
        three_days_ago = datetime.now() - timedelta(days=3)
        min_date = self.data[-1].date
        old_enough =  min_date < three_days_ago

        enough = len(self.data) >= 500
        return old_enough and enough

    def check_should_sell(self):
        super().check_should_sell()
        if not self.check_enough_data() or not self.check_far_enough_in_past(self.last_sell):
            return False

        # TODO:

    def check_if_last_sample_is_outlier(self):
        stddev = np.array([sample.price for sample in self.data]).std()
        return abs(self.data[-1].price) > self.sigma * stddev



    def determine_buy_volume(self, price, holdings, account_balance):
        super().determine_buy_volume(price, holdings, account_balance)
        volume = 2
        trans = TransationRecord('buy',datetime.now(),'XBT',price,volume,price*volume,'USD')
        self.last_buy=trans
        return volume
        # TODO:

    def determine_sell_volume(self, price, holdings, account_balance):
        super().determine_sell_volume(price, holdings, account_balance)
        volume = 2
        trans = TransationRecord('sell',datetime.now(),'XBT',price,volume,price*volume,'USD')
        self.last_sell=trans
        return volume

        # TODO:
