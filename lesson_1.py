import numpy as np
print(np.__version__)
import sys
import array
#Динамическая типизация
x = 1
print(type(x))

x = "hello"
print(type(x))

l = [True, "2", 3.0, 4]
print([type(i) for i in l])

print(sys.getsizeof(l))

l1 = []
print(type(l1))
print(sys.getsizeof(l1))

a1 = array.array('i', [])
print(type(a1))
print(sys.getsizeof(a1))

a1 = array.array('i', [1])
print(sys.getsizeof(a1))

a1 = array.array('i', [1,2])
print(sys.getsizeof(a1))

# Numpy and array - массивы хранят элементы одного типа

print(np.__version__)

# создание из списка

l = [1, 2, 3, 4, 5]
a = np.array(l)
print(a)
print(type(a))

print("list(python)", sys.getsizeof(l))
ap = array.array('i', l)
print("array(python)", sys.getsizeof(ap))
print("array(numpy)", sys.getsizeof(a))

#повышающее приведение типов
a = np.array([1.01, 2, 3, 4, 5, "a"])
print(type(a), a)

# явно задать тип
a = np.array([1.99, 2, 3, 4, 5], dtype=int)
print(type(a), a)

# Одномерные массивы range (i, j) -> i, i+1..., j-1
a = np.array(range(2, 5))
print(a)

# многомерные массивы
a = np.array([range(i, i + 5) for i in [1, 2, 3]])
#[1 2 3 4 5]
#[2 3 4 5 6]
#[3 4 5 6 7]
print(a)

# с нуля

# из 0
print(np.zeros(10, dtype=int))

# из
print(np.ones((3, 5), dtype=float))

# предопределенное значение
print(np.full(3,3), 3.1416)

# линейная последовательность чисел
print(np.arange(0, 20, 2))
print(np.arange(0, 20, 3))

# в интервале с одинаковыми промежутками
print(np.linspace(0, 1, 11))

# равномерное распределение от 0 до 1
print(np.random.random((2,4)))

# нормальное распределение
print(np.random.normal(0, 1, (2,4)))

# равномерное распределение от x до y
print(np.random.randint(0, 5, (2,2)))

# единичная матрица
print(np.eye(5, dtype=int))

# типы данных

a1 = np.zeros(10, dtype=int)
a2 = np.zeros(10, dtype='int16')
a3 = np.zeros(10, dtype=np.int16)

print(a1, type(a1), a1.dtype)
print(a2, type(a2), a2.dtype)
print(a3, type(a3), a3.dtype)

# Numerical Python = NumPy
# - атрибуты массивов
# - индексация
# - срезы
# - изменение формы
# - объединение и разбиение

# Атрибуты: ndim - число размерностей, shape - размер каждой размерности, size - общий размер массива

np.random.seed(1)

x1 = np.random.randint(10, size = 3)
print(x1)
print(x1.ndim, x1.shape, x1.size)
# 1 (3,) 3

x2 = np.random.randint(10, size = (3, 2))
print(x2)
print(x2.ndim, x2.shape, x2.size)

x3 = np.random.randint(10, size = (3, 2, 2))
print(x3)
print(x3.ndim, x3.shape, x3.size)

#Индексация

a = np.array([1, 2, 3, 4, 5])
print(a[0])

print(a[-2])

a[1] = 20
print(a)

# Многомерные

a = np.array([[1, 2], [3, 4]])
print(a)

print(a[0, 0])

print(a[-1, -2])

a[1,0] = 100
print(a)

# вставки (1 час 2 минуты)

a = np.array([1, 2, 3, 4, 5])
print(a.dtype)

a[0] = int("3")
print(a)
print(a.dtype)

a.dtype = float
print(a)
print(a.dtype)

# Срезы - подмассив массива [начало:конец:шаг] - [0:<конец>:1]

a = np.array([1, 2, 3, 4, 5])

print(a[:3])
print(a[3:])
print(a[1:4])
print(a[::2])
print(a[1::2])

# шаг < 0 [начало:конец:шаг] -> [конец:начало:шаг]

a = np.array([1, 2, 3, 4, 5])
print(a[::-1])

# Срезы в многомерных массивах

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(a)

print(a[:2, :3])
print(a[:,::2])

print(a[::-1,::-1])

print(a[:, 0])
print(a[0, :])
print(a[0])
#[[ 1  2  3  4]
# [ 5  6  7  8]
# [ 9 10 11 12]]

# Срезы в Python - копии подмассивов, NumPy - представление (view)

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(a)

a_2x2 = a[:2, :2]
print(a_2x2)

a_2x2[0,0] = 999
print(a)

a_2x2 = a[:2, :2].copy()
print(a_2x2)

a_2x2[0,0] = 1001
print(a_2x2)
print(a)

# Форма массива. Изменение

a = np.arange(1, 13)
print(a, a.shape, a.ndim)

print(a[3])
print(a[11])

a1 = a.reshape(1, 12)
print(a1, a1.shape, a1.ndim)
print(a1[0, 3])
print(a1[0, 11])

a2 = a.reshape(2, 6)
print(a2, a2.shape, a2.ndim)

a3 = a.reshape(2, 2, 3)
print(a3, a3.shape, a3.ndim)
print(a3[0, 1, 2])

a4 = a.reshape(1, 12, 1, 1)
print(a4, a4.shape, a4.ndim)
print(a4[0, 2, 0, 0])

a5 = a.reshape((2, 6))
print(a5, a5.shape, a5.ndim)

print(a5[1,4])

a6 = a.reshape((2, 6), order = "F")
print(a6, a6.shape, a6.ndim)
print(a6[1,4])

a = np.arange(1, 13)
print(a, a.shape, a.ndim)

a1 = a.reshape(1, 12)
print(a1, a1.shape, a1.ndim)

a2 = a[:, np.newaxis]
print(a2, a2.shape, a2.ndim)


