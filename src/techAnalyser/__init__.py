import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas_datareader as web
import talib as tb
import datetime as dt


class TechAnalysis:

    # This is the init part of vars and functions
    def __init__(self, data, startDate, endDate=dt.datetime.now()):
        self.startDate = startDate
        self.endDate = endDate
        self.data = web.DataReader(data, 'yahoo', self.startDate, self.endDate)

    def sma_plotter(self):
        self.data['SMA_100'] = tb.SMA(self.data['Close'], timeperiod=100)
        plt.plot(self.data['Close'], label='Close')
        plt.plot(self.data['SMA_100'], label='SMA_100')
        plt.show()

    def ema_plotter(self):
        self.data['EMA_200'] = tb.EMA(
            self.data['Close'], timeperiod=200)
        plt.plot(self.data['Close'], label='Close')
        plt.plot(self.data['EMA_200'], label='EMA_200')
        plt.show()

    def rmi_plotter(self):
        self.data['RSI'] = tb.RSI(self.data['Close'])
        fig, axis = plt.subplots(
            2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(10, 10))
        axis[0].plot(self.data['Close'], label='Close')
        axis[1].axhline(y=70, color='r', linestyle='--', label='RSI_70')
        axis[1].axhline(y=30, color='g', linestyle='--', label='RSI_30')
        axis[1].plot(self.data['RSI'], label='RSI', color='orange')
        plt.show()

    def linear_reg(self):
        self.data['LINEARREG'] = tb.LINEARREG(self.data['Close'], 200)
        plt.plot(self.data['Close'], label='Close')
        plt.plot(self.data['LINEARREG'], label='LINEARREG')
        plt.show()

    def for_macd(self):
        startDate = self.startDate
        self.data = web.DataReader("GS", "yahoo", startDate, self.endDate)
        macD, macD_sig, macD_hist = tb.MACD(self.data['Close'])
        fig, axis = plt.subplots(
            2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(10, 10))
        c = ["red" if cl < 0 else "green" for cl in macD_hist]
        axis[0].plot(self.data['Close'], label='Close')
        axis[1].plot(macD, 'b-')
        axis[1].plot(macD_sig, label='MACD-SIGNAL',
                     linestyle='--', color='orange')
        axis[1].bar(macD_hist.index, macD_hist, label='MACD-HIST', color=c)
        plt.show()

    def engf_patts(self):
        startDate = self.startDate
        self.data = web.DataReader(
            "^NSEI", "yahoo", startDate, self.endDate)
        self.data['ENGULFING'] = tb.CDLENGULFING(
            self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'])
        fig, axis = plt.subplots(2, 1, gridspec_kw={
            'height_ratios': [3, 1]}, figsize=(14, 10))
        colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000')
        mpf_style = mpf.make_mpf_style(
            marketcolors=colors, base_mpf_style="yahoo")
        mpf.plot(self.data, type='candle', style=mpf_style, ax=axis[0])
        axis[1].plot(self.data['ENGULFING'], label='ENGULFING', color='blue')
        plt.show()
