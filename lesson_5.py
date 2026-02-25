# Pandas
# Series
# DataFrame
# Index
import numpy as np
import pandas as pd
from pandas.core.methods.selectn import DataFrame

data = pd.Series([0.25, 0.5, 0.75, 1.0])
print(data)

print(data.values)
print(type(data.values))

print(data.index)

print(data[1])
print(data[1:3])

data = pd.Series([0.25, 0.5, 0.75, 1.0], index=['a', 'b', 'c', 'd'])
print(data)

print(data.index[0])
print(data['a'])
print(data['b':'d'])

data = pd.Series([0.25, 0.5, 0.75, 1.0], index=[1, 10, 7, 'd'])
print(data)

print(data.index)
print(type(data.index))
print(type(data.index[0]))
print(type(data.index[3]))

print(data[1])
print(data["d"])
print(data[10:"d"])

dict = {
    'A': 10,
    'B': 20,
    'C': 30,
    'D': 40,
    'E': 50,
}

data_dict = pd.Series(dict)
print(data_dict)
print(data_dict['B'])

print(data_dict['B':'D'])

#Списки
data = pd.Series([0.25, 0.5, 0.75, 1.0])
print(data)

data = pd.Series(5, index=[10, 20, 30])
print(data)

#Словарь
data_dict1 = pd.Series(dict, index=['A', 'B'])
print(data_dict1)

dict1 = {
    'A': 10,
    'B': 20,
    'C': 30,
    'D': 40,
    'E': 50,
    # 'F': 60,
}

data_dict1 = pd.Series(dict1)
print(data_dict1)

dict2 = {
    'A': 11,
    'B': 21,
    'C': 31,
    'D': 41,
    'E': 51,
    # 'H': 71,
}

data_dict2 = pd.Series(dict2)
print(data_dict2)

df = pd.DataFrame({'dict_01': data_dict1, 'dict_02': data_dict2})
print(df)

print(df.values)
print(type(df.values))

print(df.columns)
print(type(df.columns))

print(df.index)
print(type(df.index))

print(df['dict_01'])
print(df['dict_02'])

print(type(df['dict_01']))

df = pd.DataFrame({'dict_01': data_dict1})
print(df)

print(df.values)

print(data_dict1)
df = pd.DataFrame({'dict_01': data_dict1}, columns=['rrr'])
print(df)

print(pd.DataFrame([{'a': i, 'b': 2 * i} for i in range(4)]))

#NaN - Not a Number

print(pd.DataFrame(np.zeros(3)))

# Index - способ сослаться (reference) на данных в Series или в DataFrame

index = pd.Index([2, 5, 3, 5, 71])
print(index)
print(type(index))

print(index[1])
print(index[::2])

# index = 21

index1 = pd.Index([2, 5, 3, 5, 71])
index2 = pd.Index([1, 2, 51, 71, 4])

print(index1.intersection(index2))
print(index1.union(index2))
print(index1.symmetric_difference(index2))

# NumPy
# индексация arr[1,2]
# срезы arr[:, 1:4]
# маскирование arr[arr > 5]
# arr[0, [1,5]] arr[:, [1,5]]


data = pd.Series([0.25, 0.5, 0.75, 1.0], index=['a', 'b', 'c', 'd'])
print(data)

print(data['a'])

print('a' in data)
print('a1' in data)

print(list(data.items()))

print(data)
#
# data['a'] = 99
# print(data)
#
# data['a1'] = 990
# print(data)
#
# print(data['c': 'a1'])
#
# print(data[2:4])
# print(data[2:])

print(data[(data> 0.3) & (data < 0.8)])

print(data.loc[['c', 'a']])

print(data.iloc[[2, 0]])

# атрибут-индексаторы

dict1 = {
    'A': 10,
    'B': 20,
    'C': 30,
    'D': 40,
    'E': 50,
    # 'F': 60,
}

data_dict1 = pd.Series(dict1)
print(data_dict1)

dict2 = {
    'A': 11,
    'B': 21,
    'C': 31,
    'D': 41,
    'E': 51,
    # 'H': 71,
}

data_dict2 = pd.Series(dict2)
print(data_dict2)

df = pd.DataFrame({'dict_01': data_dict1, 'dict_02': data_dict2})
print(df)

# print(df['dict_01'])
# print(df.dict_01)

df['new'] = df['dict_01']
print(df)

df['new1'] = df['dict_01'] / df['dict_02']
print(df)

print(df.values)

print(df['dict_01']) # столбец
print(df.values[0]) # строка

print('ssss')
print(df)

print(df.loc['A':'C', :'dict_02'])
print(df.iloc[:3, :2])

print(df.loc[df.dict_02 > 30, ['new1', "dict_01"]])

df.loc[df.dict_02 > 30, ['new1', "dict_01"]] = 36
print(df)

rng = np.random.default_rng(1)
s = pd.Series(rng.integers(0, 10, 6))

print(s)

print(np.sum(s))

df = pd.DataFrame(rng.integers(0, 10, (3,4)), columns= ['A', 'B', 'C', 'D'])
print(df)

print(np.sin(df * 4))

dict1 = {
    'A': 10,
    'B': 20,
    'C': 30,
    'D': 40,
    'E': 50,
    'F': 60,
}

data_dict1 = pd.Series(dict1)
print(data_dict1)

dict2 = {
    'A': 11,
    'B': 21,
    'C': 31,
    'D': 41,
    'E': 51,
    'H': 71,
}

data_dict2 = pd.Series(dict2)
print(data_dict2)

df = pd.DataFrame({'dict_01': data_dict1, 'dict_02': data_dict2})
print(df)

print(data_dict1 + data_dict2)

print(np.add(data_dict1, data_dict2))

print(data_dict1.add(data_dict2, fill_value=5))

dict1 = {
    'A': 10,
    'B': 20,
    'C': 30,
    'D': 40,
    'E': 50,
}

data_dict1 = pd.Series(dict1)
print(data_dict1)

dict2 = {
    'A': 11,
    'B': 21,
    'C': 31,
    'D': 41,
    'E': 51,
}

data_dict2 = pd.Series(dict2)
print(data_dict2)

df = pd.DataFrame({'dict_01': data_dict1, 'dict_02': data_dict2})
print(df)

df1 = pd.DataFrame({'dict_10': data_dict1, 'dict_02': data_dict2})
print(df1)

print(df + df1)

print(df.add(df1, fill_value=df.value.sum()))

A = rng.integers(10, size = (3, 4))
print(A)

print(A[0])

print(A - A[0])

df = pd.DataFrame(A, columns = ['A', 'B', 'C', 'D'])
print(df)

print(df - df.iloc[0])

print(df.subtract(df['A'], axis=0))
