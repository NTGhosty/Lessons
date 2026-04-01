import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# img = mpimg.imread('ttt.png')
# plt.imshow(img)
# plt.axis('off')
# plt.show()

#MATLAB
# x = np.linspace(0,10,100)
#
# plt.subplot(2,1,1)
# plt.plot(x, np.sin(x))
#
# plt.subplot(2,1,2)
# plt.plot(x, np.cos(x))
#
# print(plt.gcf())
# print(plt.gca())

# OO
# fig, ax = plt.subplots(2)
#
# print(fig)

# ax[0].plot(x, np.sin(x))
# ax[1].plot(x, np.cos(x))

# x = np.linspace(0,30,100)
# ax = plt.gca()

# ax.plot(x, np.sin(x), color='blue')
# ax.plot(x, np.sin(x-1), color='g', linestyle='solid') # -
# ax.plot(x, np.sin(x-2), color='0.75', linestyle='dashed') # --
# ax.plot(x, np.sin(x-3), color='#FFDDAA', linestyle='dashdot') # -.
# ax.plot(x, np.sin(x-4), color=(1.0, 0.2, 0.3), linestyle='dotted') # RGB :
# ax.plot(x, np.sin(x-5), color='salmon')
# ax.plot(x, np.sin(x-6), '--g')

# fig, ax = plt.subplots(5)
#
# ax[0].plot(x, np.sin(x))
# ax[1].plot(x, np.sin(x))
# ax[2].plot(x, np.sin(x))
# ax[3].plot(x, np.sin(x))
# ax[4].plot(x, np.sin(x))
#
# ax[1].set_xlim(-2, 12)
# ax[1].set_ylim(-1.5, 1.5)
#
# ax[2].set_xlim(12, -2)
# ax[2].set_ylim(1.5, -1.5)
#
# # ax[3].set_xlim('tight')
# ax[3].autoscale(tight=True)
#
# ax[4].axis('equal')

# plt.subplot(3,1,1)
# plt.plot(x, np.sin(x))
# plt.title('Синус')
# plt.xlabel('x')
# plt.ylabel('sin(x) $\sqrt{2}$')
#
# plt.subplot(3,1,2)
# plt.plot(x, np.sin(x), '-g', label = 'sin(x)')
# plt.plot(x, np.cos(x), ':b', label = 'cos(x)')
# plt.title('Синус и Косинус')
# plt.xlabel('x')
# plt.legend()
#
# plt.subplot(3,1,3)
# plt.plot(x, np.sin(x), '--k', label = '$\sin x$')
# plt.plot(x, np.cos(x), '-r', label = '$\cos x$')
# plt.title('Синус и Косинус - 2')
# plt.xlabel('x')
# plt.legend()
#
# plt.subplots_adjust(hspace=0.5)

# Д.рассеивание
# x = np.linspace(0,10,100)
# y = np.sin(x)

# plt.plot(x,y, '--o', markersize=15,
#          markerfacecolor='red',
#          markeredgecolor='blue',
#          markeredgewidth=3,
#          linewidth=4, color='black'
#          )

# rng = np.random.default_rng(1)
#
# colors = rng.random(100)
# sizes = 1000 * rng.random(100)
#
# plt.scatter(x,y, c = colors, s = sizes, alpha = 0.3)
# plt.colorbar()

# from sklearn.datasets import load_iris
#
# iris = load_iris(as_frame = True)
#
# print(iris.frame.head())
#
# plt.scatter(
#     iris.frame['sepal length (cm)'],
#     iris.frame['sepal width (cm)'],
#     s = 100 * iris.frame['petal length (cm)'],
#     c = iris.frame['target'],
#     alpha = 0.3
# )

# rng = np.random.default_rng(1)
#
# x = np.linspace(0,10,100)
# dy = 0.5
# y = np.sin(x) + dy * rng.random(100)
#
# plt.plot(x,y, "-k")
# plt.errorbar(x,y,yerr=dy, fmt='.r')
#
# plt.fill_between(x ,y - dy, y + dy, color = "0.75", alpha=0.3)

# графики плотности и контурный графики (на 2D изобразить 3D)

# x = np.linspace(0, 6, 50)
# y = np.linspace(0, 5, 40)
#
# X, Y = np.meshgrid(x, y)
# print(X.shape)
# print(Y.shape)
#
# print(X)
# print(Y)
#
#
# def f(x,y):
#     return np.sin(x) ** 4 + np.cos(y + x * 30) * np.sin(y)
#
#
# Z = f(X,Y)
#
# print(Z.shape)

# # plt.contour(X,Y,Z, colors='black')
# # plt.contour(X,Y,Z, 10, cmap='RdGy')
# cnt = plt.contour(X,Y,Z,10, colors='black')
# plt.clabel(cnt, inline=1)
# # plt.contourf(X,Y,Z, 10, cmap='RdGy')
# # plt.contourf(X,Y,Z, 10, cmap='RdGy r')
# plt.imshow(
#     Z,
#     extent=[0, 6, 0, 5],
#     origin='lower',
#     cmap='RdGy',
#     # interpolation='gaussian',
#     aspect='equal',
#     alpha=0.5
# )

# plt.colorbar()

rng = np.random.default_rng(1)
# data = rng.normal(size=1000)
# plt.hist(data, bins=30, density=True)

# x1 = rng.normal(0, 0.8, 1000)
# x2 = rng.normal(-2, 0.8, 1000)
# x3 = rng.normal(0, 0.8, 1000)
#
# p = dict(alpha = 0.3, bins = 40)
#
# plt.hist(x1, **p)
# plt.hist(x2, **p)
# plt.hist(x3, **p)
#
# plt.show()
# print(np.histogram(x1, bins = 1))

mean = [0,0]
cov = [[1,1],[1,3]]
x,y = rng.multivariate_normal(mean, cov, 10000).T

# plt.hist2d(x,y,bins=40)
plt.hexbin(x,y,gridsize=30)
plt.colorbar()

plt.show()

# print(np.histogram2d(x, y, bins = 2))
