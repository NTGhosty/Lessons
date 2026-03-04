import numpy as np
import pandas as pd

# Отсутствующие данные
a = np.nan
a = -99999

# Pandas: 1) NaN, None 2) pd.NA
a = None
print(type(a))

a = np.array([1, 2, 3])
b = np.array([1, None, 3])
print(a.sum())
# print(b.sum())

c = np.array([1, np.nan, 3])
print(c)
print(c.sum())

print(1 + np.nan)
print(1 + np.nan)

# print(c.sum(c))
# print(c.nansum(c))

x = pd.Series([1, 2, 3, 4, 5], dtype = int)

print(x)
x[0] = None
x[1] = np.nan
print(x)

x = pd.Series(["1", "2", "3", "4", "5"])
print(x)
x[0] = None
x[1] = np.nan
print(x)

# x = pd.Series([True, False, False, True], dtype = bool)
# print(x)
# x[0] = None
# x[1] = np.nan
# print(x)

x = pd.Series([1, np.nan, None, 5])
print(x)


x = pd.Series([1, np.nan, None, 5, pd.NA])
print(x)

# int, uint, float
x = pd.Series([1, np.nan, None, 5, pd.NA], dtype = "Int32")
print(x)


x = pd.Series([1, np.nan, None, 5, "hello"])
print(x)

print(x.isnull())
print(x.notnull())
print(x[x.isnull()])
print(x[x.notnull()])

print(x.dropna())

x = pd.DataFrame([[1, np.nan, None], [1, 2, 3], [2, np.nan, 3]])
print(x)

print(x.dropna(axis=0))

print(x.dropna(axis=1))


x = pd.DataFrame([[1, np.nan, None], [1, 2, 3], [2, np.nan, 3]])
print(x)
# how = all - убрать если все значения отсутствуют
# how = ath - убрать, если хоть 1 значение отсутствует

print(x.dropna(axis=0, thresh=0)) # должно быть минимум N непустых



x = pd.DataFrame([None, 4, np.nan, None, 1, 2, 3], dtype = "Int32")
print(x)
print(x.fillna(-4))
print(x.ffill()) # заполняет предыдущим
print(x.bfill()) # заполняет следующим


x = pd.DataFrame([[1, np.nan, None], [1, 2, 3], [2, np.nan, 3]])
print(x)
print(x.ffill(axis = 1)) # заполняет предыдущим
print(x.bfill(axis = 1)) # заполняет следующим
print(x.ffill(axis = 0)) # заполняет предыдущим
print(x.bfill(axis = 0)) # заполняет следующим




# Иерархическая индексация
index = [
    ("A1", 2025),
    ("A1", 2026),
    ("A2", 2025),
    ("A2", 2026),
    ("A3", 2025),
    ("A3", 2026),
]

data = [1, 2, 3, 4, 5, 6]

s = pd.Series(data, index = index)
print(s)

# print(s[[i for i in s.index if i[0] == 'A1']])
mi = pd.MultiIndex.from_tuples(index)
print(mi)

s = s.reindex(mi)
print(s)

s1 = pd.Series(data, index = mi)
print(s1)


print(s['A1', :])

df = s.unstack()
print(df)

print(df.stack())

# одномерный Series может хранить данные с большим числом измерений

index = [
    ("A1", 2025, 1),
    ("A1", 2025, 2),
    ("A1", 2026, 1),
    ("A1", 2026, 2),
    ("A2", 2025, 1),
    ("A2", 2025, 2),
    ("A2", 2026, 1),
    ("A2", 2026, 2),
    ("A3", 2025, 1),
    ("A3", 2025, 2),
    ("A3", 2026, 1),
    ("A3", 2026, 2),
]

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
s = pd.Series(data, index = index)
print(s)

mi = pd.MultiIndex.from_tuples(index)
s = s.reindex(mi)
print(s)

print(s[:, 2025, 1])
df = s.unstack()
print(df)

df1 = pd.DataFrame(
    {
    "jan": s[:,:,1],
    "feb": s[:,:,2],
    "mar": s[:,:,1] + s[:,:,2],
    }
)
print(df1)

print(df1["mar"])
print(df1.loc["A1"])

print(df1.loc["A1", "feb"])

# print(df1.loc[[1, 0],[1, 1]])


rng = np.random.default_rng(1)

df = pd.DataFrame(
    rng.random((4, 2)),
    index = [["A1", "A1", "A2", "A2"], [2025, 2026, 2025, 2026]],
    columns = ["jan", "feb"],
)

print(df)

index = {
    ("A1", 2025, 1): 1,
    ("A1", 2025, 2): 2,
    ("A1", 2026, 1): 3,
    ("A1", 2026, 2): 4,
    ("A2", 2025, 1): 5,
    ("A2", 2025, 2): 6,
    ("A2", 2026, 1): 7,
    ("A2", 2026, 2): 8,
    ("A3", 2025, 1): 9,
    ("A3", 2025, 2): 10,
    ("A3", 2026, 1): 11,
    ("A3", 2026, 2): 12,
}

s = pd.Series(data)
print(s)

index = [
    ("A1", 2025, 1),
    ("A1", 2025, 2),
    ("A1", 2026, 1),
    ("A1", 2026, 2),
    ("A2", 2025, 1),
    ("A2", 2025, 2),
    ("A2", 2026, 1),
    ("A2", 2026, 2),
    ("A3", 2025, 1),
    ("A3", 2025, 2),
    ("A3", 2026, 1),
    ("A3", 2026, 2),
]

mi = pd.MultiIndex.from_tuples(index)
print(index)

mi = pd.MultiIndex.from_arrays([["A1", "A1", "A2", "A2"], [2025, 2026, 2025, 2026]])
print(mi)

mi = pd.MultiIndex.from_arrays([["A1", "A2"], [2025, 2026]])
print(mi)

mi = pd.MultiIndex(
    levels = [["A1", "A2"], [2025, 2026]],
    codes = [[1, 0, 0, 1],[1, 0, 1, 0]]
)
print(mi)

df = pd.DataFrame(
    rng.random((4, 2)),
    index = [["A1", "A1", "A2", "A2"], [2025, 2026, 2025, 2026]],
    columns = ["jan", "feb"],
)

df.index.names = ["property", "year"]
print(df)



mi1 = pd.MultiIndex.from_product([["A1", "A2"], [2025, 2026]], names=["property", "year"])
print(mi1)

mi2 = pd.MultiIndex.from_product([["B1", "B2", "B3"], ["jan", "feb"]], names=["shop", "month"])
print(mi2)

data = rng.random((4, 6))

print(data)

df = pd.DataFrame(data, index = mi1, columns = mi2)
print(df)