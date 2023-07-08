from abc import ABC, abstractmethod
from typing import Type

import pandas as pd


class Position:
    def __init__(self, size, date):
        self.size = size
        self.date = date


class Agent:
    def __init__(self, starting_cash):
        self.starting_cash = starting_cash
        self.equity = 0
        self.cash = starting_cash
        self.position = None
        self.data = []
        self.pending_order = None

    def buy(self, order):
        self.pending_order = order

    def sell(self, order):
        self.pending_order = order

    def execute(self):
        if not self.pending_order:
            return
        if self.pending_order.typ == "BUY":
            self.cash -= self.data[-1].close * self.pending_order.size
            self.equity += self.data[-1].close * self.pending_order.size
            self.position = Position(self.pending_order.size, self.pending_order.date)
            self.pending_order = None
        elif self.pending_order.typ == "SELL":
            self.cash += self.data[-1].close * self.pending_order.size
            self.equity -= self.data[-1].close * self.pending_order.size
            self.position = None
            self.pending_order = None

    def stream(self, point):
        self.data.append(point)


class SingularPoint:
    def __init__(self, open, close, date="10-01-1000"):
        self.close = close
        self.open = open
        self.date = date


class Order:
    def __init__(self, size, date, typ="BUY"):
        self.size = size
        self.date = date
        self.typ = typ


class Strategy(ABC):

    def __init__(self, agent):
        self.data = []
        self.agent = agent

    def stream(self, point):
        self.data.append(point)
        self.agent.stream(point)

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def next(self):
        pass

    def buy(self, size=5):
        order = Order(size, self.data[-1].date, typ="BUY")
        self.agent.buy(order)

    def sell(self, size=5):
        order = Order(size, self.data[-1].date, typ="SELL")
        self.agent.sell(order)


class Brain:
    def __init__(self, _strategy : Type[Strategy], data):
        self.data = data
        self._strategy = _strategy
        self.length = len(data)
        self.agent = None
        self.strategy = None

    def run(self):
        self.agent = Agent(10000)
        self.strategy = self._strategy(self.agent)
        print("STARTING CASH: ", self.strategy.agent.cash)

        for i in range(self.length):

            self.strategy.agent.execute()

            point = SingularPoint(self.data['Open'][i], self.data['Close'][i])

            self.strategy.stream(point)
            if i > 6:
                self.strategy.next()

        self.strategy.sell()

        print("ENDING CASH: ", self.strategy.agent.cash)



