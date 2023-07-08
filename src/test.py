from brain import Strategy, Order, Position, Agent, Brain
import yfinance as yf


class TestStrategy(Strategy):
    def init(self):
        pass

    def next(self):
        if self.agent.position:
            if self.data[-1].close > self.data[-2].close:
                if self.data[-2].close > self.data[-3].close:
                    self.sell()
        else:
            if self.data[-1].close < self.data[-2].close:
                if self.data[-2].close < self.data[-3].close:
                    self.buy()


if __name__ == "__main__":
    data = yf.Ticker('AAPL').history('ytd')
    print(data.columns)
    print(data['Close'][30])
    brain = Brain(TestStrategy, data)
    brain.run()
