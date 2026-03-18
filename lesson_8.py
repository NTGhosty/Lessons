import numpy as np
import pandas as pd

# Строковые операции

data = ["one one one", "TWO TWO", "tHREE tHREE", "fOuR fOuR"]
print(data)

print([s.capitalize() for s in data])

names = pd.Series(data)
print(names)

print(names.str.capitalize())

print(names.str.lower())

print(names.str.len())

print(names.str.startswith('t'))

print(names.str.split())

data = ["one1 one2 one3", "two999 two ", "tHREE tHREE", "fOuR fOuR"]

rges = r"([a-z0-9]+\s)([a-z0-9]+\s).*"
a = names.str.extract(rges)
print(a)

print(type(a))

rges = r"([a-z0-9]+\s).*"
a = names.str.extract(rges)
print(a)

print(type(a))

data = ["one1 one2 one3", "two999 two ", "tHREE tHREE", "fOuR fOuR"]
names = pd.Series(data)

print(names.str.get(2))
print(names.str[2])

print(names.str[0:3])
print(names.str.slice(0,3))

print(names.str[-1])

# Индикаторные переменные
data = ["one1 one2 one3", "two999 two ", "tHREE tHREE", "fOuR fOuR"]
names = pd.DataFrame({
    "name": data,
    "info": ["A|B", "B|C", "A|B|C", "D"]
})

print(names)

print(names['info'].str.get_dummies('|'))

recipes = pd.read_json('data/recipeitems.json', lines=True)
print(recipes.head())

print(recipes.shape)

print(recipes.iloc[0])

print(recipes.ingredients.str.len())

print(recipes.ingredients.str.len().describe())

print(recipes.name[np.argmax(recipes.ingredients.str.len())])

print(recipes.description.str.contains('Breakfast').sum())
print(recipes.description.str.contains('breakfast').sum())

spices = ["salt","pepper","cream"]

result = pd.DataFrame({i: recipes.ingredients.str.contains(i) for i in spices})

print(result)

print(result.query("salt & pepper & cream"))

select = result.query("salt & pepper & cream")

print(select.index)

print(recipes.name[select.index].head())

# Работа с временными рядами
# - конкретные моменты времени т.е. абсолютные значения "1 января 2026 года 00:00"
# - периоды или временные интервалы - есть конечная и начальная точка. "март 2025 года", "24 часа"
# - продолжительность (временная дельта) = 15 минут

# Python
from datetime import datetime
import dateutil

d = datetime(year = 2026, month = 3, day = 4)
print(d)
print(type(d))

d = dateutil.parser.parse("4th of March, 2026")
print(d)
print(type(d))

print(d.strftime("%A"))

# Numpy

d = np.array("2026-03-04", dtype=np.datetime64)
print(d)
print(d.dtype)

print(d + 1)

d1 = np.array("2026-03-04 00:00", dtype=np.datetime64)
print(d1)
print(d1.dtype)

print(d1 + 1)

d2 = d + np.arange(12)
print(d2)

t = np.array(12, dtype = np.timedelta64)
print(t)
print(t.dtype)

# 2^64
d = np.array("2026-03-04", dtype=np.datetime64)
print(d)
print(d.dtype)

d = np.datetime64("2026-03-04" , "D")
print(d)
print(d + 1)

d = np.datetime64("2026-03-04", "Y")
print(d)
print(d + 1)

d = np.datetime64("2026-03-04", "W")
print(d)
print(d + 1)

d = np.datetime64("2026-03-04", "ns")
print(d)
print(d + 1)

t = np.timedelta64(1, "D")
print(t)
print(t + 1)

t1 = np.timedelta64(1, "M")
print(t)
print(t1 + 1)

# print(t + t1)



t = np.timedelta64(1, "s")
print(t)
print(t + 1)

t1 = np.timedelta64(1, "ms")
print(t)
print(t1 + 1)

print(t + t1)

print(np.timedelta64(t + t1, "ns"))

# Y M W D h m s


# Pandas
# Timestamp (numpy.datetime64)

d = pd.to_datetime("4th of March, 2026")
print(d)
print(type(d))

print(d.strftime("%A"))

d2 = d + pd.to_timedelta(np.arange(30), "D")
print(d2)
print(type(d2))

index = d2
data = pd.Series(np.arange(30), index = index)

print(data)

print(data["2026-03-06"])

# Работа с временными рядами
# - конкретные моменты времени т.е. абсолютные значения "1 января 2026 года 00:00"
# Pandas: Timestamp (np.datetime64)
# - периоды или временные интервалы - есть конечная и начальная точка. "март 2025 года", "24 часа"
# Pandas: Period (np.datetime64) - PeriodIndex
# - продолжительность (временная дельта) = 15 минут
# Pandas: Timedelta (np.timedelta64) - TimedeltaIndex

d = pd.to_datetime("4th of March, 2026")
print(d)
print(type(d))

ds = pd.to_datetime(["2026-03-04", "2026-03-05"])
print(ds)

p = ds.to_period("D")
print(p)
print(type(p))

delt = ds[1] - ds[0]
print(delt)
print(type(delt))

idelt = ds - ds[0]
print(idelt)
print(type(idelt))

hh = pd.date_range("2026-01-01", periods=10, freq="h")

print(hh)
print(hh[0] + 2 * hh.freq)

print(pd.period_range("2026-01-01", periods=10, freq="M"))

print(pd.timedelta_range(0, periods=10, freq="h"))

# Коды периодичности
# M Q A - конец
# MS QS AS - конец

p1 = pd.Period("2026Q1")
print(p1)
print(p1.month)
print(p1.day)

print(pd.timedelta_range(0, periods=10, freq="2h15min"))

from pandas.tseries.offsets import BDay

hh = pd.date_range("2026-01-01", periods=10, freq=BDay())
print(hh)

