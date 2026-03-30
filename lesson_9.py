import numpy as np
import pandas as pd

# print(pd.date_range("2026-01-01", periods=4, freq="ME"))
#
# print(pd.date_range("2026-01-01", periods=4, freq="MS"))
#
# print(pd.date_range("2026-01-01", periods=4, freq="QE"))
#
# print(pd.date_range("2026-01-01", periods=4, freq="QS"))
#
# print(pd.date_range("2026-01-01", periods=4, freq="W"))
#
# print(pd.date_range("2026-01-01", periods=4, freq="4W-MON"))

# ind = pd.read_csv("data/index.csv", sep = ";", parse_dates = ["Date"])
#
# print(ind.head())
#
# print(type(ind))
# print(ind.dtypes)
#
# index = pd.DatetimeIndex(ind["Date"])
#
# ind.index = index
# ind = ind["Close"]
# print(ind.head())
#
# import matplotlib.pyplot as plt
#
# ind.plot()
# plt.show()

df = pd.read_csv(
    "data/FremontBridge.csv",
    index_col="Date",
    parse_dates=True,
    #date_format="%Y-%m-%d %I:%M:%S %p",
    date_format="%m/%d/%Y %I:%M:%S %p",
)
print(df.head())
print(df.dtypes)

print(df.columns)
df.columns = ["Total","East","West"]
print(df.head())

print(df.describe())
print(df.dropna().describe())

import matplotlib.pyplot as plt

# df.plot()
# plt.ylabel("Кол-во велосипедистов (в час)")
# plt.show()

# weekly = df.resample("D").sum()
# weekly.plot(style=["-",":","--"])
# plt.ylabel("Кол-во велосипедистов ( по неделям)")
# plt.show()

# daily = df.resample("D").sum()
# # center = False -> прошлые значения от выбранного
# # center = True -> прошлые и будущие значения от выбранного
# daily.rolling(30,center= True, win_type = "gaussian").mean(std = 5).plot(style=["-",":","--"])
# plt.ylabel("Средне месячное кол-во велосипедистов (скользящее окно)")
# plt.show()

# timely =  df.groupby(df.index.time).mean()
# ticks = 60 * 60 * 4 * np.arange(6)
# # print(ticks)
# timely.plot(xticks=ticks)
# plt.show()

# weekly = df.groupby(df.index.dayofweek).mean()
# weekly.plot()
# plt.show()

wl = np.where(df.index.weekday < 5, "Будни", "Выходные")
tl = df.groupby([wl,df.index.time]).mean()

fig,ax = plt.subplots(1, 2)
# ax[0].set_ylim(0,600)
# tl.loc["Будни"].plot(ax = ax[0], title = "Будни")
#
# ax[1].set_ylim(0,600)
# tl.loc["Выходные"].plot(ax = ax[1], title = "Выходные")
# plt.show()
#
# fig.savefig('ttt.png')

# timely =  df.groupby(df.index.time).mean()
# ticks = 60 * 60 * 4 * np.arange(6)
# # print(ticks)
# timely.plot(xticks=ticks)
# plt.show()

from IPython.display import Image

Image('ttt.png')

print(fig.canvas.get_supported_filetypes())

# MATPLOTLIB

# pip install matplotlib
# pip install pyqt5

plt.style.use('classic')

# plt.show() # ! Должно быть в единственном экземпляре