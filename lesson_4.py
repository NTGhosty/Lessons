from itertools import count

import numpy as np

# простые индексы
# срезы
# маскирование

x = np.arange(12).reshape((3, 4))
print(x)

# print(x[2])
# print(x[2, [2, 0, 1]])
# print(x[[2, 0, 1], 2])

# срезы
# print(x[1:])
# print(x[1:, [2, 0, 1]])

# маскирование
mask = np.array([1, 1, 1, 1], dtype=bool)
print(mask)
print(mask.shape)

row = np. array([0, 2])

print(row[:, np.newaxis].shape)

print(x[row[:, np.newaxis], mask])

# mask = np.array([1, 1, 1, 0], dtype=bool)
# row = np. array([0, 1, 2])
# # x[0][0] x[1][1] x[2][2]
# print(mask.shape)
# # (4,)
# print(row.shape)
# # (3,)
# print(x[row[:], mask])
# # [0 5 10]

rng = np.random.default_rng(seed = 1)
x = rng.multivariate_normal([0,0], [[1,2],[2,5]], 100)

print(x.shape)

import  matplotlib.pyplot as plt

# plt.scatter(x[:, 0], x[:, 1])
# plt.show()
#
# np.random.seed(0)
# ind = np.random.choice(100, 30, replace = False)
# print(ind)
#
# select = x[ind]
#
#
# plt.scatter(x[:, 0], x[:, 1], alpha = 0.3)
# plt.scatter(select[:, 0], select[:, 1], s = 200)
#
# plt.show()

x = np.arange(10)
print(x)
inx = np.array([2, 8, 4, 1])

# x [inx] = 99
x [inx] += 1
# np.add.at(x, inx, 1)
print(x)

rng = np.random.default_rng(seed = 1)
x = rng.integers(100, size = 100)
print(x[:10])

bins = np.linspace(0, 100, 11)
print(bins)

counts = np.zeros(11)
print(counts)

i = np.searchsorted(bins, x)
print(i[:10])

np.add.at(counts, i, 1)
print(counts)

print(sum(counts))

a = [3, 2, 5, 1, 4, 6, 78, 3, 54, 6, 3, 2 ,4 ,56]
# print(sorted(a))
#
# print(a)
#
# a.sort()
# print(a)

x = np.array(a)
print(x)
#
print(np.sort(x)) #sorted
print(x)
#
# x.sort()
inx = np.argsort(x)
print(inx)

print(x[inx])


rng = np.random.default_rng(seed = 1)
x = rng.integers(0, 10, size = (4,6))
print(x)

print(np.sort(x, axis = 1))
print(np.sort(x, axis = 0))

# структурированные массивы
# массивы записей
name = ["Ирина", "Виталий", "Олег", "Саша"]
age = [25, 17, 52, 44]
weight = [55.0, 57, 78, 72]

i = 1
print(name[i], age[i], weight[i])

data = np.zeros(
 4, dtype = {"names": ("name_", "age_", "weight_"), "formats": ("U10", "i4", "f8")}
)

print(data.dtype)

data["name_"] = name
data["age_"] = age
data["weight_"] = weight

print(data)

print(data[["name_"]])
print(data[0])
print(data[-1]["name_"])

data_rec = data.view(np.recarray)
print(data_rec)

print(data_rec.name_)
print(data_rec[0])
print(data_rec[-1].name_)

print(data["age_"] < 30)

print(data[data["age_"] < 30])
print(data[data["age_"] < 30]["name_"])

tp = np.dtype([("id", "i8"), ("mat", "f8", (3,3))])
x = np.zeros(2, dtype=tp)
print(x)

x["mat"][0] = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print(x)

data = [("Ирина", 25, 55), ("Виталий", 17, 57)]

dtype = {"names": ("name_", "age_", "weight_"), "formats": ("U10", "i4", "f8")}

data_rec = np.rec.array(data, dtype=dtype)
print(data_rec)

print(data_rec.name_)