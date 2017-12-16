#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime, timedelta
from unittest import TestCase
from bitbaibai import NagatomoAlgorithm ,PriceSample,TransationRecord

class TestNagatomoAlgorithm(TestCase):

    def setUp(self):
        self.alg = NagatomoAlgorithm(3.0)

    def sample_data(self,n,sigma,mu):
        values = np.random.normal(mu,sigma,n)
        values[values >= 3* sigma] = sigma
        dt = timedelta(minutes=10)
        data = []
        for i in range(n):
            price = values[i]
            date = datetime.now() - dt*i
            sample = PriceSample(price, date,'XBT','USD')
            data.append(sample)
        return data


    def sample_price(self,date = datetime.now()):
        return PriceSample(15 , date,'XBT','USD')

    def test_can_be_instantiated(self):
        # assert 2 == 2
        alg = NagatomoAlgorithm(4.0)
        assert alg.sigma == 4.0

    def test_last_buy_sell_start_none(self):
        assert self.alg.last_buy is None
        assert self.alg.last_sell is None

    def test_starts_empty_data(self):
        assert len(self.alg.data) == 0

    def test_adds_data_when_received(self):
        self.alg.process_data([self.sample_price()])
        assert len(self.alg.data) ==1

    def test_does_not_overwrite_data(self):
        self.alg.process_data([self.sample_price()])
        self.alg.process_data([self.sample_price(), self.sample_price()])
        assert len(self.alg.data) == 3

    def test_dont_buy_data_too_new(self):
        date = datetime.now() - timedelta(days=2)
        self.alg.process_data([self.sample_price(date)])
        assert self.alg.check_should_buy() is False

    def test_dont_but_data_too_few(self):
        date = datetime.now() - timedelta(days=5)
        data = []
        for _ in range(499):
            data.append(self.sample_price(date))
        self.alg.process_data(data)
        assert self.alg.check_should_buy() is False

    def test_dont_sell_data_too_new(self):
        date = datetime.now() - timedelta(days=2)
        self.alg.process_data([self.sample_price(date)])
        assert self.alg.check_should_sell() is False

    def test_dont_sell_data_too_few(self):
        date = datetime.now() - timedelta(days=5)
        data = []
        for _ in range(499):
            data.append(self.sample_price(date))
        self.alg.process_data(data)
        assert self.alg.check_should_sell() is False

    def test_set_last_buy_on_buy(self):
        self.alg.determine_buy_volume(20,5,1000)
        assert self.alg.last_buy is not None

    def test_set_last_sell_on_sell(self):
        self.alg.determine_sell_volume(20,5,1000)
        assert self.alg.last_sell is not None

    def test_dont_buy_last_buy_too_recent(self):
        self.alg.last_buy = TransationRecord('buy',datetime.now(),'XBT',10,5,50,'USD')
        data = []
        date = datetime.now() - timedelta(days=5)
        for _ in range(600):
            data.append(self.sample_price(date))
        self.alg.process_data(data)
        assert self.alg.check_should_buy() is False

    def test_dont_sell_last_sell_too_recent(self):
        self.alg.last_sell = TransationRecord('sell',datetime.now(),'XBT',10,5,50,'USD')
        data = []
        date = datetime.now() - timedelta(days=5)
        for _ in range(600):
            data.append(self.sample_price(date))
        self.alg.process_data(data)
        assert self.alg.check_should_sell() is False


    def test_no_outlies(self):
        self.alg.data = self.sample_data(1000,1,100)
        assert self.alg.check_if_last_sample_is_outlier() is False



    def test_outlies(self):
        self.alg.data = self.sample_data(1000,1,100)
        self.alg.data.append(PriceSample(9999,datetime.now(),'XBT','USD')
        assert self.alg.check_if_last_sample_is_outlier() is True
