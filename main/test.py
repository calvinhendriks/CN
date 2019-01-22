import matplotlib.pyplot as plt
import scipy.stats as stats
import math as mth
import numpy as np

lower, upper = 1, 1000
mu, sigma = 12, 10.56
X = stats.truncnorm(
    (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
N = stats.norm(loc=mu, scale=sigma)
E = stats.expon(loc = mu, scale = sigma)

fig, ax = plt.subplots(3, sharex=True)
ax[0].hist(X.rvs(10000), density=True)
ax[1].hist(N.rvs(10000), density=True)
ax[2].hist(E.rvs(10000), density=False, bins=1000)
plt.show()



# print(X.rvs(size=100))
# print(X.mean())
# print(X.var())
# print(mth.sqrt(X.var()))
#
# dt = np.dtype([('scheme', np.unicode_, 16), ('size', np.int32), ('value', np.float64, (100,))])
#
# test = np.array([('seq', 1 , np.zeros(100)),('seq', 4 , np.zeros(100)),
#                      ('seq', 5 , np.zeros(100)),('seq', 8 , np.zeros(100)),
#                      ('del', 1 , np.zeros(100)),('del', 4 , np.zeros(100)),
#                      ('del', 5 , np.zeros(100)) ,('del', 8 , np.zeros(100))], dtype=dt)
# print(test)
# # a = test[test['scheme'] == 'seq']
# #
# # print(a)
#
# # b = test[np.logical_and(test['scheme'] == 'seq', test['size'] == 1)]
# # print(b)
# # b['value'][0][0] = 1
# # print(b)
# # b['value'][0][1] = 1100
# # print(b)
# # test['value'][0][0][test[np.logical_and(test['scheme'] == 'seq', test['size'] == 1)]] = 1.
#
#
# # print(a[test['size'] == 1])
# #
# # dt = np.dtype([('name', np.unicode_, 16), ('grades', np.float64, (2,))])
# # x = np.array([('Sarah', (8.0, 7.0)), ('John', (6.0, 7.0))], dtype=dt)
# #
# #
# # print(test[np.logical_and(test['scheme'] == 'seq', test['size'] == 1, test['value'][:,0] == 0.)])
# # # print(np.logical_and(test['scheme'] == 'seq', test['size'] == 1, test['value'][0][0] == 0.))
# #
# # print(test['size'][0] == 1)
# # print(test['value'][:,0] == 0. )
#
# test['value'][:,0][np.logical_and(test['scheme'] == 'seq', test['size'] == 1)] = 1.
# test['value'][:,1][np.logical_and(test['scheme'] == 'seq', test['size'] == 1)] = 2.
# a = test[np.logical_and(test['scheme'] == 'seq', test['size'] == 1)]['value'][0][0]
# print(a)
# print(test)
#
# # print(test[np.logical_and(test['scheme'] == 'seq', test['size'] == 1)]['value'] )